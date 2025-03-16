import base64 as b64
from Cryptodome.Cipher import AES
import secrets

# base64相关函数
# 编码
def b64encode(content):
    '''
        忘了当时为什么要这么写，
        怕报错所以保留
    '''
    try:
        return str(b64.b64encode(content.encode("utf-8")), "utf-8")
    except:
        return str(b64.b64encode(content), "utf-8")

# 解码
def b64decode(content):
        return b64.b64decode(content)


# 补足16位
def add_to_16(content):
    return (content + ('\0' * (16 - (len(content.encode("utf-8")) % 16)))).encode("utf-8")


# AES加密相关函数（使用ECB模式，不安全！）
# 加密
def aesencrypt(content: str, key: str):
    content = add_to_16(content)
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(content)

# 解密
def aesdecrypt(content: str, key: str):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(content).decode().rstrip("\0")


# 生成随机秘钥
def randkey(lenth: int):
    return b64encode(secrets.token_bytes(lenth))


# 整合
# 加密
def tkcuencrypt(content: str, key: str):
    return b64encode(aesencrypt(b64encode(content), b64decode(key)))

# 解密
def tkcudecrypt(content: str, key: str):
    return b64decode(aesdecrypt(b64decode(content), b64decode(key))).decode("utf-8")


# 调试
# print(randkey(16))