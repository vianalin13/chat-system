#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:56:01 2021

@author: bing
"""

import random
import string



def caesarEncrypt(message, codebook, shift):
    '''
    - you can compute the index of a character, or,
    - you can convert the codebook into a dictionary
    '''
    
    encrypted = ""
    e=[]

    for i in range(len(message)):
        for k in range(len(codebook)):
            if message[i]==codebook[k]:
                e.append(k)
    for i in range(len(message)):
        if not message[i].isalpha():
            e.insert(i,message[i])

    s=len(codebook)-shift-1
    for i in e:
        if str(i).isdigit():
            if i>s:
                encrypted+=codebook[i-len(codebook)-1+shift]
            else:
                encrypted+=codebook[i+shift]
        else:
            encrypted+=i
    
    return encrypted


def caesarDecrypt(message, codebook, shift):
    decrypted = ""
    ##put your code here
    decrypted=caesarEncrypt(message, codebook, -shift)
    
    
    return decrypted


if __name__ == "__main__":
    ##The following several lines generate the codebook
    ##Please don't change it
    random.seed("Caesar")
    
    codebook = []
    for e in string.ascii_letters:
        codebook.append(e)
        
    random.shuffle(codebook)
    print("Your codebook:")
    print(codebook)
    ## end of the codebook generation
    
    m = "Hello Kitty!"
    shift = 3
    encoded = caesarEncrypt(m, codebook, shift)
    decoded = caesarDecrypt(encoded, codebook, shift)
    print("Origin:", m)
    print("Encoded:", encoded)
    print("Decoded", decoded)
