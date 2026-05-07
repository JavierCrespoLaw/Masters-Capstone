from cryptography.fernet import Fernet
import os

# File path and name of the symmetric key
directory_path = ".\\encryptionKey"
key_name = "filekey.key"

# Creates a symmetric key and saves it to the specified location
def createKey():
    key = Fernet.generate_key()
    os.makedirs(directory_path, exist_ok=True)

    with open(directory_path + '\\' + key_name, 'wb') as f:
        f.write(key)

def getFernetKey():
    with open(directory_path + '\\' + key_name, 'rb') as f:
        key = f.read()

    fernet = Fernet(key)
    return fernet

# Encrypts the given information with the symmetric key
def encryptInfo(info):
    fernet = getFernetKey()
    encryptedInfo = fernet.encrypt(info)

    return encryptedInfo

# Decrypts the given information with the symmetric key
def decryptInfo(info):
    fernet = getFernetKey()
    decryptedInfo = fernet.decrypt(info)

    return decryptedInfo