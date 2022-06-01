from Crypto.Util.number import *
from Crypto.Hash import SHA3_512
from random import randint

class Cramour_Shoup:
    def __init__(self,num):
        self.keygen(num)

    def keygen(self,num):
        #generate PrimeNumber p
        self.p = getPrime(num)

        #generate g,h∈G^2
        g = randint(0,self.p-1)
        h = randint(0,self.p-1)

        #generate (x00,x01,x10,x11,x20,x21)∈Z_{p}^6
        x00 = randint(0,self.p-1)
        x01 = randint(0,self.p-1)
        x10 = randint(0,self.p-1)
        x11 = randint(0,self.p-1)
        x20 = randint(0,self.p-1)
        x21 = randint(0,self.p-1)

        #calculate y_{i}
        y0 = (pow(g,x00,self.p))*(pow(h,x01,self.p))
        y1 = (pow(g,x10,self.p))*(pow(h,x11,self.p))
        y2 = (pow(g,x20,self.p))*(pow(h,x21,self.p))

        #key
        self.pk = (y0,y1,y2,g,h)
        self.sk = (x00,x01,x10,x11,x20,x21)

    
    def enc(self,m):
        r = randint(0,self.p-1)

        #calculate cipher123
        c1 = pow(self.pk[3],r,self.p)
        c2 = pow(self.pk[4],r,self.p)
        c3 = m*(pow(self.pk[0],r,self.p))%self.p
        #calculate hash
        c1_b = format(c1,'b')
        c2_b = format(c2,'b')
        c3_b = format(c3,'b')
        c123_b = c1_b + c2_b + c3_b
        hs = SHA3_512.new(bytearray(c123_b,"utf-8"))
        hs = int(hs.hexdigest(),16)
                
        #calculate cipher4
        c4 = pow((self.pk[1]*pow(self.pk[2],hs,self.p))%self.p,r,self.p)

        return (c1,c2,c3,c4)
    
    def dec(self,c):
        #hash
        c1_b = format(c[0],'b')
        c2_b = format(c[1],'b')
        c3_b = format(c[2],'b')
        c123_b = c1_b + c2_b + c3_b
        hs = SHA3_512.new(bytearray(c123_b,"utf-8"))
        hs = int(hs.hexdigest(),16)


        #calculate ck_num = {(c1^x10)(c2^x11)}{(c1^x20)(c2^x21)}^H(c1,c2,c3)
        ck_num1 = (pow(c[0],self.sk[2],self.p)*pow(c[1],self.sk[3],self.p))%self.p
        ck_num2 = (pow(c[0],self.sk[4],self.p)*pow(c[1],self.sk[5],self.p))%self.p
        ck_num3 = pow(ck_num2,hs,self.p)
        ck_num = (ck_num1*ck_num3 )%self.p

        #check c4 == ck_num
        if(c[3] == ck_num):
            m1= c[2]*pow(c[0],-self.sk[0],self.p)%self.p
            m= m1 * pow(c[1],-self.sk[1],self.p)%self.p
            return m
        else:
            print("error")




if __name__ == '__main__':
    k = Cramour_Shoup(1024)
    #message
    m="Hello_IPA!!!"
    print("Plain text is :" +m)
    m_byte_to_long = bytes_to_long(m.encode("utf-8"))
    #enc
    m_enc = k.enc(m_byte_to_long)
    print("Cipher text is :" ,str(m_enc[0]),str(m_enc[1]),str(m_enc[2]),str(m_enc[3]))
    #dec
    m_dec = k.dec(m_enc)
    m_long_to_byte = long_to_bytes(m_dec)
    print("Decrypted cipher text is :"+m_long_to_byte.decode("utf-8"))






    


