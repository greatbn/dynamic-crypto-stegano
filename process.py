#!/usr/bin/python
"""
Author: Nguyen Quoc Trung
"""
import math

from crypto import Crypto

from stegano import Stegano

class DynamicStegProcess(object):

    def start_embed(self, message, key, source_image, dest_image):
        """
        Starting embed
        """
        s = Stegano(source_image)
        binary = []
        c = Crypto(key=key,
                   text=message)
        C = c.encrypt()
        # Change binary in C to bits in binary
        [[[[binary.append(int(l)) for l in k]for k in j]for j in i]for i in C]
        b = s.embed(binary=binary)
        # print "======================="
        # print "Write result in image after.png"
        try:
            with open(dest_image, 'wb') as f:
                f.write(bytearray(b))
            print "[-] Saved image to ", dest_image
        except Exception as e:
            print "[-] Cannot save image ", e

    def start_retriev(self, key, image_retriev):
        s = Stegano(image_retriev)
        b = s.retriev()
        C = []
        LIST_BINARY = []
        # Change bits to binary
        for i in range(0, len(b), 8):
            exp = 7   # exp: 7 -> 1
            sum = 0   # sum is decimal of 8 bit sequent
            for j in b[0+i:8+i]:
                sum = j * math.pow(2, exp) + sum
                exp = exp-1
            binary = format(int(sum), '08b')
            LIST_BINARY.append(binary)
        rows = []
        for i in range(len(LIST_BINARY)/4):
            LIST_SPLIT = []
            for j in LIST_BINARY[i*4:(i+1)*4]:
                LIST_SPLIT.append(j)
            rows.append(LIST_SPLIT)
            if (i+1) % 4 == 0:
                C.append(rows)
                rows = []
        p = Crypto(key=key,
                   text=C)
        P = p.decrypt()
        print "[+] Hidden message is: ", P


if __name__ == '__main__':
    pass
