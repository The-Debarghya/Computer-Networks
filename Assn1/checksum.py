#!/usr/bin/env python3
class Checksum:

    @classmethod
    def generate_checksum(cls, chunks):
        res = ""
        size = len(chunks[0])
        for chunk in chunks:
            res = bin(int(res, 2)+int(chunk, 2)) if res != "" else chunk
        res = res[2:]
        res = bin(int(res[-size:], 2)+int(res[:-size], 2))
        return ''.join('1' if x == '0' else '0' for x in res[2:])

    @classmethod
    def check_checksum(cls, chunks, checksum):
        res = ""
        size = len(chunks[0])
        for chunk in chunks:
            if chunk == '':
                continue
            res = bin(int(res, 2)+int(chunk, 2)) if res != "" else chunk
        res = res[2:]
        res = bin(int(res[-size:], 2)+int(res[:-size], 2)+int(checksum, 2))
        if res.count("1") == size:
            return True
        else:
            return False
