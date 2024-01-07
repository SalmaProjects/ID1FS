#!/usr/bin/env python3


from paython2 import FileSystem  # Import your FileSystem class from the filesystem.py file
import getpass
import os
import subprocess
from pathlib import Path
def color_input(prompt, color):
    colors = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'purple': '\033[95m',
        'pink': '\033[95m'
          # Ajout de la couleur violet
    }
    return input(f"{colors[color]}{prompt}{colors['reset']}").strip()
def login(fs):
    while True:
       	color_print_dual("          				*******************Welcome to ID 1 FS Terminal********************",'cyan','white')
        print("                                				Choose an option:")
        print("                                				1. Login")
        print("                                				2. Register")
        print("                                				3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")

            if fs.login(username, password):
                print("Login successful!")
                os.system('cls' if os.name == 'nt' else 'clear')
                return username
            else:
                print("Login failed. Please try again.\n")
        elif choice == "2":
            new_username = input("Enter a new username: ")
            new_password = getpass.getpass("Enter a password: ")
            fs.register_user(new_username, new_password)
            print("Registration successful!")
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please enter a valid option.\n")


def color_print_part(text_part, color):
    colors = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'pink': '\033[95m' 
    }
    return f"{colors[color]}{text_part}{colors['reset']}"

def color_print_dual(line, color1, color2, separator=":"):
    parts = line.split(separator, 1)
    
    # Vérifiez s'il y a au moins deux parties avant d'essayer d'accéder à la deuxième partie
    if len(parts) > 1:
        colored_part1 = color_print_part(parts[0], color1)
        colored_part2 = color_print_part(parts[1], color2)
        print(f"{colored_part1}{separator}{colored_part2}")
    else:
        # Si le séparateur n'est pas présent dans la ligne, appliquez la couleur uniquement à la première partie
        colored_part1 = color_print_part(parts[0], color1)
        print(colored_part1)
def execute_exiftool(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.strip()}"

# Inside your Python script where you handle the 'exifdata' command

def interact_with_file_system(fs, username):
    print(f"Welcome {username} to ID 1 FS Terminal. Enter 'help' for available commands.")
    while True:
        command = color_input(f"{username}@{username}-VirtualBox:~$ ", 'purple').strip()   
        if command == "help":
        	color_print_dual("     					********************Available commands********************", 'red', 'white')
        	color_print_dual("			add a directory 		     : adefr <directory_name>", 'cyan', 'yellow')
        	color_print_dual("			add a file 			     : adeff <file_name> <file_content>", 'cyan', 'yellow')
        	color_print_dual("			list the content of a directory      : sard <directory_to_list> ro default sard", 'cyan', 'yellow')
        	color_print_dual("			temporarily  delete a file 	     : azelft <file_name> ", 'cyan', 'yellow')
        	color_print_dual("			delete a file permanently 	     : azelfd <file_name> ", 'cyan', 'yellow')
        	color_print_dual("			delete a directory 	 	     : azelr <directory_name>", 'cyan', 'yellow')
        	color_print_dual("			restore a file 		             : rec <file_to_restore>", 'cyan', 'yellow')
        	color_print_dual("			add a file to a preview 	     : adef_f <file_name> <distination_directory>", 'cyan', 'yellow')
        	color_print_dual("			add a directory to a preview 	     : adef_r <directory_name> <distination_directory>", 'cyan', 'yellow')
        	color_print_dual("			set the permission 		     : amer <target_file> <permission>", 'cyan', 'yellow')
        	color_print_dual("			give the username 		     : ana ", 'cyan', 'yellow')
        	color_print_dual("			change the name of a file 	     : badel <current_name> <new_name>", 'cyan', 'yellow')
        	color_print_dual("			give the current date 	             : waqt", 'cyan', 'yellow')
        	color_print_dual("			cut a file			     : qas <file_name> <source_directory> <destination_directory>", 'cyan', 'yellow')
        	color_print_dual("			copy a file 			     : nasq <file_name> <source_directory> <destination_directory>", 'cyan', 'yellow')
        	color_print_dual("			search for a file                    : baht <file_name>", 'cyan', 'yellow')
        	color_print_dual("			read the content of a file           : iqra <file_name> [source_directory] or default iqra <file_name>", 'cyan', 'yellow')
        	color_print_dual("			add text to the file                 : zed <file_name> <text to add>", 'cyan', 'yellow')
        	color_print_dual("			list metadata of the file given      : bayanat <file_name>", 'cyan', 'yellow')
        	color_print_dual("			read the contenent of the log file   : showlog", 'cyan', 'yellow')
        	color_print_dual("			exiting the ID 1 FS terminal         : exit", 'cyan', 'yellow')
        elif command.startswith("bayanat"):
            parts = command.split(' ')
            if len(parts) == 2:
                file_name = parts[1]
                directory_path = fs.base_directory / 'Personal Folder'

                file_found = False
                for root, dirs, files in os.walk(directory_path):
                    if file_name in files:
                        file_path = Path(root) / file_name
                        exiftool_command = f'exiftool "{file_path.resolve()}"'  # Enclose path in double quotes to handle spaces
                        metadata = execute_exiftool(exiftool_command)
                        print(metadata)
                        file_found = True
                        break  # Stop the loop once the file is found

                if not file_found:
                    print(f"File '{file_name}' not found.")
            else:
                print("Invalid command format. Usage: bayanat <file_name>")
        elif command.startswith("adefr"):
            parts = command.split(' ')
            if len(parts) == 2:
                directory_name = parts[1]
                fs.adefr(directory_name)
            else:
                print("Invalid command format. Usage: adefr <directory_name>")
        elif command.startswith("adeff"):
            parts = command.split(' ', 2)
            if len(parts) == 3:
                file_name = parts[1]
                file_content = parts[2]
                fs.adeff(file_name, file_content)
            else:
                print("Invalid command format. Usage: adeff <file_name> <file_content>")
        elif command.startswith("sard"):
            parts = command.split(' ')
            if len(parts) == 2:
                directory_name = parts[1]
                fs.sard(directory_name)
            elif len(parts) == 1:
                fs.sard()  # If no directory is specified, list contents of current directory
            else:
                print("Invalid command format. Usage: sard <directory_to_list> ro default sard")
        elif command.startswith("azelft"):
            parts = command.split(' ')
            if len(parts) == 2:
                file_name = parts[1]
                fs.azelft(file_name)
            else:
                print("Invalid command format. Usage: azelft <file_name>")
        
        elif command.startswith("azelfd"):
            parts = command.split(' ')
            if len(parts) == 2:
                file_name = parts[1]
                fs.azelfd(file_name)
            else:
                print("Invalid command format. Usage: azelfd <file_name>")
        elif command.startswith("azelr"):
            parts = command.split(' ')
            if len(parts) == 2:
                directory_name = parts[1]
                fs.azelr(directory_name)
            else:
                print("Invalid command format. Usage: azelr <directory_name>")
        elif command.startswith("rec"):
            file_to_restore = command.split(' ', 1)
            if len(file_to_restore) == 2:
                file_to_restore = file_to_restore[1]
                fs.rec(file_to_restore)
            else:
                print("Invalid command format. Usage: rec <file_to_restore>")
        elif command.startswith("adef_r"):
            parts = command.split(' ')
            if len(parts) == 3:
                directory_name = parts[1]
                target_directory = parts[2]
                fs.adef_r(directory_name, target_directory)
            else:
                print("Invalid command format. Usage: adef_r <directory_name> <distination_directory>")
        elif command.startswith("adef_f"):
            parts = command.split(' ')
            if len(parts) == 3:
                file_name = parts[1]
                target_directory = parts[2]
                fs.adef_f(file_name, target_directory)
            else:
                print("Invalid command format. Usage: adef_f <file_name> <distination_directory>")
        elif command.startswith("amer"):
            parts = command.split(' ')
            if len(parts) == 3:
                target_file = parts[1]
                permission = parts[2]
                fs.amer(target_file, permission)
            else:
                print("Invalid command format. Usage: amer <target_file> <permission>")
        elif command == "ana":
            fs.ana()
        elif command.startswith("badel"):
            parts = command.split(' ', 2)
            if len(parts) == 3:
                current_name = parts[1]
                new_name = parts[2]
                fs.badel(current_name, new_name)
            else:
                print("Invalid command format. Usage: badel <current_name> <new_name>")
        elif command == "waqt":
            fs.waqt()
        elif command.startswith("qas"):
            parts = command.split(' ')
            if len(parts) == 4:
                file_name = parts[1]
                source_directory = parts[2]
                destination_directory = parts[3]
                fs.qas(file_name, source_directory, destination_directory)
            else:
                print("Invalid command format. Usage: qas <file_name> <source_directory> <destination_directory>")
        elif command.startswith("nasq"):
            parts = command.split(' ')
            if len(parts) == 4:
                file_name = parts[1]
                source_directory = parts[2]
                destination_directory = parts[3]
                fs.nasq(file_name, source_directory, destination_directory)
            else:
                print("Invalid command format. Usage: nasq <file_name> <source_directory> <destination_directory>")
        elif command.startswith("baht"):
            parts = command.split(' ')
            if len(parts) == 2:
                file_name = parts[1]
                fs.baht(file_name)
            else:
                print("Invalid command format. Usage: baht <nom_fichier>")
        elif command.startswith("iqra"):
            parts = command.split(' ')
            if len(parts) == 3:
                file_name = parts[1]
                source_directory = parts[2]
                fs.iqra(file_name, source_directory)
            elif len(parts) == 2:
                file_name = parts[1]
                fs.iqra(file_name)
            else:
                print("Invalid command format. Usage: iqra <file_name> [source_directory] or default iqra <file_name> ")
        elif command.startswith("zed"):
            parts = command.split(' ', 2)
            if len(parts) == 3:
                nom_fichier = parts[1]
                texte_a_ajouter = parts[2]
                fs.zed(nom_fichier, texte_a_ajouter)
            else:
                print("Invalid command format. Usage: zed <nom_fichier> <texte_a_ajouter>")
        elif command == "showlog":
            fs.showlog()                
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Enter 'help' for available commands.")

if __name__ == "__main__":
	while True:
		username = getpass.getuser()
		base_directory = f"/home/{username}/Documents/MyFileSystem"  # Construct the base directory path
		fs = FileSystem(base_directory)
		logged_in_username = login(fs)
		interact_with_file_system(fs, logged_in_username)
    
    
    
    

    
