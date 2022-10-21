#!/usr/bin/env python3
def get_checksum(segment_data: str) -> str:
    total = 0
    chunks = [segment_data[i:i+32] for i in range(0, len(segment_data), 32)]
    for chunk in chunks:
        total += int(chunk, 2)
        if total >= 4294967295:
            total -= 4294967295
    checksum = 4294967295 - total
    return '{0:032b}'.format(checksum)

def validate_checksum(segment_data: str) -> bool:
    total = 0
    chunks = [segment_data[i:i+32] for i in range(0, len(segment_data), 32)]
    for chunk in chunks:
        total += int(chunk, 2)
        if total >= 4294967295:
            total -= 4294967295
    return True if total == 0 else False 