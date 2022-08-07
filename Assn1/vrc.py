#!/usr/bin/env python3

class VRC:
    @classmethod
    def generate_vrc(cls, chunks):
        res = ""
        for chunk in chunks:
            if chunk.count("1") % 2 == 0:
                res = res + "0"
            else:
                res = res + "1"
        return res

    @classmethod
    def check_vrc(cls, chunks, vrc):
        i = 0
        for chunk in chunks:
            if chunk == '':
                continue
            if (chunk.count("1") % 2 == 0 and vrc[i] == "0") or (chunk.count("1") % 2 != 0 and vrc[i] == "1"):
                i = i+1
                continue
            else:
                return False
        return True
