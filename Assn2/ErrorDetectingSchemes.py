#!/usr/bin/env python3

class CRC:
    @classmethod
    def xor(cls, a, b):
        x = ""
        for i in range(1, len(b)):
            if a[i] == b[i]:
                x += "0"
            else:
                x += "1"
        return x

    @classmethod
    def binaryDivision(cls, divident, divisor):
        m = len(divisor)
        n = len(divident)
        temp = divident[0: m]

        while m < n:
            if temp[0] == '1':
                temp = cls.xor(divisor, temp) + divident[m]
            else:
                temp = cls.xor("0"*len(divisor), temp) + divident[m]
            m += 1
        if temp[0] == '1':
            temp = cls.xor(divisor, temp)
        else:
            temp = cls.xor("0"*len(divisor), temp)
        return temp

    @classmethod
    def generateCRC(cls, data, poly):
        k = len(poly)
        ndata = data + "0"*(k - 1)
        rem = cls.binaryDivision(ndata, poly)
        crc = data + rem
        return crc

    @classmethod
    def checkCRC(cls, data, poly):
        rem = cls.binaryDivision(data, poly)
        if rem == "0"*len(rem):
            return False
        return True
