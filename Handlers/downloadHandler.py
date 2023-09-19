import os
import tornado.web
from AES_utils import decrypt_data,encrypt_data
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

class DownloadHandler(tornado.web.RequestHandler):
    def get(self, filename):
        # Baca file terenkripsi
        decrypted_filename = os.path.join("Uploads", filename)
        with open(decrypted_filename, "rb") as decrypted_file:
            decrypted_data = decrypted_file.read()

        # Dekripsi file
        encrypted_data = encrypt_data(decrypted_data)

        # Set header agar browser mengenali kontennya sebagai file
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', f'attachment; filename={filename}')
        
        # Kirim data terdekripsi ke browser
        self.write(encrypted_data)
