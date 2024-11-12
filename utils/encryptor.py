from Crypto.Cipher import AES
import os


def encrypt_video(input_video, encrypted_video, key):
    video = open(input_video, 'rb')

    iv = os.urandom(AES.block_size)

    key = key.encode('utf-8')
    key = key + (b'\0' * (AES.block_size - len(key)))

    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(encrypted_video, 'wb') as encrypted_video:
        encrypted_video.write(iv)

        while True:
            chunk = video.read(AES.block_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % AES.block_size != 0:
                chunk += b' ' * (AES.block_size - len(chunk) % AES.block_size)
            encrypted_video.write(cipher.encrypt(chunk))

    video.close()
    