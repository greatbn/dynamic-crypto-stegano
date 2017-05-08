#!/usr/bin/python
"""
Author: Sa Phi saphi070@gmail.com
Perform embed and retriev binary to/from image
"""
import sys
import re

from common import log
LOG = log.setup_log(__name__)


class Stegano(object):
    def __init__(self, image):
        self.image = image

    def embed(self, binary):
        """
        Embed function
        """
        try:
            with open(self.image, 'rb') as image:
                f = image.read()
                b_array = bytearray(f)
        except IOError:
            print '[-] Cannot open image ', self.image
        if len(b_array) < (3300 + len(binary)*8):
            LOG.error('The image is too small to process')
            sys.exit(0)
        # embed length of cipher binary
        # convert length to string -> ascii -> binary
        # example: 120 => 49 50 48 => 00110001 00110010 00110000
        length = str(len(binary))
        len_in_bin = ''
        for i in length:
            len_in_bin += format(ord(i), '08b')
        for i in range(0, len(len_in_bin), 2):
            origin = format(b_array[3001+i/2], '08b')
            origin = origin[:6] + len_in_bin[i] + origin[7:]
            origin = origin[:7] + len_in_bin[i+1] + origin[8:]
            b_array[3001+i/2] = int(origin, 2)

        # embed cipher text
        next_index1 = 6
        next_index2 = 7
        for i in range(0, len(binary), 2):
            origin = format(b_array[3301 + i/2], '08b')
            origin = origin[:next_index1] + str(binary[i]
                                                ) + origin[next_index1+1:]
            origin = origin[:next_index2] + str(binary[i+1]
                                                ) + origin[next_index2+1:]
            b_array[3301+i/2] = int(origin, 2)
            if binary[i] == 0 and binary[i+1] == 0:
                next_index1 = 6
                next_index2 = 7
            elif binary[i] == 0 and binary[i+1] == 1:
                next_index1 = 7
                next_index2 = 6
            elif binary[i] == 1 and binary[i+1] == 0:
                next_index1 = 5
                next_index2 = 6
            elif binary[i] == 1 and binary[i+1] == 1:
                next_index1 = 6
                next_index2 = 5
        return b_array

    def retriev(self):
        """
        Retriev function
        """
        try:
            with open(self.image, 'rb') as image:
                f = image.read()
                b_array = bytearray(f)
        except IOError:
            print "[-] Cannot open image ", self.image
        # Retriev length of embedded message
        length = ''
        len_in_dec = ''
        for i in range(300):
            embed_byte = format(b_array[3001+i], '08b')
            length += embed_byte[6]
            length += embed_byte[7]
            if len(length) == 8:
                len_in_dec += chr(int(length, 2))
                length = ''

        length = re.findall('\d+', len_in_dec)
        length = int(length[0])
        # Retriev message
        next_index1 = 6
        next_index2 = 7
        # binary
        binary = []
        for i in range(0, length, 2):
            embed_byte = format(b_array[3301+i/2], '08b')
            bin_1 = int(embed_byte[next_index1])
            bin_2 = int(embed_byte[next_index2])
            binary.append(bin_1)
            binary.append(bin_2)
            if bin_1 == 1 and bin_2 == 1:
                next_index1 = 6
                next_index2 = 5
            elif bin_1 == 1 and bin_2 == 0:
                next_index1 = 5
                next_index2 = 6
            elif bin_1 == 0 and bin_2 == 1:
                next_index1 = 7
                next_index2 = 6
            elif bin_1 == 0 and bin_2 == 0:
                next_index1 = 6
                next_index2 = 7
        return binary


def main():
    print "Embed binary in picture"
    print "+++++++++++++++++++++++"
    s = Stegano('before.png')
    binary = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]
    print "Perform embed list binary {0} on image {1}".format(binary,
                                                              "before.png")
    b = s.embed(binary=binary)
    print "======================="
    print "Write result in image after.png"
    with open('after.png', 'wb') as f:
        f.write(bytearray(b))
    print "***********************"
    print "Perform retriev binary in image after.png"
    s = Stegano('after.png')
    b = s.retriev()
    print "Result: ", b


if __name__ == '__main__':
    main()
