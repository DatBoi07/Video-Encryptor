from Crypto.Cipher import AES


def decrypt_video(input_video, decrypted_video, key):
    encrypted_video = open(input_video, 'rb')

    iv = encrypted_video.read(AES.block_size)

    key = key.encode('utf-8')
    key = key + (b'\0' * (AES.block_size - len(key)))

    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(decrypted_video, 'wb') as decrypted_video:
        while True:
            chunk = encrypted_video.read(AES.block_size)
            if len(chunk) == 0:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            decrypted_video.write(decrypted_chunk)

    encrypted_video.close()