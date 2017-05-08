#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
Perform encrypt or decrypt text
"""
from utils import genkey
from utils import matrixoperation
from common import log
from numpy.linalg import inv
import copy
LOG = log.setup_log(__name__)


class Crypto(object):
    def __init__(self, text, key):
        self.text = text
        self.key = key
        self.matrix = matrixoperation.MatrixOperations()
        self.sub_keys = self.get_sub_keys()

    def convert_string_to_matrix(self, text):
        """
        Input: string with 16 charaters
        Output: Matrix 4*4
        """
        text = [ord(x) for x in text]
        return [[text[i + 4*j] for i in range(4)] for j in range(4)]

    def convert_matrix_to_string(self, matrix):
        """
        Input: matrix 4*4
        Output: String with 16 charaters
        """
        text = ''
        for row in range(4):
            for col in range(4):
                text += chr(int(matrix[row][col]))
        return text

    def get_sub_keys(self):
        _gen = genkey.GenerateKeys(K=self.key)
        sub_keys = _gen.generate_sub_keys()
        if not sub_keys:
            LOG.error('The master key has length %r, expected 32',
                      len(self.key))
            exit(0)
        else:
            return sub_keys

    def encrypt(self):
        """
        perform encrypt input string using input key
        """
        C = []
        for count in range(len(self.text)/16+1):
            sub_p = ''
            if (count+1)*16 < len(self.text):
                sub_p = self.text[count*16:(count+1)*16]
            else:
                sub_p = self.text[count*16:].ljust(16)
            P = self.convert_string_to_matrix(sub_p)
            for i in range(len(self.sub_keys)):
                sub_key = self.matrix.convert_matrix_bin_to_decimal(
                    self.sub_keys[i]
                    )
                P1 = self.matrix.multiple(matrixA=sub_key,
                                          matrixB=P,
                                          modulo=127)
                P = P1
            P = self.matrix.convert_matrix_demcimal_to_bin(P)
            for i in range(len(self.sub_keys)):
                P2 = self.matrix.stir(P)
                sub_key = self.sub_keys[i]
                P3 = self.matrix.xor(matrixA=sub_key,
                                     matrixB=P2)
                P = P3
            C.append(P)
        return C

    def decrypt(self):
        """
        perform decrypt input string with key
        """
        P = ''
        for C in self.text:
            for i in reversed(range(len(self.sub_keys))):
                sub_key = copy.deepcopy(self.sub_keys[i])
                C1 = self.matrix.xor(matrixA=sub_key,
                                     matrixB=C)
                C2 = self.matrix.stir(C1)
                C = C2
            C = self.matrix.convert_matrix_bin_to_decimal(C)
            for i in reversed(range(len(self.sub_keys))):
                # start calculate K^-1
                sub_key = copy.deepcopy(self.sub_keys[i])
                Km = self.matrix.convert_matrix_bin_to_decimal(sub_key)
                inv_Km = self.matrix.inverse_matrix_with_modulo(A=Km, p=127)
                # End calculate K^-1
                C3 = self.matrix.multiple(matrixA=inv_Km,
                                          matrixB=C,
                                          modulo=127)
                C = C3
            plain = self.convert_matrix_to_string(matrix=C)
            P += plain
        return P


if __name__ == '__main__':
    key = '778b9e660d5b8c9d7247a1194b3fsthb'
    plain_text = 'saphi saphi saphi'
    print "======================"
    print "[-] Master key ", key
    print "**********************"
    print "[-] Plain text ", plain_text

    c = Crypto(key=key,
               text=plain_text)
    C = c.encrypt()
    print C
    print "+++++++++++++++++++++"
    print "[+] Encrypted to binary ", C
    p = Crypto(key=key,
               text=C)
    P = p.decrypt()
    print "--------------------"
    print "[+] Decrypted: ", P
