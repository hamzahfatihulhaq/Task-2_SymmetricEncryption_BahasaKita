from Crypto.Cipher import AES, DES3, ChaCha20
from Crypto.Random import get_random_bytes
import os
import time
from base64 import b64encode, b64decode


sample_dir = 'Sampel'
result_dir = 'Hasil'
# files = ['file1KB', 'file1MB', 'file10MB', 'file50MB', 'file100MB']
files = ['test.txt']

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# algorithms = ["AES", "ChaCha20", "DES3"]
algorithms = ["AES"]

def AES_Algorithms(data):
    # Encrypt
    key = get_random_bytes(32)

    start_time = time.time()

    e_cipher = AES.new(key, AES.MODE_EAX)
    print(type(key))
    cipher_nonce = e_cipher.nonce
    ciphertext, tag = e_cipher.encrypt_and_digest(data)
    # print(ciphertext)
    encryption_time = time.time() - start_time

    result_file = f'Test_result'

    with open(os.path.join(result_dir, result_file), 'wb') as result_f:
        result_f.write(ciphertext)


    # Decrypt
    start_time = time.time()
    d_cipher = AES.new(key, AES.MODE_EAX, cipher_nonce)
    print(key)
    # Verify and decrypt
    with open(os.path.join(result_dir, result_file), 'rb') as f:
        ciphertext1 = f.read()
    
    d_data = d_cipher.decrypt(ciphertext1)
    # print(d_data)
    
    try:
        d_cipher.verify(tag)

    except ValueError:
        print("Key incorrect or message corrupted")
    
    decryption_time = time.time() - start_time

    return encryption_time, decryption_time

def DES3_Algorithms(data):
    # Generate random 24-byte (192-bit) key for Triple DES
    key = get_random_bytes(24)
    iv = get_random_bytes(8)  # IV should be 8 bytes for DES3 in CFB mode

    start_time = time.time()

    # Create a Triple DES cipher object with CFB mode and IV
    e_cipher = DES3.new(key, DES3.MODE_CFB, iv=iv)

    # Encrypt the data
    ciphertext = e_cipher.encrypt(data)

    encryption_time = time.time() - start_time

    # Decrypt the data
    start_time = time.time()
    d_cipher = DES3.new(key, DES3.MODE_CFB, iv=iv)

    d_data = d_cipher.decrypt(ciphertext)

    decryption_time = time.time() - start_time

    return encryption_time, decryption_time

def CHACHA20_Algorithms(data):
    key = get_random_bytes(32)
    
    # Encrypt the data
    start_time = time.time()

    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(data)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ciphertext).decode('utf-8')
    
    encryption_time = time.time() - start_time

    # Decrypt the data
    start_time = time.time()
    try:
        cipher = ChaCha20.new(key=key, nonce=b64decode(nonce))
        plaintext = cipher.decrypt(b64decode(ct))

    except (ValueError, KeyError):
        print("Incorrect decryption")
    
    decryption_time = time.time() - start_time

    return encryption_time, decryption_time
    
for cipher_name in algorithms:
    results = []
    for file in files:
        with open(os.path.join(sample_dir, file), 'rb') as f:
            data = f.read()

        if cipher_name == "AES": 
            print("The message is authentic AES")
            encryption_time, decryption_time = AES_Algorithms(data)
        
        elif cipher_name == "DES3":
            print("The message is authentic 3DES")
            encryption_time, decryption_time = DES3_Algorithms(data)

        elif cipher_name == "ChaCha20":
            print("The message is authentic Chacha2")
            encryption_time, decryption_time = CHACHA20_Algorithms(data)
            
        
        result = {
            "File": file,
            "Algorithm": cipher_name,
            "Encryption_Time": round(encryption_time, 6),
            "Decryption_Time": round(decryption_time, 6)
        }

        results.append(result)
    
    result_file = f'{cipher_name}_result.txt'
    with open(os.path.join(result_dir, result_file), 'w') as result_f:
        for result in results:
            result_f.write(f"File: {result['File']}, Algorithm: {result['Algorithm']}\n")
            result_f.write(f"Encryption Time: {result['Encryption_Time']} seconds\n")
            result_f.write(f"Decryption Time: {result['Decryption_Time']} seconds\n")
            result_f.write("---\n")
