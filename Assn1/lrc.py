#!/usr/bin/env python3

class LRC:

    @classmethod
    def generate_lrc(cls, chunks):
        res = ""
        for i in range(len(chunks[0])):
            count = 0
            for chunk in chunks:
                if chunk[i] == '1':
                    count = count+1
            if count % 2 == 0:
                res = res+"0"
            else:
                res = res+"1"
        return res

    @classmethod
    def check_lrc(cls, chunks, lrc):
        for i in range(len(chunks[0])):
            count = 0
            for chunk in chunks:
                if chunk == '':
                    continue
                if chunk[i] == '1':
                    count = count+1
            if (count % 2 == 0 and lrc[i] == '0') or (count % 2 != 0 and lrc[i] == '1'):
                continue
            else:
                return False
        return True

