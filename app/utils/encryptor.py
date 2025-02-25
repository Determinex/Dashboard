import os
import json
import struct
import secrets
import sys
import logging
from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_key():
    """Retrieve the encryption key from environment variables."""
    return os.getenv('ENCRYPTION_KEY', 'default_secure_key_123!')

def encrypt_file(key, in_filename, out_filename=None):
    """Encrypts a file using AES with the given key."""
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = secrets.token_bytes(16)
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    with open(in_filename, 'rb') as infile:
        filesize = os.path.getsize(in_filename)
        magic = b"MyCrYpT"

        with open(out_filename, 'wb') as outfile:
            outfile.write(magic)
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(64 * 1024)  # 64KB
                if not chunk:
                    break
                if len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, out_filename=None):
    """Decrypts a file using AES with the given key."""
    if not out_filename:
        out_filename = in_filename[:-4]

    with open(in_filename, 'rb') as infile:
        data = infile.read()
        if data[:len(b"MyCrYpT")] != b"MyCrYpT":
            raise ValueError('Not an encrypted file')

        filedata = data[len(b"MyCrYpT"):]

        filesize = struct.unpack('<Q', filedata[:8])[0]
        iv = filedata[8:24]
        decryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            offset = 24
            while offset < len(filedata):
                chunk = filedata[offset:offset + 64 * 1024]  # 64KB
                if not chunk:
                    break
                outfile.write(decryptor.decrypt(chunk))
                offset += 64 * 1024
            
            outfile.truncate(filesize)

def encrypt_metadata(key, metadata):
    """Encrypts the metadata dictionary and returns it as bytes."""
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    iv = cipher.iv
    json_data = json.dumps(metadata)
    encrypted_data = cipher.encrypt(pad(json_data.encode('utf-8'), AES.block_size))
    return iv + encrypted_data  # Prepend IV to the encrypted data

def decrypt_metadata(key, encrypted_metadata):
    """Decrypts the metadata bytes and returns it as a dictionary."""
    iv = encrypted_metadata[:16]  # First 16 bytes are the IV
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_metadata[16:]), AES.block_size)
    return json.loads(decrypted_data)

def encrypt_directory_and_store_metadata(key, dir_path, metadata_file):
    """Encrypt all files in a directory recursively, store encrypted metadata, and delete originals."""
    metadata = {}
    
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            original_path = os.path.join(root, file_name)
            encrypted_name = f"{secrets.token_hex(8)}.enc"  # Create a random name for the encrypted file
            encrypted_path = os.path.join(root, encrypted_name)

            encrypt_file(key, original_path, encrypted_path)  # Encrypt the file
            os.remove(original_path)  # Delete original file after encryption

            # Store metadata
            metadata[encrypted_name] = {
                'original_name': file_name,
                'original_path': root,
                'extension': os.path.splitext(file_name)[1]
            }
            logging.info(f"Encrypted '{original_path}' to '{encrypted_path}' and deleted original.")

    # Encrypt the metadata and write to JSON file
    encrypted_metadata = encrypt_metadata(key, metadata)
    with open(metadata_file, 'wb') as meta_file:
        meta_file.write(encrypted_metadata)
    logging.info(f"Encrypted metadata stored in '{metadata_file}'.")

def decrypt_directory_and_restore(key, dir_path, metadata_file):
    """Decrypt all files in a directory using metadata and restore original names."""
    with open(metadata_file, 'rb') as meta_file:
        encrypted_metadata = meta_file.read()
        metadata = decrypt_metadata(key, encrypted_metadata)

    for encrypted_name, data in metadata.items():
        encrypted_path = os.path.join(dir_path, encrypted_name)
        
        if os.path.isfile(encrypted_path):
            original_name = data['original_name']
            original_path = os.path.join(data['original_path'], original_name)
            decrypt_file(key, encrypted_path, original_path)  # Decrypt the file

            os.remove(encrypted_path)  # Optionally delete the encrypted file
            logging.info(f"Decrypted '{encrypted_path}' to '{original_path}'.")

def check_encryption_status(dir_path, metadata_file):
    """Check encryption status of files in a directory using metadata."""
    if not os.path.isfile(metadata_file):
        logging.info("No metadata file found. Cannot check encryption status.")
        return

    with open(metadata_file, 'rb') as meta_file:
        encrypted_metadata = meta_file.read()
        metadata = decrypt_metadata(get_key(), encrypted_metadata)

    encrypted_files = list(metadata.keys())
    if encrypted_files:
        logging.info(f"Encrypted files in '{dir_path}': {', '.join(encrypted_files)}")
    else:
        logging.info(f"No encrypted files found in '{dir_path}'.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python encryptor.py -encrypt/-decrypt/-check <path_to_directory> [metadata_file] [key]")
        sys.exit(1)

    action = sys.argv[1]
    dir_path = sys.argv[2]
    metadata_file = sys.argv[3] if len(sys.argv) > 3 else "metadata.json"
    key = sys.argv[4] if len(sys.argv) == 5 else get_key()

    if action == '-encrypt':
        if os.path.isdir(dir_path):
            encrypt_directory_and_store_metadata(key, dir_path, metadata_file)
        else:
            logging.error(f"The path '{dir_path}' is not a directory.")

    elif action == '-decrypt':
        if os.path.isdir(dir_path):
            decrypt_directory_and_restore(key, dir_path, metadata_file)
        else:
            logging.error(f"The path '{dir_path}' is not a directory.")

    elif action == '-check':
        check_encryption_status(dir_path, metadata_file)

if __name__ == "__main__":
    main()