from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from decouple import config
SECRET_KEY = config('SECRET_KEY').encode('utf-8')

# Fungsi untuk enkripsi data menggunakan AES
def encrypt_data(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    # print(SECRET_KEY)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext + tag

# Fungsi untuk dekripsi data menggunakan AES
def decrypt_data(data):
    # print(SECRET_KEY)
    nonce = data[:16]
    ciphertext = data[16:-16]
    tag = data[-16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext