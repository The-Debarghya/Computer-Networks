#!/usr/bin/env python3

import string
import random
import re

n = 7 * (32 * 13)

res = ''.join(random.choices(re.sub(r'\s+', '', string.printable), k=n))
file = open("data.txt", "w")
file.write(res)
file.close()
