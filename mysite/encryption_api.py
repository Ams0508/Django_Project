from cryptography.fernet import Fernet

#to generate a secret key:
'''
secret_key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(secret_key)
'''

def encrypt_password(password):
    #1. Load the secret key from the file
    with open('secret.key', 'rb') as key_file:
        secret_key = key_file.read()
    
    #2. Create a Fernet object with the secret key
    fernet = Fernet(secret_key)

    # Encrypt the password using the Fernet object
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    #1. Load the secret key from the file
    with open('secret.key', 'rb') as key_file:
        secret_key = key_file.read()
    
    #2. Create a Fernet object with the secret key
    fernet = Fernet(secret_key)
    
    # Decrypt the password using the Fernet object
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password
#print(decrypt_password(b'gAAAAABkI-uoWx1WZs1hR2K1tRm0iP5Ko3cQUfm6fbKxNiA9kmE9j617wTbX_cw-4wwdhj0fuI2MDSQNCg_k1edHya7XE4ngnQ=='))