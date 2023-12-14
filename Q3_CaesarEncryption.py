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

    for letter in message:

        #account for the space and punctuations not being changed
        if letter == " " or letter in string.punctuation:
            encrypted += letter
        
        for i in range(len(codebook)):
            if letter == codebook[i]:
                newidx = i + shift

                #if index too big, loop again through the list
                while newidx > len(codebook):
                    newidx =- len(codebook)
                encrypted += codebook[newidx]

    return encrypted


def caesarDecrypt(message, codebook, shift):
    decrypted = ""
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
