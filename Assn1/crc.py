#!/usr/bin/env python3

class CRC:
    @classmethod
    def xor(cls, a, b):
        result = []
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
        return ''.join(result)

    @classmethod
    def mod2div(cls, dividend, divisor):
        pick = len(divisor)
        tmp = dividend[0: pick]
        while pick < len(dividend):
            if tmp[0] == '1':
                tmp = cls.xor(divisor, tmp) + dividend[pick]
            else:
                tmp = cls.xor('0'*pick, tmp) + dividend[pick]
            pick += 1

        if tmp[0] == '1':
            tmp = cls.xor(divisor, tmp)
        else:
            tmp = cls.xor('0'*pick, tmp)

        checkword = tmp
        return checkword

    @classmethod
    def encodeData(cls, chunks, key):
        l_key = len(key)
        enc_chunks = []
        for data in chunks:
            appended_data = data + '0'*(l_key-1)
            remainder = cls.mod2div(appended_data, key)
            codeword = data + remainder
            enc_chunks.append(codeword)
        return enc_chunks

    @classmethod
    def checkRemainder(cls, chunks, key):
        l_key = len(key)
        for data in chunks:
            appended_data = data + '0'*(l_key-1)
            remainder = cls.mod2div(appended_data, key)
            if remainder.count('1') != 0:
                return False

        return True
