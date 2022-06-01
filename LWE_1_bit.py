import numpy as np

class LWE:
    def __init__(self):
        #dimention
        self.n = 230
        #prime num <10000
        self.q = 4093
        #base matrix (n×n)
        self.A = np.random.randint(1,self.q-1,(self.n,self.n)) 
        #alpha
        self.a = 8.0
        

        self.keygen()
    
    def D_gaussian_(self,a,num):
        sigma = a/np.sqrt(2*np.pi)
        #gaussian μ=0,sigma = a/sqrt(2pi)
        rg = np.random.normal(0,sigma,num)
        return np.rint(rg)
    
    def keygen(self):
        s = np.random.randint(1,self.q-1,(self.n,1))
        #lattice point
        G = np.dot(self.A,s) %  self.q
        #error
        e = self.D_gaussian_(self.a,(self.n,1))
        #lattice point with error
        T = (G + e )% self.q
        #publickey and secretkey
        self.pk = T
        self.sk = (s,e)
    
    def enc(self,m):
        r = self.D_gaussian_(self.a,(1,self.n))
        c1 = np.dot(r,self.A) % self.q

        #check m == 1
        if m ==1:
            M = (self.q + 1)/2
        elif m == 0:
            M = 0
        else:
            raise Exception("error!")
        
        c2 = (np.dot(r,self.pk) - M )% self.q

        return (c1,c2)
    
    def dec(self,c):
        flag = (np.dot(c[0],self.sk[0]) -c[1]) % self.q
        
        if (-(self.q + 1)/2 < flag and flag < -(self.q + 1)/4) or ((self.q + 1)/4 < flag < (self.q + 1)/2):
            return 1
        else:
            return 0
    


if __name__ == '__main__':
    L = LWE()
    m = 0
    c = L.enc(m)
    m_dec = L.dec(c)
    print(m)
    print(m_dec)