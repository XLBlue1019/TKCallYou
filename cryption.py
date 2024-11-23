import base64 as b64
from Crypto.Cipher import AES
import secrets


def b64encode(content):
    try:
        return str(b64.b64encode(content.encode("utf-8")), "utf-8")
    except:
        return str(b64.b64encode(content), "utf-8")


def b64decode(content):
        return b64.b64decode(content)


def add_to_16(content):
    return (content + ('\0' * (16 - (len(content.encode("utf-8")) % 16)))).encode("utf-8")


def aesencrypt(content: str, key: str):
    content = add_to_16(content)
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(content)

    
def aesdecrypt(content: str, key: str):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(content).decode().rstrip("\0")


def randkey(lenth: int):
    return b64encode(secrets.token_bytes(lenth))


def tkcuencrypt(content: str, key: str):
    return b64encode(aesencrypt(b64encode(content), b64decode(key)))


def tkcudecrypt(content: str, key: str):
    return b64decode(aesdecrypt(b64decode(content), b64decode(key))).decode("utf-8")

