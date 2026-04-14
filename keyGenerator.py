from cryptography.fernet import Fernet

# Generate a key. This must be kept secret!
key = Fernet.generate_key()

# The key is a URL-safe base64-encoded 32-byte key.
print("Your secret key is:", key.decode())

# It's crucial to save this key securely for later decryption.
# For example, write it to a file.
with open('secret.key', 'wb') as key_file:
    key_file.write(key)