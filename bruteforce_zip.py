import subprocess
import zipfile
import os
import sys
import rarfile

def print_usage():
    print("Usage: python bruteforce_archives.py -p /path/to/file -w /path/to/wordlist.txt")

def load_wordlist(wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"Wordlist file not found: {wordlist_path}")
        return []
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        return []


def try_zip_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path) as z:
            file_name = z.namelist()[0]  # Get the name of the first file
            z.extract(member=file_name, pwd=password.encode('utf-8'))  # Attempt extraction to test the password
            return True
    except (RuntimeError, zipfile.BadZipFile):
        return False

def try_7z_password(archive_path, password):
    command = ['7z', 'e', archive_path, f'-p{password}', '-y']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def try_rar_password(rar_path, password):
    try:
        with rarfile.RarFile(rar_path) as r:
            r.extract(r.namelist()[0], pwd=password)  # Attempt extraction
            return True
    except (rarfile.BadRarFile, RuntimeError):
        return False

def main():
    if len(sys.argv) != 5:
        print_usage()
        return 1

    archive_path = ""
    wordlist_path = ""

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-p":
            archive_path = sys.argv[i + 1]
        elif sys.argv[i] == "-w":
            wordlist_path = sys.argv[i + 1]

    # Check for the existence of the archive file
    if not os.path.exists(archive_path):
        print(f"Archive file not found: {archive_path}")
        return 1

    # Load the wordlist and check if it exists
    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        return 1  # Exit if wordlist is empty or not found

    # Check the file extension to determine which function to use
    file_extension = os.path.splitext(archive_path)[1].lower()

    for i, password in enumerate(wordlist, start=1):  # Start enumeration at 1 for better readability
        print(f"Checking password {i}/{len(wordlist)}: {password}")  # Print current password and its number
        if file_extension == '.zip':
            if try_zip_password(archive_path, password):
                print("Password found successfully.")
                print(f"password: {password}")  # Print found password in the desired format
                return 0
        elif file_extension == '.7z':
            if try_7z_password(archive_path, password):
                print("Password found successfully.")
                print(f"password: {password}")  # Print found password in the desired format
                return 0
        elif file_extension == '.rar':
            if try_rar_password(archive_path, password):
                print("Password found successfully.")
                print(f"password: {password}")  # Print found password in the desired format
                return 0





    print("No password found in the wordlist.")
    return 0

if __name__ == "__main__":
    main()
