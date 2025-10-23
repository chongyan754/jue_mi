from Crypto.Util.number import getPrime
import time


# 生成质数
p = getPrime(2048)
#print(p)
print("质数p生成完成")
q = getPrime(2048)
#print(q)
print("质数q生成完成")

n = p * q
#print(n)
e = 65537
phi = (p - 1) * (q - 1)
d=pow(e, -1, phi)


print("公钥n")
print(n)
#print("服务器端私钥 d =", d)

# 从客户端接收密文
c = int(input("请输入客户端加密的密文c: "))
m = pow(c, d, n)
print("解密后的对称密钥 m ")
print(m)

