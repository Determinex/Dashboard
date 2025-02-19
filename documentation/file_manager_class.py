# Class for file operations
class FileManager:
    def __init__(self, directory, excluded_dirs, excluded_files):
        self.directory = Path(directory)
        self.excluded_dirs = excluded_dirs
        self.excluded_files = excluded_files
        self.supported_extensions = {'.py', '.html', '.js', '.css', '.txt'}

    def find_files_and_directories(self):
        files = []
        directory_structure = []
        folder_structure = {}

        for path in self.directory.rglob('*'):
            rel_path = path.relative_to(self.directory)

            # Check if the directory is excluded
            if path.is_dir():
                if any(excluded_dir in str(rel_path) for excluded_dir in self.excluded_dirs):
                    logging.debug(f"Excluding directory: {rel_path}")
                    continue  # Skip excluded directories
                
                # Add directory to the folder structure
                dirs = rel_path.parts
                current_level = folder_structure
                for folder in dirs:
                    if folder not in current_level:
                        current_level[folder] = {}
                    current_level = current_level[folder]

                # Append to directory structure for TOC
                directory_structure.append('│   ' * (len(dirs) - 1) + '├── ' + dirs[-1])  # Visibly format directory

            elif path.is_file() and path.suffix in self.supported_extensions:
                # Check if the file is excluded
                file_name_with_extension = f"{path.stem}{path.suffix}"
                if any(excluded_file in file_name_with_extension for excluded_file in self.excluded_files) or \
                   any(excluded_dir in str(path.parent) for excluded_dir in self.excluded_dirs):
                    logging.debug(f"Excluded file: {file_name_with_extension}")
                    continue  # Skip excluded files

                current_level = folder_structure
                for folder in rel_path.parent.parts:
                    current_level = current_level.get(folder, {})
                current_level[path.name] = None  # Use None to indicate that this is a file

                # Add found file to the list
                files.append(path)

        # Build the tree structure for the directory
        def build_tree_structure(current, depth=0):
            for name, children in current.items():
                if children is None:  # It's a file
                    directory_structure.append(f"{'│   ' * depth}└── {name}")
                else:  # It's a directory
                    directory_structure.append(f"{'│   ' * depth}├── {name}")
                    build_tree_structure(children, depth + 1)

        build_tree_structure(folder_structure)

        logging.info(f"Found {len(files)} files and {len(directory_structure)} directories.")
        return files, directory_structure

    @staticmethod
    def read_file_generator(file_path):
        logging.debug(f"Reading file: {file_path}")
        try:
            with file_path.open('r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()  # Strip whitespace
                    if isinstance(line, str) and line:  # Only yield non-empty strings
                        yield line
                    else:
                        logging.warning(f"Skipping a non-string or empty line in {file_path}.")
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            yield ""  # Yield an empty string instead of None