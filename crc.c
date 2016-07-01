/* 
  Copyright (C) 2016 Enrico Rossi
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published
  by the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.
 
  You should have received a copy of the GNU Lesser General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

/** @fn void CRC_calcCrc8(u16 *crcReg, u16 poly, u16 u8Data)
* @ Standard CRC calculation on an 8-bit piece of data. To make it
* CCITT-16, use poly=0x1021 and an initial crcReg=0xFFFF.
*
* Note: This function allows one to call it repeatedly to continue
*
calculating a CRC. Thus, the first time it's called, it
*
should have an initial crcReg of 0xFFFF, after which it
*
can be called with its own result.
*
* @param *crcRegPointer to current CRC register.
* @param poly Polynomial to apply.
* @param u8Datau8 data to perform CRC on.
* @return None.
*/
void CRC_calcCrc8(uint16_t *crcReg, uint16_t poly, uint16_t u8Data)
{
	uint16_t i, xorFlag, bit;
	uint16_t dcdBitMask = 0x80;

	for(i=0; i<8; i++) {
		// Get the carry bit. This determines if the polynomial should be
		// xor'd with the CRC register.
		xorFlag = *crcReg & 0x8000;
		// Shift the bits over by one.
		*crcReg <<= 1;
		// Shift in the next bit in the data byte
		bit = ((u8Data & dcdBitMask) == dcdBitMask);
		*crcReg |= bit;

		// XOR the polynomial
		if(xorFlag)
			*crcReg = *crcReg ^ poly;

		// Shift over the dcd mask
		dcdBitMask >>= 1;
	}
}

uint16_t crc_xmodem_update (uint16_t crc, uint8_t data)
{
	int i;

	crc = crc ^ ((uint16_t)data << 8);

	for (i=0; i<8; i++)
	{
		if (crc & 0x8000)
			crc = (crc << 1) ^ 0x1021;
		else
			crc <<= 1;
	}

	return crc;
}

int main(void)
{
	char *rfid;
	char *substr;
	unsigned int i, byte[6];
	uint16_t crc;

	rfid = malloc(20);
	substr = malloc(3);
	strcpy(rfid, "0003");
	printf("-> %s \n", rfid);

	for (i=0; i<2; i++) {
		strncpy(substr, rfid + (i*2), 2);
		byte[i] = strtoul(substr, 0, 16);
		printf("byte[%d]: %2x\n", i, byte[i]);
	}

	crc = crc_xmodem_update(0xffff, byte[0]);
	crc = crc_xmodem_update(crc, byte[1]);
	printf("crc: %4x\n", crc);

	crc = 0xffff;
	CRC_calcCrc8(&crc, 0x1021, byte[0]);
	CRC_calcCrc8(&crc, 0x1021, byte[1]);
	printf("crc: %4x\n", crc);

	free(substr);
	free(rfid);
}
