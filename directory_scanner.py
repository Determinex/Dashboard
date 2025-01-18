import os

def scan_directory(base_path, file_handler, indent_level=0):
    """Recursively scan the directory and write its structure to the given file handler."""
    try:
        # List all entries in the directory
        for entry in os.listdir(base_path):
            entry_path = os.path.join(base_path, entry)

            # Skip the script file itself and the output file
            if entry == os.path.basename(__file__) or entry == 'directory_structure.txt':
                continue
            
            # Format the entry with indentation and a tree-like structure
            prefix = ' ' * indent_level + '├── ' if indent_level > 0 else ''
            file_handler.write(f'{prefix}{entry}\n')
            
            # If the entry is a directory, recurse into it
            if os.path.isdir(entry_path):
                scan_directory(entry_path, file_handler, indent_level + 4)  # Increase indent for subdirectories
    except PermissionError:
        # Ignore directories that cannot be accessed
        pass
    except Exception as e:
        print(f"Error accessing {base_path}: {e}")

def main():
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Open a text file to write the directory structure with UTF-8 encoding
    with open('directory_structure.txt', 'w', encoding='utf-8') as file_handler:
        file_handler.write(f"Directory structure for: {os.path.basename(current_directory)}\n\n")
        scan_directory(current_directory, file_handler)

if __name__ == "__main__":
    main()