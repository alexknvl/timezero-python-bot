<?php
	/**
	 * \author Konovalov Alexander
	 */
	class Encryptor
	{
		private static $replaceTable = array (35,6,4,25,7,8,36,16,20,37,12,31,39,38,21,5,33,15,9,13,29,23,32,22,2,27,1,10,30,24,0,19,26,14,18,34,17,28,11,3);
		
		private static function shr($num, $cnt)
		{
			$ret = $num >> $cnt;
			for($i = 0; $i < $cnt; $i++) $ret &= ~(1 << (31 - $i));
			return $ret;
		}

		private static function rol($num, $cnt)
		{ 
			return (($num << $cnt) | (self::shr($num, 32 - $cnt)));
		}

		public static function encrypt($data, $key)
		{
			$data = substr($data, 0, 1) . substr($key, 0, 10) . substr($data, 1) . substr($key, 10);
			$dataLength8 = strlen($data) * 8;

			$buffer1Length = (($dataLength8 + 64) >> 9 << 4) + 16;
			$buffer1 = array();
			for ($i = 0; $i < $buffer1Length; $i++) 
				$buffer1[$i] = 0;

			for ($i = 0; $i < $dataLength8; $i += 8)
				$buffer1[$i >> 5] = $buffer1[$i >> 5] | ((ord(substr($data, $i >> 3, 1)) & 0xFF) << (24 - ($i & 0x1F)));
			$buffer1[$dataLength8 >> 5] = $buffer1[$dataLength8 >> 5] | 128 << 24 - ($dataLength8 & 0x1F);
			$buffer1[$buffer1Length - 1] = $dataLength8;

			$buffer2 = array();
			for ($i = 0; $i < 80; $i++) 
				$buffer2[$i] = 0;

			$_loc13 = 1732584193;
			$_loc6 = -271733879;
			$_loc8 = -1732584194;
			$_loc7 = 271733878;
			$_loc14 = -1009589776;
			$_loc15 = 0;
			$_loc21 = 0;
			$_loc19 = 0;
			$_loc23 = 0;
			$_loc10 = 0;
			$_loc38 = 0;
			$_loc2 = 0;
			$_loc4 = 0;
			$_loc3 = 0;
			$flag = false;

			for ($i = 0; $i < $buffer1Length; $i+=16)
			{
				$_loc32 = (int)$_loc13;
				$_loc31 = (int)$_loc6;
				$_loc30 = (int)$_loc8;
				$_loc29 = (int)$_loc7;
				$_loc28 = (int)$_loc14;

				for ($k = 0; $k < 80; ++$k)
				{
					if ($k < 16)
					{
						$buffer2[$k] = $buffer1[$i + $k];
					}
					else
					{
						$_loc16 = $buffer2[$k - 3] ^ $buffer2[$k - 8] ^ $buffer2[$k - 14] ^ $buffer2[$k - 16];
						$buffer2[$k] = self::rol($_loc16, 1);
					}

					$_loc20 = (int)self::rol($_loc13, 5);
					$_loc4 = (int)$_loc14;
					$_loc3 = (int)$buffer2[$k];
					$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
					$_loc15 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
					$_loc23 = $k < 20 ? (1518500249) : ($k < 40 ? (1859775393) : ($k < 60 ? (-1894007588) : (-899497514)));
					$_loc4 = (int)$_loc15;
					$_loc3 = (int)$_loc23;
					$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
					$_loc21 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);

					do
					{
						if ($flag)
						{
							if ($k < 20)
							{
								$_loc10 = (int)($_loc6 & $_loc8 | ($_loc6 ^ 0xFFFFFFFF) & $_loc7);
							}
							elseif ($k < 40)
							{
								$_loc10 = (int)($_loc6 ^ $_loc8 ^ $_loc7);
							}
							elseif ($k < 60)
							{
								$_loc10 = (int)($_loc6 & $_loc8 | $_loc6 & $_loc7 | $_loc8 & $_loc7);
							}
							else
							{
								$_loc10 = (int)($_loc6 ^ $_loc8 ^ $_loc7);
							}

							$_loc4 = (int)$_loc20;
							$_loc3 = (int)$_loc10;
							$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
							$_loc19 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
						}
						$flag = !$flag;
					} while ($flag);

					$_loc4 = (int)$_loc19;
					$_loc3 = (int)$_loc21;
					$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
					$_loc22 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
					$_loc14 = (int)$_loc7;
					$_loc7 = (int)$_loc8;
					$_loc8 = (int)self::rol($_loc6, 30);
					$_loc6 = (int)$_loc13;
					$_loc13 = (int)$_loc22;
				}

				$_loc4 = (int)$_loc13;
				$_loc3 = (int)$_loc32;
				$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
				$_loc13 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
				$_loc4 = (int)$_loc6;
				$_loc3 = (int)$_loc31;
				$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
				$_loc6 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
				$_loc4 = (int)$_loc8;
				$_loc3 = (int)$_loc30;
				$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
				$_loc8 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
				$_loc4 = (int)$_loc7;
				$_loc3 = (int)$_loc29;
				$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
				$_loc7 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
				$_loc4 = (int)$_loc14;
				$_loc3 = (int)$_loc28;
				$_loc2 = (int)(($_loc4 & 65535) + ($_loc3 & 65535));
				$_loc14 = (int)(($_loc4 >> 16) + ($_loc3 >> 16) + ($_loc2 >> 16) << 16 | $_loc2 & 65535);
      		}

			$output = array($_loc13, $_loc6, $_loc8, $_loc7, $_loc14);
	    	$retval = array();
			$hexchars = "0123456789ABCDEF";

			for ($i = 0; $i < 20; ++$i)
			{
				$retval[self::$replaceTable[$i*2]] = $hexchars[$output[$i >> 2] >> (3 - $i % 4) * 8 + 4 & 15];
				$retval[self::$replaceTable[$i*2+1]] = $hexchars[$output[$i >> 2] >> (3 - $i % 4) * 8 & 15];
			}
			ksort($retval);
			return join($retval);
		}
	}
?>