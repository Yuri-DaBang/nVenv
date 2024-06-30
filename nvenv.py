import argparse
import os
import shutil
import subprocess
import getpass
from colorama import init, Fore, Style
from cryptography.fernet import Fernet
import base64
import glob

# Initialize colorama
init(autoreset=True)

TRASH_DIR = os.path.join(os.path.expanduser("~"), "TrashENVs")
BACKUP_DIR = os.path.join(os.path.expanduser("~"), "EnvBackups")

def ensure_dirs_exist():
    """Ensure necessary directories exist."""
    if not os.path.exists(TRASH_DIR):
        os.makedirs(TRASH_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def generate_key(password):
    """Generate encryption key from password."""
    password_bytes = password.encode('utf-8')
    key = base64.urlsafe_b64encode(password_bytes.ljust(32)[:32])
    return key

def encrypt_directory(directory, key):
    """Encrypt files in the directory using the given key."""
    fernet = Fernet(key)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)

def decrypt_directory(directory, key):
    """Decrypt files in the directory using the given key."""
    fernet = Fernet(key)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                decrypted_data = fernet.decrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(decrypted_data)
            except Exception as e:
                print(Fore.RED + f"Error decrypting file {file_path}: {str(e)}")

def create_env(env_name, password, location=None, temporary=False):
    """Create a new environment."""
    env_path = get_env_path(env_name, location)
    if not os.path.exists(env_path):
        os.makedirs(env_path)
        with open(os.path.join(env_path, "cmds.log"), "w") as log_file:
            log_file.write("")

        # Create senv directory for shell environment
        senv_path = os.path.join(env_path, "senv")
        os.makedirs(senv_path)

        # Encrypt the environment directory
        key = generate_key(password)
        encrypt_directory(env_path, key)

        if temporary:
            with open(os.path.join(env_path, ".temporary"), "w") as temp_file:
                temp_file.write("This is a temporary environment.")

        print(Fore.GREEN + f"Environment '{env_name}' created successfully.")
        if temporary:
            print(Fore.YELLOW + "This is a temporary environment and will be moved to TrashENVs upon exit.")
    else:
        print(Fore.YELLOW + f"Environment '{env_name}' already exists.")

def run_env(env_name, password, location=None):
    """Run commands within the specified environment."""
    env_path = get_env_path(env_name, location)
    if os.path.exists(env_path):
        key = generate_key(password)
        decrypt_directory(env_path, key)
        try:
            while True:
                cmd = input(f"{env_name}"+ Fore.GREEN + " > " + Style.RESET_ALL)
                with open(os.path.join(env_path, "cmds.log"), "a") as log_file:
                    if not (cmd.startswith("wcmd ") or cmd.startswith("wps ")):
                        log_file.write(cmd + "\n")
                if cmd.startswith("wcmd "):
                    command = cmd[len("wcmd "):]
                    process = subprocess.Popen(command, shell=True, cwd=os.path.join(env_path, "senv"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    print(out.decode() if out else print(f"<return with-err>"))
                elif cmd.startswith("wps "):
                    command = cmd[len("wps "):]
                    process = subprocess.Popen(["powershell", "-Command", command], cwd=os.path.join(env_path, "senv"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    print(out.decode() if out else print(f"<return with-err>"))
                elif cmd == "exit":
                    encrypt_directory(env_path, key)
                    if os.path.exists(os.path.join(env_path, ".temporary")):
                        shutil.move(env_path, os.path.join(TRASH_DIR, env_name))
                        print(Fore.YELLOW + f"Temporary environment '{env_name}' moved to TrashENVs.")
                    break
                else:
                    command = cmd
                    process = subprocess.Popen(["powershell", "-Command", command], cwd=os.path.join(env_path, "senv"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    print(out.decode() if out else print(f"<return with-err>"))
        except KeyboardInterrupt:
            encrypt_directory(env_path, key)
            if os.path.exists(os.path.join(env_path, ".temporary")):
                shutil.move(env_path, os.path.join(TRASH_DIR, env_name))
                print(Fore.YELLOW + f"Temporary environment '{env_name}' moved to TrashENVs.")
            print("KeyboardInterrupt: ENCRYPTION COMPLETE!")
            exit()
        encrypt_directory(env_path, key)
    else:
        print(Fore.RED + f"Environment '{env_name}' does not exist.")

def remove_env(env_name, password, location=None):
    """Remove an environment and move it to TrashENVs directory."""
    env_path = get_env_path(env_name, location)
    if os.path.exists(env_path):
        key = generate_key(password)
        decrypt_directory(env_path, key)
        shutil.move(env_path, os.path.join(TRASH_DIR, env_name))
        print(Fore.GREEN + f"Environment '{env_name}' removed and moved to Trash.")
    else:
        print(Fore.YELLOW + f"Environment '{env_name}' does not exist.")

def clone_env(target_name, new_name, password, location=None):
    """Clone an existing environment."""
    target_path = get_env_path(target_name, location)
    new_path = get_env_path(new_name, location)
    if os.path.exists(target_path):
        shutil.copytree(target_path, new_path)
        print(Fore.GREEN + f"Environment '{target_name}' cloned as '{new_name}' successfully.")
    else:
        print(Fore.RED + f"Environment '{target_name}' does not exist.")

def backup_env(env_name, password, location=None):
    """Backup an environment."""
    env_path = get_env_path(env_name, location)
    if os.path.exists(env_path):
        key = generate_key(password)
        decrypt_directory(env_path, key)
        shutil.make_archive(os.path.join(BACKUP_DIR, env_name), 'zip', env_path)
        print(Fore.GREEN + f"Environment '{env_name}' backed up successfully.")
        encrypt_directory(env_path, key)
    else:
        print(Fore.RED + f"Environment '{env_name}' does not exist.")

def clean_log(env_name, password, location=None):
    """Clean the commands log of an environment."""
    env_path = get_env_path(env_name, location)
    log_path = os.path.join(env_path, "cmds.log")
    if os.path.exists(log_path):
        key = generate_key(password)
        decrypt_directory(env_path, key)
        with open(log_path, "r") as log_file:
            lines = log_file.readlines()
        filtered_lines = [line for line in lines if not any(line.strip().startswith(cmd) for cmd in ["wcmd ", "wps "])]
        with open(log_path, "w") as log_file:
            log_file.writelines(filtered_lines)
        print(Fore.GREEN + f"Log cleaned for environment '{env_name}'.")
        encrypt_directory(env_path, key)
    else:
        print(Fore.YELLOW + f"No log found for environment '{env_name}'.")

def get_env_path(env_name, location=None):
    """Get full path to the environment directory."""
    if location:
        return os.path.join(location, env_name)
    else:
        return os.path.join(os.getcwd(), env_name)

def main():
    """Main function to handle argument parsing."""
    ensure_dirs_exist()

    parser = argparse.ArgumentParser(description=Fore.YELLOW + "Manage partial user spaces (environments)." + Style.RESET_ALL)
    subparsers = parser.add_subparsers(dest="command")

    parser_mkenv = subparsers.add_parser("mkenv", help="Create a new environment.")
    parser_mkenv.add_argument("name", type=str, help="Name of the environment.")
    parser_mkenv.add_argument("password", type=str, help="Password for encryption.")
    parser_mkenv.add_argument("-loc", type=str, help="Location to create the environment.", default=None)
    parser_mkenv.add_argument("-temp", action="store_true", help="Create a temporary environment that will be moved to TrashENVs upon exit.")
    parser_mkenv.add_argument("-run", action="store_true", help="Create and immediately run the environment.")

    parser_run = subparsers.add_parser("run", help="Run commands within an environment.")
    parser_run.add_argument("name", type=str, help="Name of the environment.")
    parser_run.add_argument("password", type=str, help="Password for encryption.")
    parser_run.add_argument("-loc", type=str, help="Location of the environment.", default=None)

    parser_rmenv = subparsers.add_parser("rmenv", help="Remove an environment.")
    parser_rmenv.add_argument("name", type=str, help="Name of the environment.")
    parser_rmenv.add_argument("password", type=str, help="Password for encryption.")
    parser_rmenv.add_argument("-loc", type=str, help="Location of the environment.", default=None)

    parser_clenv = subparsers.add_parser("clenv", help="Clone an existing environment.")
    parser_clenv.add_argument("target_name", type=str, help="Name of the environment to clone.")
    parser_clenv.add_argument("new_name", type=str, help="Name for the new cloned environment.")
    parser_clenv.add_argument("password", type=str, help="Password for encryption.")
    parser_clenv.add_argument("-loc", type=str, help="Location to create the new environment.", default=None)

    parser_backup = subparsers.add_parser("backup", help="Backup an environment.")
    parser_backup.add_argument("name", type=str, help="Name of the environment.")
    parser_backup.add_argument("password", type=str, help="Password for encryption.")
    parser_backup.add_argument("-loc", type=str, help="Location of the environment.", default=None)

    parser_clean = subparsers.add_parser("clean", help="Clean the commands log of an environment.")
    parser_clean.add_argument("name", type=str, help="Name of the environment.")
    parser_clean.add_argument("password", type=str, help="Password for encryption.")
    parser_clean.add_argument("-loc", type=str, help="Location of the environment.", default=None)

    args = parser.parse_args()

    if args.command == "mkenv":
        create_env(args.name, args.password, args.loc, args.temp)
        if args.run:
            run_env(args.name, args.password, args.loc)
    elif args.command == "run":
        run_env(args.name, args.password, args.loc) 
    elif args.command == "rmenv":
        remove_env(args.name, args.password, args.loc)
    elif args.command == "clenv":
        clone_env(args.target_name, args.new_name, args.password, args.loc)
    elif args.command == "backup":
        backup_env(args.name, args.password, args.loc)
    elif args.command == "clean":
        clean_log(args.name, args.password, args.loc)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()