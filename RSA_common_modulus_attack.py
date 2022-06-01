from Crypto.Util.number import *
from math import lcm,gcd
class RSA_common_modulus:
    def __init__(self,num):
        self.keygen(num)

    def keygen(self,num):
        #generate prime number p,q
        p = getStrongPrime(num)
        q = getStrongPrime(num)
        n=p*q
        print(n)
        
        #calculate LCM
        lm = lcm(p-1,q-1)

        #generate key pair e,d
        e = getPrime(num)
        s,d = self.ex_Euclid_gen_d(lm,e)

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
        return  x0,y0

    def enc(self,m):
        
        c = pow(m,self.pk[0],self.pk[1])
        return c
    
    def dec(self,c):
        m = pow(c,self.sk[0],self.sk[1])
        return m

    #change e (same n)
    def change_e(self,num):
        flag = True
        while flag:
            e = getPrime(num)
            if e != self.pk[0]:
                flag = False
            n = self.pk[1]
            self.pk = (e,n)




if __name__ == '__main__':
    #plain text
    m = "Hello_IPA!"
    print("Plain text is :" +m)
    m_byte_to_long = bytes_to_long(m.encode("utf-8"))

    #encryption gcd(e1,e2) == 1
    flag = True
    while flag:
        r1 = RSA_common_modulus(1024)
        m_enc1 = r1.enc(m_byte_to_long)
        e1 = r1.pk[0]
        r1.change_e(1024)
        m_enc2 = r1.enc(m_byte_to_long)
        e2 = r1.pk[0]
        if gcd(e1,e2) != 1:
            continue
        else:
            flag = False
            
     
    print("Cipher1 is "+str(m_enc1))
    print("Cipher2 is "+str(m_enc2))
    print("e1 is : "+str(e1))
    print("e2 is : " +str(e2))

    #Ex Euclid
    x,y = r1.ex_Euclid_gen_d(e1,e2)
    #common modulus attack
    m_attack1 = pow(m_enc1,x,r1.pk[1])
    m_attack2 = pow(m_enc2,y,r1.pk[1])
    m_attack = (m_attack1 * m_attack2) %r1.pk[1]

    #decryption
    print("Attacked decypted text is "+ long_to_bytes(m_attack).decode("utf-8"))
