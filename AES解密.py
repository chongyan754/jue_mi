import base64
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding


def int_to_bytes(n: int) -> bytes:
    """将整数转换为 16/24/32 字节的 AES 密钥"""
    byte_length=(n.bit_length()+7)//8
    if byte_length not in {16,24,32}:
        target_length=16 if byte_length<=16 else 24 if byte_length<=24 else 32
        n_bytes=n.to_bytes(target_length,'big')
        print(f"警告: 密钥长度自动调整为 {len(n_bytes)} 字节 ({len(n_bytes)*8} 位)")
        return n_bytes
    return n.to_bytes(byte_length,'big')


def aes_decrypt():
    # 输入数字密钥 (必须与加密时相同)
    key_int=int(input("请输入密钥数字:").strip())
    key=int_to_bytes(key_int)

    while True:
        encrypted_b64=input("请输入密文:").strip()
        encrypted_data=base64.b64decode(encrypted_b64)

        # 分离 IV 和密文
        iv=encrypted_data[:16]
        ciphertext=encrypted_data[16:]

        # 创建解密器
        cipher=Cipher(algorithms.AES(key),modes.CBC(iv))
        decryptor=cipher.decryptor()

        # 执行解密
        padded_plaintext=decryptor.update(ciphertext)+decryptor.finalize()

        # 移除 PKCS7 填充
        unpadder=padding.PKCS7(128).unpadder()
        plaintext=unpadder.update(padded_plaintext)+unpadder.finalize()

        print(f"{plaintext.decode('utf-8')}")


if __name__=="__main__":
    aes_decrypt()