import random
import string

class Caesar:
    def __init__(self):
        self.codebook = self.generate_codebook()

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
            
            for i in range(len(self.codebook)):
                if letter == self.codebook[i]:
                    newidx = i + shift

                    #if index too big, loop again through the list
                    while newidx > len(self.codebook):
                        newidx =- len(self.codebook)
                    encrypted += self.codebook[newidx]

        return encrypted


    def caesarDecrypt(self, message, shift):
        decrypted=self.caesarEncrypt(message, -shift)
        return decrypted


if __name__ == "__main__":
    codebook = Caesar()
    msg = "Hello Kitty!"
    shift = 3
    encoded = codebook.caesarEncrypt(msg, shift)
    decoded = codebook.caesarDecrypt(encoded, shift)
    print("Origin:", msg)
    print("Encoded:", encoded)
    print("Decoded", decoded)
