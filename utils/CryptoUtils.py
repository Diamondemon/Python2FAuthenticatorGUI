from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

from utils.CryptoParams import CryptoParams
from utils.CryptoResult import CryptoResult
from utils.SCryptParams import SCryptParams

CRYPTO_TAG_LEN = 16
CRYPTO_KEY_LEN = 32


def create_decrypt_cipher(key: bytes, nonce: bytes):
    return AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=CRYPTO_TAG_LEN)


def create_encrypt_cipher(key: bytes):
    return AES.new(key, AES.MODE_GCM, mac_len=CRYPTO_TAG_LEN)


def encrypt(key: bytes, decrypted: bytes, cipher=None):
    if cipher is None:
        cipher = AES.new(key, AES.MODE_GCM, mac_len=CRYPTO_TAG_LEN)
    encrypted = cipher.encrypt(decrypted)
    return CryptoResult(encrypted, CryptoParams(cipher.nonce, cipher.digest()))


def decrypt(key: bytes, encrypted, params: CryptoParams, cipher=None):
    if cipher is None:
        cipher = AES.new(key, AES.MODE_GCM, nonce=params.nonce)
    decrypted = cipher.decrypt_and_verify(encrypted, params.tag)

    return CryptoResult(decrypted, params)


def generate_salt():
    return get_random_bytes(CRYPTO_KEY_LEN)


def derive_key(password: str, params: SCryptParams):
    key_bytes = scrypt(password, params.salt, CRYPTO_KEY_LEN, params.n, params.r, params.p)
    return key_bytes
