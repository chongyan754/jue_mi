import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding


def int_to_bytes(n: int) -> bytes:
    """将整数转换为 16/24/32 字节的 AES 密钥"""
    # 计算整数占用的字节数
    byte_length=(n.bit_length()+7)//8

    # 检查是否有效 AES 密钥长度
    if byte_length not in {16,24,32}:
        # 自动填充到最近的有效长度
        target_length=16 if byte_length<=16 else 24 if byte_length<=24 else 32
        n_bytes=n.to_bytes(target_length,'big')
        print(f"警告: 密钥长度自动调整为 {len(n_bytes)} 字节 ({len(n_bytes)*8} 位)")
        return n_bytes

    return n.to_bytes(byte_length,'big')


def aes_encrypt():
    # 输入数字密钥 (例如 RSA 解密得到的密钥)
    key_int=int(input("请输入密钥数字: ").strip())
    key=int_to_bytes(key_int)

    while True:
        plaintext=input("请输入明文: ").encode('utf-8')

        # 生成随机 IV (初始向量)
        iv=os.urandom(16)

        # 创建加密器 (使用 PKCS7 填充)
        padder=padding.PKCS7(128).padder()
        padded_data=padder.update(plaintext)+padder.finalize()

        # 执行 AES-CBC 加密
        cipher=Cipher(algorithms.AES(key),modes.CBC(iv))
        encryptor=cipher.encryptor()
        ciphertext=encryptor.update(padded_data)+encryptor.finalize()

        # 组合 IV + 密文 并 Base64 编码
        encrypted_data=iv+ciphertext
        result=base64.b64encode(encrypted_data).decode('utf-8')

        print(f"{result}")
        #print(f"密钥长度: {len(key)*8} 位")


会=0
if __name__=="__main__":
    aes_encrypt()