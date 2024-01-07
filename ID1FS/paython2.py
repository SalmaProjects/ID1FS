import os
import stat
import shutil
import logging
import hashlib
import json
import getpass
from pathlib import Path
from datetime import datetime

class Directory:
    def __init__(self, name):
        self.name = name
        self.children = {}  # Store child directories/files

    def add_directory(self, directory_name):
        if directory_name not in self.children:
            new_directory = Directory(directory_name)
            self.children[directory_name] = new_directory

    def add_file(self, file_name, content):
        if file_name not in self.children:
            self.children[file_name] = content
        else:
            print(f"File '{file_name}' already exists in '{self.name}' directory.")

    def list_contents(self):
        print(f"Contents of directory '{self.name}':")
        for item in self.children:
            if isinstance(self.children[item], Directory):
                print(f"Directory: {item}")
            else:
                print(f"File: {item}")

class FileSystem:
    def __init__(self, base_directory):
        self.root = Directory('root')
        self.base_directory = Path(base_directory)
        log_directory = self.base_directory / 'logs'
        log_file_path = log_directory / 'file_system.log'
        if not log_directory.exists():
            log_directory.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('file_system')

        self.users_directory = self.base_directory / 'Personal Folder'  # Path to the users directory
        self.create_users_directory()
    def create_users_directory(self):
        if not self.users_directory.exists():
            self.users_directory.mkdir(parents=True)  # Create the users directory along with parent directories if missing

        self.users_file = self.base_directory / 'users.json'
        self.load_users()

    def load_users(self):
        if not self.users_file.exists():
            self.users = {}
        else:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
        else:
            hashed_password = self.hash_password(password)
            self.users[username] = hashed_password
            self.save_users()
            print("User registered successfully.")

    def login(self, username, password):
        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username] == hashed_password:
                print("Login successful.")
                return True
            else:
                print("Invalid password. Please try again.")
        else:
            print("User not found. Please register.")

        return False
        
    def showlog(self):
        log_file_path = self.base_directory / 'logs' / 'file_system.log'
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()
                print(log_content)
        except FileNotFoundError:
            print("Log file not found.")
        except Exception as e:
            print(f"Error occurred while reading the log file: {e}")
    def adeff(self, filename, content):
        try:
            file_path = self.base_directory / 'Personal Folder' / 'UserFiles' / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Create the file
            with open(file_path, 'w') as file:
                file.write(content)

            # Set permissions for the created file
            os.chmod(file_path, 0o644)  # Example: Read/write for owner, read-only for group and others

            log_msg = f"File '{filename}' created in directory '{self.base_directory / 'UserFiles'}' with content '{content}'."
            logging.info(log_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

    def sard(self, directory_name='.'):
        try:
            directory_path = self.base_directory / 'Personal Folder' / directory_name
            directory_path = directory_path.resolve()

            if directory_path.exists() and directory_path.is_dir():
                files = os.listdir(directory_path)

                log_msg = f"Listing contents of '{directory_name}':"
                print(log_msg)
                logging.info(log_msg)

                for item in files:
                    print(item)

            else:
                error_msg = f"Directory '{directory_name}' does not exist or is not a directory."
                print(error_msg)
                logging.error(error_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)
    def adefr(self, directory_name):
        try:
            directory_path = self.base_directory / 'Personal Folder' / directory_name

            # Create the directory
            directory_path.mkdir(parents=True, exist_ok=True)

            # Set permissions for the created directory
            os.chmod(directory_path, 0o755)  # Example: Read/write/execute for owner, read/execute for group and others

            log_msg = f"Directory '{directory_name}' created in directory '{self.base_directory}'"
            
            logging.info(log_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

    def azelft(self, file_name):
        try:
            destination_directory = self.base_directory / 'Personal Folder' / 'moved_files'

            if not destination_directory.exists():
                destination_directory.mkdir(parents=True, exist_ok=True)

            for root, dirs, files in os.walk(self.base_directory):
                if file_name in files:
                    source_file_path = Path(root) / file_name
                    destination_file_path = destination_directory / file_name

                    shutil.move(source_file_path, destination_file_path)

                    log_msg = f"File '{file_name}' moved to '{destination_directory}' successfully."
                    
                    logging.info(log_msg)
                    return
            error_msg = f"File '{file_name}' not found in the current directory or its subdirectories."
            
            logging.error(error_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)

    def rec(self, file_to_restore):
        try:
            moved_files_path = self.base_directory / 'Personal Folder' / 'moved_files'

            if moved_files_path.exists() and moved_files_path.is_dir():
                moved_files = os.listdir(moved_files_path)

                
                for file in moved_files:
                    print(file)

                user_files_path = self.base_directory / 'Personal Folder' / 'UserFiles'
                if not user_files_path.exists():
                    user_files_path.mkdir()

                if file_to_restore in moved_files:
                    source_file_path = moved_files_path / file_to_restore
                    destination_file_path = user_files_path / file_to_restore

                    if source_file_path.is_file():
                        shutil.move(source_file_path, destination_file_path)
                        log_msg = f"File '{file_to_restore}' restored to 'UserFiles' directory."
                        
                        logging.info(log_msg)
                    else:
                        error_msg = f"Error: '{file_to_restore}' is not a file."
                        print(error_msg)
                        logging.error(error_msg)
                else:
                    error_msg = f"Error: File '{file_to_restore}' not found in 'moved_files' directory."
                    print(error_msg)
                    logging.error(error_msg)
            else:
                error_msg = "Error: 'moved_files' directory does not exist."
                print(error_msg)
                logging.error(error_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)
    def adef_r(self, directory_name, target_directory):
        try:
            # Check if the target directory exists, create it if not
            target_dir_path = self.base_directory / 'Personal Folder' / target_directory
            if not target_dir_path.exists():
                target_dir_path.mkdir(parents=True, exist_ok=True)
                log_msg = f"Directory '{target_directory}' created successfully."
                logging.info(log_msg)
                print(log_msg)

            # Check if the directory exists in the target directory, create it if not
            new_directory_path = target_dir_path / directory_name
            if not new_directory_path.exists():
                new_directory_path.mkdir(parents=True, exist_ok=True)
                log_msg = f"Directory '{directory_name}' created inside '{target_directory}' successfully."
                logging.info(log_msg)
                
            else:
                log_msg = f"Directory '{directory_name}' already exists inside '{target_directory}'."
                logging.warning(log_msg)
                print(log_msg)

        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)

    def adef_f(self, file_name, target_directory):
        try:
            # Check if the target directory exists, create it if not
            target_dir_path = self.base_directory / 'Personal Folder' / target_directory
            if not target_dir_path.exists():
                target_dir_path.mkdir(parents=True, exist_ok=True)
                log_msg = f"Directory '{target_directory}' created successfully."
                logging.info(log_msg)
                print(log_msg)

            # Check if the file exists in the target directory, create it if not
            new_file_path = target_dir_path / file_name
            if not new_file_path.exists():
                with open(new_file_path, 'w') as file:
                    file.write("This is a sample content.")  # You can provide your content here
                log_msg = f"File '{file_name}' created inside '{target_directory}' successfully."
                logging.info(log_msg)
                
            else:
                log_msg = f"File '{file_name}' already exists inside '{target_directory}'."
                logging.warning(log_msg)
                print(log_msg)

        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)

    def azelr(self, directory_name):
        try:
            directory_found = False

            for root, dirs, files in os.walk(self.base_directory):
                if directory_name in dirs:
                    target_directory = Path(root) / directory_name

                    shutil.rmtree(target_directory)
                    log_msg = f"Directory '{directory_name}' removed from '{root}' successfully."
                    logging.info(log_msg)
                    
                    directory_found = True

            if not directory_found:
                log_msg = f"Directory '{directory_name}' not found in the file system."
                logging.warning(log_msg)
                

            log_msg = f"Search for '{directory_name}' completed."
            logging.info(log_msg)
            

        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)
    def azelfd(self, file_name):
        try:
            file_found = False

            for root, dirs, files in os.walk(self.base_directory /'Personal Folder'):
                if file_name in files:
                    target_file = Path(root) / file_name

                    # Remove the file
                    os.remove(target_file)
                    
                    log_msg = f"File '{file_name}' removed from '{root}' successfully."
                    logging.info(log_msg)
                    
                    
                    file_found = True

            if not file_found:
                log_msg = f"File '{file_name}' not found in the file system."
                logging.warning(log_msg)
                print(log_msg)

            log_msg = f"Search for '{file_name}' completed."
            logging.info(log_msg)
            

        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)
    def ana(self):
        try:
            nom_utilisateur = os.getlogin()
            log_msg = f"the current user : {nom_utilisateur}"
            logging.info(log_msg)
            print(log_msg)
        except Exception as e:
            error_msg = f"Erreur lors de la récupération du nom d'utilisateur : {e}"
            logging.error(error_msg)
            print(error_msg)

    def badel(self, current_name, new_name):
        try:
            directory_path = self.base_directory / 'Personal Folder'

            for root, dirs, files in os.walk(directory_path):
                if current_name in files:
                    current_file_path = Path(root) / current_name
                    new_file_path = Path(root) / new_name

                    current_file_path.rename(new_file_path)
                    log_msg = f"File '{current_name}' renamed to '{new_name}'."
                    logging.info(log_msg)
                    return

            log_msg = f"File '{current_name}' not found in '{directory_path}'."
            logging.warning(log_msg)
            print(log_msg)

        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)

    def waqt(self):
        try:
            date_actuelle = datetime.now()
            date_formattee = date_actuelle.strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"the current time : {date_formattee}"
            logging.info(log_msg)
            print(log_msg)
        except Exception as e:
            error_msg = f"Erreur lors de la récupération de la date actuelle : {e}"
            logging.error(error_msg)
            print(error_msg)

    def qas(self, file_name, source_directory='', destination_directory='.'):
        try:
            if not source_directory:
                source_directory = os.getcwd()

            source_path = self.base_directory / 'Personal Folder' / source_directory / file_name
            destination_path = self.base_directory / 'Personal Folder' / destination_directory / file_name

            if source_path.exists():
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.rename(destination_path)
                log_msg = f"File '{file_name}' moved to '{destination_directory}' successfully."
                logging.info(log_msg)
                
            else:
                log_msg = f"File '{file_name}' not found in '{source_path}'."
                logging.warning(log_msg)
                print(log_msg)
        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)

    def nasq(self, file_name, source_directory='UserFiles', destination_directory='.'):
        try:
            for root, dirs, files in os.walk(self.base_directory / 'Personal Folder' / source_directory):
                if file_name in files:
                    source_path = Path(root) / file_name
                    destination_path = self.base_directory / 'Personal Folder' / destination_directory / file_name

                    log_msg_before_copy = f"Before copying...\nSource Path: {source_path}\nDestination Path: {destination_path}"
                    logging.info(log_msg_before_copy)
                    

                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, destination_path)

                    log_msg_after_copy = f"File '{file_name}' copied to '{destination_directory}' successfully."
                    logging.info(log_msg_after_copy)
                   
                    return

            log_msg_not_found = f"File '{file_name}' not found in the '{source_directory}' directory or its subdirectories."
            logging.warning(log_msg_not_found)
            print(log_msg_not_found)
        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)
    def baht(self, file_name):
        try:
            for root, dirs, files in os.walk(self.base_directory):
                if file_name in files:
                    file_path = Path(root) / file_name
                    log_msg = f"File '{file_name}' found at: {file_path}"
                    print(log_msg)
                    logging.info(f"File '{file_name}' found at: {file_path}")
                    return

            not_found_msg = f"the file '{file_name}' doesn't exist."
            print(not_found_msg)
            logging.warning(f"File '{file_name}' not found.")

        except Exception as e:
            error_msg = f"Erreur lors de la recherche du fichier : {e}"
            print(error_msg)
            logging.error(f"Error searching for file '{nom_fichier}': {e}")
    def iqra(self, file_name, source_directory=None):
        try:
            if source_directory is None:
                for root, dirs, files in os.walk(self.base_directory / 'Personal Folder'):
                    if file_name in files:
                        file_path = Path(root) / file_name
                        with open(file_path, 'r') as file:
                            content = file.read()
                            log_msg = f"Content of file '{file_name}' :\n{content}"
                            logging.info(log_msg)
                            print(log_msg)
                        return

                log_msg_not_found = f"File '{file_name}' not found."
                logging.warning(log_msg_not_found)
                print(log_msg_not_found)
            else:
                file_path = self.base_directory / source_directory / file_name

                if file_path.exists() and file_path.is_file():
                    with open(file_path, 'r') as file:
                        content = file.read()
                        log_msg = f"Content of file '{file_name}' :\n{content}"
                        logging.info(log_msg)
                        print(log_msg)
                    log_msg_not_found = f"File '{file_name}' not found in '{self.base_directory / source_directory}' or is not a regular file."
                    logging.warning(log_msg_not_found)
                    print(log_msg_not_found)
        except Exception as e:
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            print(error_msg)

    def zed(self, nom_fichier, texte_a_ajouter):
        try:
            for root, dirs, files in os.walk(self.base_directory / 'Personal Folder'):
                if nom_fichier in files:
                    fichier_path = Path(root) / nom_fichier
                    with open(fichier_path, 'a') as fichier:
                        fichier.write(texte_a_ajouter + '\n')
                    log_msg = f"The text has been added to the file '{nom_fichier}'."
                    logging.info(log_msg)
                    
                    return

            log_msg_not_found = f"The file '{nom_fichier}' not found."
            logging.warning(log_msg_not_found)
            print(log_msg_not_found)
        except Exception as e:
            error_msg = f"Error adding text to file : {e}"
            logging.error(error_msg)
            print(error_msg)
    def amer(self, target_file, permissions):
        try:
            start_directory = self.base_directory / 'Personal Folder'
            found_file_path = self.find_file(start_directory, target_file)

            if found_file_path:
                current_permissions = os.stat(found_file_path).st_mode

                permission_mapping = {
                    'r': stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,  # Read
                    'w': stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,  # Write
                    'x': stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,  # Execute
                    'a': stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO,  # All (rwx for user, group, and others)
                }

                new_permissions = current_permissions  # Initialize with the current permissions

                for permission in permissions:
                    if permission not in permission_mapping:
                        print(f"Invalid permission: {permission}. Please enter valid permissions.")
                        return

                    new_permissions |= permission_mapping[permission]

                os.chmod(found_file_path, new_permissions)

                log_message = f"Permissions for file '{target_file}' at '{found_file_path}' changed to '{''.join(permissions)}'."
                
                logging.info(log_message)
            else:
                not_found_msg = f"File '{target_file}' not found in '{start_directory}' or its subdirectories."
                print(not_found_msg)
                logging.warning(not_found_msg)
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)

    def find_file(self, start_path, target_file):
        for dirpath, dirnames, filenames in os.walk(start_path):
            if target_file in filenames:
                return os.path.join(dirpath, target_file)
        return None
