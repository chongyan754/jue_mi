import os
import time

e = 65537
n = int(input("请输入服务端提供的公钥:"))

# 生成共享密钥 m (随机数)
aes_key_bytes = os.urandom(32)  # 32字节=256位
m = int.from_bytes(aes_key_bytes, 'big')
print("生成的AES密钥 m 为")
print(m)
print(("妥善保存，不可泄露，后续AES加解密使用"))

# 计算密文
c = pow(m, e, n)
print("加密后的密文 c :")
print(c)

input("把这个玩意复制给我")