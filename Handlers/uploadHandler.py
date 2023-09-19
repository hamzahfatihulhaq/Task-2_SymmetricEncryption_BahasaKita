import os
import tornado.web
import uuid
from AES_utils import decrypt_data,encrypt_data
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

class UploadHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            uploaded_file = self.request.files['file'][0]
            file_content = uploaded_file['body']

            # Membuat ID unik
            unique_id = self.create_unique_id()

            print(file_content)
            # Enkripsi file
            decrypted_data = decrypt_data(file_content)

            # print(decrypted_data)
            # Simpan file terenkripsi
            decrypted_filename = os.path.join("Uploads", unique_id)
            with open(decrypted_filename, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            self.write("File berhasil diunggah dan didekripsi.")

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

    def create_unique_id(self):
        # Kode untuk membuat ID unik di sini, misalnya dengan modul uuid
        unique_id = str(uuid.uuid4())  # Membuat UUID versi 4 (random)
        return unique_id
    