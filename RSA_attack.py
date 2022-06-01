from Crypto.Util.number import *
import math

class RSA_small_e:
    def __init__(self,num):
        self.keygen(num)

    def keygen(self,num):
        #generate prime number p,q
        p = getStrongPrime(num)
        q = getStrongPrime(num)
        n=p*q
        
        #calculate LCM
        lm = math.lcm(p-1,q-1)

        #generate key pair e,d
        e = 3
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
    #attack
    def check_m_size(self,m):
        if m**self.pk[0] < self.pk[1]:
            return True
        else:
            return False

    def small_e__attack(self,c):
        #if c is too long,Overflow.Because in function pow ,int to float conversion does not work well.
        m = pow(c,(1/self.pk[0]))
        m = round(m)
        return m


if __name__ == "__main__":
    r = RSA_small_e(1024)
    #plain text
    m = "Hello"
    print("Plain text is : " +m)
    m_byte_to_long = bytes_to_long(m.encode("utf-8"))

    #cipher text
    c = r.enc(m_byte_to_long)
    print("cipher text is :"+str(c))
    
    if r.check_m_size(m_byte_to_long):
        #attack
        attacked_m = r.small_e__attack(c)
        attacked_m = long_to_bytes(attacked_m)
        print("Decrypted text is :" +attacked_m.decode("utf-8"))
    else:
        print("Failed Attack.")
