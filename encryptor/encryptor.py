'''
Created on 22 Feb 2011

@author: alex
'''

from numpy import uint32

replaceTable = \
    [35,6,4,25,7,8,36,16,20,37,12,31,39,38,\
     21,5,33,15,9,13,29,23,32,22,2,27,1,10,\
     30,24,0,19,26,14,18,34,17,28,11,3]
        
def bit_rol(num, cnt):
    unum = uint32(num)
    ures = to_int( ((unum << cnt) | (unum >> (32 - cnt))) )
    return to_int(ures)

def to_int(x): 
    val = x & 0xFFFFFFFF
    if val > 0x7FFFFFFF:
        val = - ((-val) & 0xFFFFFFFF)
    return int(val)

def encrypt(data, key):
    data = data[0:1] + key[0:10] + data[1:] + key[10:]
    dataLength8 = len(data) * 8
    
    temp = (((dataLength8 + 64) >> 9) << 4) + 16
    buffer1 = [uint32(0)] * temp
    
    i = 0
    while i < dataLength8:
        buffer1[i >> 5] = buffer1[i >> 5] | (ord(data[i >> 3]) & 0xFF) << 24 - (i & 0x1F)
        i += 8
    
    buffer1[dataLength8 >> 5] = buffer1[dataLength8 >> 5] | 128 << 24 - (dataLength8 & 0x1F)
    buffer1[len(buffer1) - 1] = dataLength8
    
    #print buffer1
    
    buffer2 = [uint32(0)] * 80
        
    _loc13 = (1732584193)
    _loc6 = (-271733879)
    _loc8 = (-1732584194)
    _loc7 = (271733878)
    _loc14 = (-1009589776)
    _loc15 = (0)
    _loc21 = (0)
    _loc19 = (0)
    _loc23 = (0)
    _loc10 = (0)
    _loc38 = (0)
    _loc2 = (0)
    _loc4 = (0)
    _loc3 = (0)
    
    #print _loc14
    
    flag = False
    i = 0
    while i < len(buffer1):
        _loc32 = _loc13
        _loc31 = _loc6
        _loc30 = _loc8
        _loc29 = _loc7
        _loc28 = _loc14
        k = 0
        while k < 80:
            if k < 16:
                buffer2[k] = buffer1[i + k]
            else:
                _loc16 = buffer2[k - 3] ^ buffer2[k - 8] ^ buffer2[k - 14] ^ buffer2[k - 16]
                buffer2[k] = bit_rol(_loc16, 1)
            #Console.WriteLine(buffer2[k]);
            _loc20 = bit_rol(_loc13, 5)
            _loc4 = _loc14
            _loc3 = buffer2[k]
            _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
            _loc15 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
            _loc23 = to_int( (1518500249) if k < 20 else ((1859775393) if k < 40 else ((-1894007588) if k < 60 else (-899497514))) )
            _loc4 = _loc15
            _loc3 = _loc23
            _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
            _loc21 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
            while True:
                if flag:
                    if k < 20:
                        _loc10 = to_int( (_loc6 & _loc8 | (_loc6 ^ (0xFFFFFFFF)) & _loc7) )
                    elif k < 40:
                        _loc10 = to_int( _loc6 ^ _loc8 ^ _loc7 )
                    elif k < 60:
                        _loc10 = to_int( _loc6 & _loc8 | _loc6 & _loc7 | _loc8 & _loc7 )
                    else:
                        _loc10 = to_int( _loc6 ^ _loc8 ^ _loc7 )
                    _loc4 = _loc20
                    _loc3 = _loc10
                    _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
                    _loc19 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
                flag = not flag
                if not flag:
                    break
            _loc4 = _loc19
            _loc3 = _loc21
            _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
            _loc22 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
            _loc14 = _loc7
            _loc7 = _loc8
            _loc8 = bit_rol(_loc6, 30)
            _loc6 = _loc13
            _loc13 = _loc22
            k += 1
        _loc4 = _loc13
        _loc3 = _loc32
        _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
        _loc13 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
        _loc4 = _loc6
        _loc3 = _loc31
        _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
        _loc6 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
        _loc4 = _loc8
        _loc3 = _loc30
        _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
        _loc8 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
        _loc4 = _loc7
        _loc3 = _loc29
        _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
        _loc7 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535 )
        _loc4 = _loc14
        _loc3 = _loc28
        _loc2 = to_int( (_loc4 & 0xFFFF) + (_loc3 & 0xFFFF) )
        _loc14 = to_int( (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 0xFFFF )
        i += 16
    output = [_loc13, _loc6, _loc8, _loc7, _loc14]
    
    #print output
    
    hexchars = "0123456789ABCDEF"
    retval = [' ']*40
    i = 0
    while i < 20:
        retval[replaceTable[i * 2]] = hexchars[output[i >> 2] >> (3 - i % 4) * 8 + 4 & 15]
        retval[replaceTable[i * 2 + 1]] = hexchars[output[i >> 2] >> (3 - i % 4) * 8 & 15]
        i += 1
    return ''.join(retval)