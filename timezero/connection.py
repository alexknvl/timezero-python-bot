'''
Created on 22 Feb 2011

@author: alex
'''

import socket

from select import select
from xml.dom import minidom

class Connection(object):
    def __init__(self, serializer):
        self.connected = False
        self.buffer = ""
        self.queue = []
        self.host = ""
        self.port = 0
        self.serializer = serializer
    
    def connect(self, host, port):
        self.host = host
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.setblocking(False)
        
        self.connected = True
    
    def close(self):
        self.socket.close()
        self.socket = None
        self.host = ""
        self.port = 0
        self.connected = False
        
    def write(self, s):
        self.socket.send(self.serializer.serialize(s) + "\x00")
    
    def __read(self, timeout):
        r, w, e = select([self.socket], [], [], timeout)
        
        if (len(r) != 0):
            self.buffer += self.socket.recv(4096)
            
            while True:
                head, sep, tail = self.buffer.partition("\x00")
                if sep == "\x00":
                    self.buffer = tail
                    head = self.serializer.deserialize(head)
                    head = head.decode("utf-8")
                    self.queue.append(head)
                else:
                    break
    
    def read(self, blocking = False, timeout = 0.1):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        
        self.__read(timeout)
            
        if blocking:
            while len(self.queue) == 0:
                self.__read(timeout)
            return self.queue.pop(0)
        else:
            if len(self.queue) > 0:
                return self.queue.pop(0)
            return None
        
class PacketDispatcher(object):
    def __init__(self):
        self.connections = {}
        
    def addConnection(self, name, connection):
        if name in self.connections:
            raise Exception("connections must have unique names")
        
        self.connections[name] = {
            "connection":connection, 
            "listeners":{}
        }
        
    def removeConnection(self, name, connection):
        if name in self.connections:
            del self.connections[name]
            
    def addPacketHandler(self, connName, packetName, handler):
        if connName not in self.connections:
            raise Exception(
                "could not add packet handler :" + 
                "connection %s does not exist" % connName
            )
        
        listeners = self.connections[connName]["listeners"]
            
        if packetName not in listeners:
            listeners[packetName] = []
            
        listeners[packetName].append(handler)
    
    def removePacketHandler(self, connName, packetName, handler):
        if connName not in self.connections:
            return
        
        listeners = self.connections[connName]["listeners"]
        
        if packetName not in listeners:
            return
        
        listeners[packetName].remove(handler)
    
    def handleRawPacket(self, connName, rawPacket):
        if connName not in self.connections:
            raise Exception(
                "invalid arguments :" +
                "connection %s does not exist" % connName
            )
        
        listeners = self.connections[connName]["listeners"]
        
        document = minidom.parseString("<packet>" + rawPacket.encode("utf-8") + "</packet>")
        document = document.firstChild
        
        print rawPacket.encode("cp1251", "ignore")
        
        for node in document.childNodes:
            if node.nodeType == minidom.Node.ELEMENT_NODE:
                if node.nodeName in listeners:
                    copiedListeners = listeners[node.nodeName][:]
                    listeners[node.nodeName] = []
                    
                    for handler in copiedListeners:
                        if handler(node) == True:
                            listeners[node.nodeName].append(handler)
                else:
                    print "Unknown packet : %s" % node.nodeName
                
    def handleInput(self, timeout):
        timeout = timeout / len(self.connections)
        
        for k, v in self.connections.items():
            connection = v["connection"]
            if connection.connected:
                rawPacket = connection.read(False, timeout)
                if rawPacket != None:
                    self.handleRawPacket(k, rawPacket)
                
    def send(self, connName, packet):
        if connName not in self.connections:
            raise Exception(
                "invalid arguments :" +
                "connection %s does not exist" % connName
            )
        connection = self.connections[connName]["connection"]
        connection.write(packet)
        
    def connect(self, connName, host, port):
        if connName not in self.connections:
            raise Exception(
                "invalid arguments :" +
                "connection %s does not exist" % connName
            )
        connection = self.connections[connName]["connection"]
        connection.connect(host, port)
    