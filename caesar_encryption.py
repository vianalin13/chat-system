import random
import string

class Caesar:
    def __init__(self):
        self.codebook = self.generate_codebook()
        self.shift = random.randint(1,51)

    def generate_codebook(self):
        random.seed("Caesar")

        codebook = []
        for e in string.ascii_letters:
            codebook.append(e)
        random.shuffle(codebook)

        return codebook
        ## end of the codebook generation


    def caesarEncrypt(self, message, shift):
        encrypted = ""

        for letter in message:
            #account for the space and punctuations not being changed
            if letter == " " or letter in string.punctuation:
                encrypted += letter
            
            else: 
                for i in range(len(self.codebook)):
                    if letter == self.codebook[i]:
                        newidx = (i + shift) % len(self.codebook)
                        encrypted += self.codebook[newidx]

        return encrypted
    
    def caesarDecrypt(self, message, shift):
        decrypted=self.caesarEncrypt(message, -shift)
        return decrypted
