using System;
using System.Collections.Generic;
using System.Text;

namespace Timezero
{
    public class Encryptor
    {
        private static int[] ReplaceTable = 
        {
            35,		//0
		    6,		//1
		    4,		//2
		    25,		//3
		    7,		//4
		    8,		//5
		    36,		//6
		    16,		//7
		    20,		//8
		    37,		//9
		    12,		//10
		    31,		//11
		    39,		//12
		    38,		//13
		    21,		//14
		    5,		//15
		    33,		//16
		    15,		//17
		    9,		//18
		    13,		//19
		    29,		//20
		    23,		//21
		    32,		//22
		    22,		//23
		    2,		//24
		    27,		//25
		    1,		//26
		    10,		//27
		    30,		//28
		    24,		//29
		    0,		//30
		    19,		//31
		    26,		//32
		    14,		//33
		    18,		//34
		    34,		//35
		    17,		//36
		    28,		//37
		    11,		//38
		    3		//39
        };
        private static int bit_rol(int num, int cnt)
        {
            uint unum = BitConverter.ToUInt32(BitConverter.GetBytes(num), 0);
            uint ures = ((unum << cnt) | (unum >> (32 - cnt)));
            return BitConverter.ToInt32(BitConverter.GetBytes(ures), 0);
        }
        public static string Encrypt(string data, string key)
        {
            data = data.Substring(0, 1) + key.Substring(0, 10) + data.Substring(1) + key.Substring(10);
            int dataLength8 = data.Length * 8;

            int[] buffer1 = new int[((dataLength8 + 64) >> 9 << 4) + 16];
            for (int i = 0; i < buffer1.Length; i++) buffer1[i] = 0;

            for (int i = 0; i < dataLength8; i += 8) buffer1[i >> 5] = buffer1[i >> 5] | (data[i >> 3] & 0xFF) << 24 - (i & 0x1F);
            buffer1[dataLength8 >> 5] = buffer1[dataLength8 >> 5] | 128 << 24 - (dataLength8 & 0x1F);
            buffer1[buffer1.Length - 1] = dataLength8;

            int[] buffer2 = new int[80];
            for (int i = 0; i < buffer2.Length; i++) buffer2[i] = 0;

            int _loc13 = 1732584193;
            int _loc6 = -271733879;
            int _loc8 = -1732584194;
            int _loc7 = 271733878;
            int _loc14 = -1009589776;
            int _loc15 = 0;
            int _loc21 = 0;
            int _loc19 = 0;
            int _loc23 = 0;
            int _loc10 = 0;
            int _loc38 = 0;
            int _loc2 = 0;
            int _loc4 = 0;
            int _loc3 = 0;
            bool flag = false;
            for (int i = 0; i < buffer1.Length; i+=16)
            {
                int _loc32 = _loc13;
                int _loc31 = _loc6;
                int _loc30 = _loc8;
                int _loc29 = _loc7;
                int _loc28 = _loc14;

                for (int k = 0; k < 80; ++k)
                {
                    if (k < 16)
                    {
                        buffer2[k] = buffer1[i + k];
                    }
                    else
                    {
                        int _loc16 = buffer2[k - 3] ^ buffer2[k - 8] ^ buffer2[k - 14] ^ buffer2[k - 16];
                        buffer2[k] = bit_rol(_loc16, 1);
                        //Console.WriteLine(buffer2[k]);
                    }
                    int _loc20 = bit_rol(_loc13, 5);
                    _loc4 = _loc14;
                    _loc3 = buffer2[k];
                    _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                    _loc15 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                    _loc23 = k < 20 ? (1518500249) : (k < 40 ? (1859775393) : (k < 60 ? (-1894007588) : (-899497514)));
                    _loc4 = _loc15;
                    _loc3 = _loc23;
                    _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                    _loc21 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                    do
                    {
                        if (flag)
                        {
                            if (k < 20)
                            {
                                _loc10 = (int)(_loc6 & _loc8 | (_loc6 ^ 0xFFFFFFFF) & _loc7);
                            }
                            else if (k < 40)
                            {
                                _loc10 = _loc6 ^ _loc8 ^ _loc7;
                            }
                            else if (k < 60)
                            {
                                _loc10 = _loc6 & _loc8 | _loc6 & _loc7 | _loc8 & _loc7;
                            }
                            else
                            {
                                _loc10 = _loc6 ^ _loc8 ^ _loc7;
                            }
                            _loc4 = _loc20;
                            _loc3 = _loc10;
                            _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                            _loc19 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                        }
                        flag = !flag;
                    } while (flag);
                    _loc4 = _loc19;
				    _loc3 = _loc21;
				    _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
				    int _loc22 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
				    _loc14 = _loc7;
				    _loc7 = _loc8;
                    _loc8 = bit_rol(_loc6, 30);
				    _loc6 = _loc13;
				    _loc13 = _loc22;
                }
                _loc4 = _loc13;
                _loc3 = _loc32;
                _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                _loc13 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                _loc4 = _loc6;
                _loc3 = _loc31;
                _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                _loc6 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                _loc4 = _loc8;
                _loc3 = _loc30;
                _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                _loc8 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                _loc4 = _loc7;
                _loc3 = _loc29;
                _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                _loc7 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
                _loc4 = _loc14;
                _loc3 = _loc28;
                _loc2 = (_loc4 & 65535) + (_loc3 & 65535);
                _loc14 = (_loc4 >> 16) + (_loc3 >> 16) + (_loc2 >> 16) << 16 | _loc2 & 65535;
            }
            int[] output = new int[]{_loc13, _loc6, _loc8, _loc7, _loc14};
		    string hexchars = "0123456789ABCDEF";
		    char[] retval = new char[40];

    	    for (int i = 0; i < 20; ++i)
		    {
			    retval[ReplaceTable[i*2]] = hexchars[output[i >> 2] >> (3 - i % 4) * 8 + 4 & 15];
			    retval[ReplaceTable[i*2+1]] = hexchars[output[i >> 2] >> (3 - i % 4) * 8 & 15];
		    }
            return new string(retval);
        }
    }
}
