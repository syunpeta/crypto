from random import randint
from Crypto.Util.number import *
from math import lcm
import gmpy2
class RSA_CCA:
    def __init__(self,num):
        self.keygen(num)

    def keygen(self,num):
        #generate prime number p,q
        p = getStrongPrime(num)
        q = getStrongPrime(num)
        n=p*q
        
        #calculate LCM
        lm = lcm(p-1,q-1)

        #generate key pair e,d
        e = getPrime(num)
        d = self.ex_Euclid_gen_d(lm,e)

        #publickey secretkey
        self.pk = (e,n)
        self.sk = (d,n)

    #Extended Euclid (lm x + e y = 1 )
    def ex_Euclid_gen_d(self,a,b):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while b != 0:
            q, a, b = a // b, b, a % b
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return  y0

    def enc(self,m):
        
        c = pow(m,self.pk[0],self.pk[1])
        return c
    
    def dec(self,c):
        m = pow(c,self.sk[0],self.sk[1])
        return m
    def CCA_attack(self,c):
        r = randint(2,100)
        c_mul = (c*pow(r,self.pk[0],self.pk[1]))%self.pk[1]
        m_mul = self.dec(c_mul)
        m = (m_mul * gmpy2.invert(r,self.pk[1]))%self.pk[1]
        return m


if __name__ == '__main__':
    r = RSA_CCA(1024)
    #plain text
    m = "Hello_IPA!"
    print("Plain text is :" +m)
    m_byte_to_long = bytes_to_long(m.encode("utf-8"))

    #encryption
    m_enc = r.enc(m_byte_to_long)
    print("Cipher is "+str(m_enc))

    #decryption
    m_dec = r.dec(m_enc)
    print("Decrypted text is "+ long_to_bytes(m_dec).decode("utf-8"))

    #attack CCA2
    m_attack = r.CCA_attack(m_enc)
    print("Attacked text is :" + long_to_bytes(m_attack).decode("utf-8"))


