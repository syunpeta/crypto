import numpy as np
import random

class NTRU:
    def __init__(self,p,q,N,dg,df,d):
        
        self.m =self.create_random_message(N,p)
        self.keygen(p,q,N,dg,df)

    def keygen(self,p,q,N,dg,df):
        while True:
            f = self.random_poly(N,df,df-1)
            print("polynomial f is :\n",f)
            flag_fp ,Fq = self.inverse(f%q,q)
            flag_fq,Fp = self.inverse(f%p,p)
            if flag_fp == flag_fq:
                break
        g = self.random_poly(N,dg,dg)
        self.pk= self.conv_mult(Fq,g)%q
        self.sk = f
        self.Fp = Fp
    
    def enc(self,m,d,N,p,q):
        phi = self.random_poly(N,d,d)
        e = (p*(self.conv_mult(phi,self.pk)) + m)%q
        return e
    
    def dec(self,e,p,q):
        a = self.conv_mult(self.sk,e)%q
        a = self.centerlift(a,q)

        dec_e = self.conv_mult(self.Fp,a)%p
        dec_e = self.centerlift(dec_e,p)
        return dec_e        

    #畳み込み積
    def conv_mult(self,a,b): 
        N = a.shape[0]
        if N != b.shape[0]:
            raise Exception('size unmatch')
        conv = np.zeros(N)
        for i in range(N):
            for j in range(N):
                conv[(i+j)%N] += a[i]*b[j]
        return conv

    # ユークリッドの互除法でF_p上のx,yのgcd(x,y)とux+vy=gcd (mod p)なるu,vを返す
    def euclid(self,x,y,p):# p is the order of F_p, x > y
        if x <= y:
            swap_flag = True
            x,y = y,x
        else:
            swap_flag = False
        if y==0:
            return x,1,0
        q,r = x//y, x%y
        gcd,u,v = self.euclid(y,r,p)
        if swap_flag:
            return gcd,(u-q*v)%p,v
        return gcd,v,(u-q*v)%p

    # 有限体F_p上でのaの逆元を計算
    def inv_in_finite_field(self,a,p):
        if a >= p:
            raise Exception(f'First arg should be less than second one: {a} >= {p}')
        gcd,a_inv,_ = self.euclid(a,p,p)
        return a_inv

    # a(x)の次数を計算
    def deg(self,a):
        n = a.shape[0]
        for i in range(n-1,-1,-1):
            if a[i]!=0:
                return i
        return -1*np.inf

    # R_p での a(x) = q(x)b(x)+r(x)なるq,rを計算
    def div(self,a,b,p): # a is dividend, b is divisor
        deg_a,deg_b = self.deg(a),self.deg(b)
        if np.isinf(deg_a): return np.zeros(a.shape[0]),np.zeros(a.shape[0])
        if np.isinf(deg_b): raise Exception('Divisor equals 0')
        q = np.zeros(a.shape[0])
        r = a.copy()
        b_head_inv = self.inv_in_finite_field(b[deg_b],p)
        for i in range(deg_a,deg_b-1,-1):
            partial_q = (r[i]*b_head_inv)%p
            q[i-deg_b] = partial_q
            #if r[i] < 0: partial_q -= p
            r[i-deg_b:i+1] = (r[i-deg_b:i+1]-partial_q*b[:deg_b+1]).copy()
        return q,r%p

    #拡張ユークリッド法でf(x)とg(x)のR_pでの最大公約元を計算f(x)u +g(x)v = 1 (mod p)
    def extended_euclid(self,f,g,p):
        if np.isinf(self.deg(g)): # g=0 -> f= gcd(f_init,g_init)
            u = np.zeros(f.shape[0])
            u[0] = 1
            v = np.zeros(f.shape[0])
            return f,u,v
        q,r = self.div(f,g,p)
        gcd,u,v = self.extended_euclid(g,r,p)
        return gcd,v,(u-self.conv_mult(q,v))%p

    #R_p でのf(x)の逆元f^{-1}(x)を計算
    def inverse(self,f,p):
        f = f.copy()%p
        N = f.shape[0]
        print(N)
        deg_f = self.deg(f)
        if np.isinf(deg_f):return False,None
        f_head = f[deg_f]
        q = self.inv_in_finite_field(f_head,p)
        if deg_f==0: return True,np.concatenate(([q],np.zeros(N-1)))
        deg_diff = N-deg_f
        XN_1 = np.zeros(N)
        XN_1[0] = p-1
        XN_1[deg_diff:] = (XN_1[deg_diff:]-q*f[:deg_f])%p
        gcd,u,v = self.extended_euclid(XN_1,f,p)
        if gcd[0]!=0 and not (gcd[1:].any()):
            gcd_inv = self.inv_in_finite_field(gcd[0],p)
            q_X_diff = np.zeros(N)
            q_X_diff[deg_diff] = q  
            return True, (gcd_inv*(v-self.conv_mult(q_X_diff,u)))%p
        else:
            return False,None

    # ランダムにメッセージを作る
    def create_random_message(self,N,p):
        np.random.seed(3)
        m = np.random.randint(0,p,N)
        return m
        
    #L(d1,d2)の空間からランダムな多項式を返す(fは1×nの係数行列)
    def random_poly(self,N,d1,d2):
        f = np.zeros((N),int)
        #d1個の要素が1になる場所の集合
        groupN=list(range(N))
        group_d1 =  random.sample(groupN,d1)
        #d2個の要素が-1になる場所の集合
        for i in group_d1:
            groupN.remove(i)
        group_d2 = random.sample(groupN,d2)
        #fをd1個1,d2個-1の要素を持つ1×n行列としてreturn
        for index in group_d1:
            f[index] = 1
        for index in group_d2:
            f[index] = -1

        return f
    
    #center lift
    def centerlift(self,f,p):
        p_half = p/2
        degf = self.deg(f)
        for i in range(degf):
            if f[i] >p_half:
                f[i] = f[i] - p
            else:
                continue
        return f    
    
    
if __name__ == '__main__':
    p,q,N = 2 ,101,256
    dg,df,d = 35,35, 22
    Cpt = NTRU(p,q,N,dg,df,d)
    m = Cpt.m
    e = Cpt.enc(m,d,N,p,q)
    dec_e = Cpt.dec(e,p,q)

    flag = True
    for i in range(len(m)):
        if m[i] != dec_e[i]:
            flag = False
    print(flag)
    

# reference
#https://qiita.com/shugar/items/deb54b987f4151626417#%E8%A3%9C%E8%B6%B3
    




