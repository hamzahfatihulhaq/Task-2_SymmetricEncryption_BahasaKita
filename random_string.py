import random
import string

# Membuat string 32 byte dengan karakter acak (256 bit)
random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
print(random_string)