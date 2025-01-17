import os

def scan_directory(base_path):
    """Recursively scan the directory and list folders, files, and encrypted entries."""
    folder_names = []
    file_names = []
    encrypted_names = []

    for root, dirs, files in os.walk(base_path):
        # Collect folder names
        for dir_name in dirs:
            folder_names.append(os.path.join(root, dir_name))

        # Collect file names
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_names.append(file_path)

            # Check for encryption (placeholder logic, modify as needed)
            if is_encrypted(file_name):
                encrypted_names.append(file_path)

    return folder_names, file_names, encrypted_names

def is_encrypted(file_name):
    """Placeholder function to check if the file or folder is encrypted."""
    # Example: consider files starting with 'enc_' as encrypted
    return file_name.startswith('enc_')

def write_to_file(file_path, data):
    """Write the collected data to a specified file."""
    with open(file_path, 'w') as f:
        for line in data:
            f.write(f"{line}\n")

def main():
    # Get the current directory
    base_path = os.getcwd()

    # Scan the directory
    folder_names, file_names, encrypted_names = scan_directory(base_path)

    # Write results to files
    write_to_file('folder_names.txt', folder_names)
    write_to_file('file_names.txt', file_names)
    write_to_file('encrypted_list.txt', encrypted_names)

    print("Scanning complete. Results written to folder_names.txt, file_names.txt, and encrypted_list.txt.")

if __name__ == "__main__":
    main()