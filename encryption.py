from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Removed encryption functions as bcrypt will be used for password hashing.
