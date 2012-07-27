'''
Created on 21 Feb 2011

@author: alex
'''

from timezero.serializers import GameSerializer, ChatSerializer
from timezero.connection import Connection, PacketDispatcher

from xml.dom import minidom
import time

def attributes(xmlnode):
    result = {}
    for k, v in xmlnode._attrs.items():
        result[k] = v.value
    return result

def copyEntries(dict, fields):
    for k, v in dict.items():
        fields[k] = v
        
def subnodes(node):
    result = []
    for i in node.childNodes:
        if i.nodeType == minidom.Node.ELEMENT_NODE:
            result.append(i)
            
    return result

class Session(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.session = ""
        self.params = ""
        
        self.myParams = {}
        self.inventory = []
        self.bots = []
        self.locations = {}
        
    def clearBots(self):
        self.bots = []
        
    def addBot(self, attr):
        self.bots.append(attr)

class GameClient(object):
    def __init__(self, session):
        self.dispatcher = PacketDispatcher()
        self.dispatcher.addConnection("game", Connection(GameSerializer()))
        self.dispatcher.addConnection("chat", Connection(ChatSerializer()))
        
        self.scheduledTasks = []        
        self.logicHandler = None
        
        self.session = session
        self.state = None
    
    def connect(self, name, host):
        self.dispatcher.connect(name, host, 5190)
        
    def schedule(self, timeout, task):
        self.scheduledTasks.append((time.clock() + timeout, task))
    
    def loop(self):
        while True:
            self.dispatcher.handleInput(0.1)
            if self.logicHandler != None:
                self.logicHandler()
            
            copied = self.scheduledTasks[:]
            for task in copied:
                if time.clock() > task[0]:
                    task[1]()
                    self.scheduledTasks.remove(task)

class GameState(object):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.dispatcher = client.dispatcher
        
        self.dispatcher.addPacketHandler("game", "BOT", self.BOT_handler)
        self.dispatcher.addPacketHandler("game", "DLG", self.DLG_handler)
        self.dispatcher.addPacketHandler("game", "SPECIAL", self.SPECIAL_handler)
        self.dispatcher.addPacketHandler("game", "BAFF", self.BAFF_handler)
        self.dispatcher.addPacketHandler("game", "MYPARAM", self.MYPARAM_handler)
        self.dispatcher.addPacketHandler("game", "GOBLD", self.GOBLD_handler)
        self.dispatcher.addPacketHandler("game", "GOLOC", self.GOLOC_handler)
        self.dispatcher.addPacketHandler("game", "ERRGO", self.ERRGO_handler)
        
        self.dispatcher.addPacketHandler("chat", "S", self.S_handler)
        self.dispatcher.addPacketHandler("chat", "A", self.A_handler)
        self.dispatcher.addPacketHandler("chat", "D", self.D_handler)
        self.dispatcher.addPacketHandler("chat", "R", self.R_handler)
        
        self.client.schedule(45, self.sendPing)
        
        self.dispatcher.send("game", "<GETME/>")
    
    def sendPing(self):
        print "Ping!"
        self.dispatcher.send("chat", "<N />")
        self.dispatcher.send("game", "<N />")
        self.client.schedule(45, self.sendPing)
    
    def sendChatMessage(self, text):
        self.dispatcher.send("chat", '<POST t="%s" />' % text)
        
    def goOut(self):
        self.dispatcher.send("game", '<GOBLD n="0" />')
    
    def goBuilding(self, n):
        self.dispatcher.send("game", '<GOBLD n="%d" />' % n)
        
        #-> <GOBLD n="0" />
        #<- <BOT clear="1" />
        #<- <GOBLD n="0" n="0" hz="0" owner="0"/>
        #<- (chat) R
        #-> <GOLOC d="123456789" />
        #<- <GOLOC n="0">
        #    <L X="119" Y="49" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="120" Y="49" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="121" Y="49" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="119" Y="50" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="120" Y="50" tm="5" t="A" m="*dDFdJFeFDeHDgLEgNEgQEiFiGiHiIiHiHlYElYElYElYElZElZElZElZElZElZEl[El]El_ElaElbElcElcElcElrElsElsDltEltEltDluDluDlvDlxDl|Dl|DrGFtBGtCEtDFtDFtEEtEDtHEtHFtIFtJEtKEtOGt[Et_Ft`FtcFtfFtgFtiF" flags="16" p="0">
        #        <B X="288" Y="228" Z="1" name="2"Old Arsenal" N="0" layer="8"/>
        #        <B X="648" Y="342" Z="2" name="50"Incubator" N="0" layer="8"/>
        #    </L>
        #    <L X="121" Y="50" tm="10" t="A" m="*eBDeHEeKDgLEgMFgOEgQEiGiGlZGlZGlZGl[Gl[Gl^Gl^Gl`GlsGl|ElGrKFtEGtEFtFFtHGtHGtIGtKGtKGtKGtLGtMGtOGtXGt]Gt_Ft`GtgGtqF" flags="16">
        #        <B X="558" Y="247" Z="1" name="11"Portal" N="0" layer="9"/>
        #    </L>
        #    <L X="119" Y="51" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="120" Y="51" tm="20" t="A" flags="16" o="999" b="1" z="0"/>
        #    <L X="121" Y="51" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
        #    </GOLOC>
        #
        #-> <GOBLD n="1" />
        #<- <BOT clear="1" /><GOBLD n="1" n="1" hz="2" owner="0"/>
        #-> <AR />
        #<- <AR ... />
        
        #-> <AR a="54721599782.2" c="300" s="0" />
        #-> <NEWID />
        
        #-> <GETINFO login="Journal Forpost" />
        #<- <USERPARAM login="Journal Forpost" F"1" str="4" dex="4" int="6" pow="9" HP="20" psy="0" bio="0" stamina="1maxHP="20" maxPsy="15" maxBio="15" regday="11.09.2010Pabout="   1-10www.tzjournal.ru/pubs/169/  TimeZerowww.tzjournal.ru/quests/      www.tzjournal.ru/locator/         www.tzjournal.ru/analizator/   www.tzjournal.ru/gallery/ www.tzjournal.ru/rating/   www.tzjournal.ru/news/21/     www.tzjournal.ru/news/75/   www.tzjournal.ru/blacklist/          " ne=",,,,," ne2=",,,,,,,,,,,,,,,," serverid="2" man="1" siluet="type=1,body=5,body2=1,head=3,rgb=40,hair=21" clanF="-2" name="  TimeZero  FortPost" city="    www.tzjournal.ru" clan="" ROOM="0" X="120" Y="50" confattack="1" dpsy="" btlformat="-108"52710443829.2XB"a1-b1"Boots"/52710443830.2XG"1-p4"Ingram"/52710443832.2XA"a1-t1"Jeans"/52710443833.2XCDE"a1-c2"Jeans vest"/></USERPARAM>
    
        #<GETINFO login="Journal Forpost" details="1" />
        
        #-> <GOLOC n="6" d="369" t1="1298536047" t2="1298528846" />
        #<- <ERRGO />
    
    def S_handler(self, packet):
        text = attributes(packet)["t"]
        (unknown, sep, text) = text.partition(":")
        (hours, sep, text) = text.partition(":")
        (minutes, sep, text) = text.partition(" ")
        
        print "chat message : %s" % text.encode("cp1251")
        return True
        
    def A_handler(self, packet):
        print "Player %s entered the room" % packet._attrs["t"].value.encode("cp1251")
        return True
        
    def D_handler(self, packet):
        print "Player %s left the room" % packet._attrs["t"].value.encode("cp1251")
        return True
    
    def R_handler(self, packet):
        text = attributes(packet)["t"]
        return True
        
    def BOT_handler(self, packet):
        if "clear" in attributes(packet):
            self.session.clearBots()
        elif "addbot" in attributes(packet):
            self.session.addBot(attributes(packet))
        return True
    
    def DLG_handler(self, packet):
        return True
    
    def MYPARAM_handler(self, packet):
        copyEntries(attributes(packet), self.session.myParams)
        for node in subnodes(packet):
            self.session.inventory.append(attributes(node))
            
        return True
            
    def SPECIAL_handler(self, packet):
        return True
    
    def BAFF_handler(self, packet):
        return True
    
    def GOBLD_handler(self, packet):
        if attributes(packet)["n"] == "0":
            self.dispatcher.send("game", '<GOLOC d="123456789" />')
            
        print attributes(packet)
        return True
    
    def GOLOC_handler(self, packet):
        if attributes(packet)["n"] == "0":
            #<L X="119" Y="49" tm="120" t="A" flags="16" o="999" b="1" z="0"/>
            for node in subnodes(packet):
                attrs = attributes(node)
                x = int(attrs["X"])
                y = int(attrs["Y"])
                
                attrs["buildings"] = []
                for subnode in subnodes(node):
                    attrs["buildings"].append(attributes(subnode))
                
                if (x, y) not in self.session.locations:
                    self.session.locations[(x, y)] = {}
                
                copyEntries(attrs, self.session.locations[(x, y)])
        return True
                
    def ERRGO_handler(self, packet):
        
        return True
    
class LoginState(object):
    def __init__(self, client, onLogin):
        self.client = client
        self.session = client.session
        self.dispatcher = client.dispatcher    
        self.dispatcher.addPacketHandler("game", "KEY", self.KEY_handler)
        self.onLogin = onLogin
    
    def KEY_handler(self, packet):
        key = packet._attrs["s"].value
        self.dispatcher.send(
            "game",
            '<LOGIN lang="ru" v2="7.0.1" v="108" p="%s" l="%s" />' 
            % (self.session.password, self.session.name)
        )
        
        self.dispatcher.addPacketHandler("game", "ERROR", self.ERROR_handler)
        self.dispatcher.addPacketHandler("game", "OK", self.OK_handler)
        
        return False
    
    def ERROR_handler(self, packet):
        print "error: " + packet._attrs["code"].value
        return False
        
    def OK_handler(self, packet):
        self.session.name = packet._attrs["l"].value
        self.session.session = packet._attrs["ses"].value
        self.session.params = packet._attrs["params"].value
        
        self.dispatcher.send("game", '<CHAT/>')
        
        self.dispatcher.addPacketHandler("game", "CLIENT_STATUS", self.CLIENT_STATUS_handler)
        self.dispatcher.addPacketHandler("game", "UPDATE_VER", self.UPDATE_VER_handler)
        self.dispatcher.addPacketHandler("game", "CHAT", self.CHAT_handler)
        return False
    
    def CLIENT_STATUS_handler(self, packet):
        print "client_status : " + packet._attrs["val"].value
        return False
        
    def UPDATE_VER_handler(self, packet):
        print "update_ver : " + packet._attrs["ver"].value
        (self.onLogin)()
        return False
        
    def CHAT_handler(self, packet):
        self.dispatcher.connect("chat", packet._attrs["server"].value, 5190)
        self.dispatcher.send("chat", 
            '<CHAT ses="%s" l="%s" />' % (self.session.session, self.session.name))
        return False


if __name__ == '__main__':    
    client = GameClient(Session("YOURNAME", "YOURPASSWORD"))
    client.connect("game", "city2.timezero.ru")
    
    def onLogin():
        client.state = GameState(client)
        return
    
    client.state = LoginState(client, onLogin)
    client.loop()
    pass