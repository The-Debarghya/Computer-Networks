#!/usr/bin/env python3
from sympy import Poly

CRCPolynomials = {
    "CRC_1"       : "x+1",
    "CRC_4_ITU"   : "x^4 + x^1 + 1",
    "CRC_5_ITU"   : "x^5 + x^4 + x^2 + 1",
    "CRC_5_USB"   : "x^5 + x^2 + 1",
    "CRC_6_ITU"   : "x^6 + x^1 + 1",
    "CRC_7"       : "x^7 + x^3 + 1",
    "CRC_8_ATM"   : "x^8 + x^2 + x^1 + 1",
    "CRC_8_CCITT" : "x^8 + x^7 + x^3 + x^2 + 1",
    "CRC_8_MAXIM" : "x^8 + x^5 + x^4 + 1",
    "CRC_8"       : "x^8 + x^7 + x^6 + x^4 + X^2 +1",
    "CRC_8_SAE"   : "x^8 + x^4 + x^3 + X^2 +1",
    "CRC_10"      : "x^10 + x^9 + x^5 + x^4 + x^1 + 1",
    "CRC_12"      : "x^12 + x^11 + x^3 + x^2 + x + 1",
    "CRC_15-CAN"  : "x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + 1",
    "CRC-16"      : "x^16 + x^15 + x^2 + 1" 
    
}

def convToBinary(key):
	polynomial = Poly(CRCPolynomials[key])
	binary = bin(polynomial.eval(2))
	return binary[2:]
	
	
