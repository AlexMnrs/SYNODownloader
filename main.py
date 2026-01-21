import sys
import os
from src.config import Config
from src.client import SynologyClient

def main():
    # Clear screen (cross-platform way)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Validate configuration
    error = Config.validate()
    if error:
        print(f"Configuration Error: {error}")
        print("Please check your .env file.")
        sys.exit(1)

    print("[*] Initializing SYNODownloader...")
    
    client = SynologyClient(
        url=Config.SYNO_URL,
        user=Config.SYNO_USER,
        password=Config.SYNO_PASSWORD,
        download_path=Config.DOWNLOAD_PATH
    )

    try:
        print("[*] Logging in...")
        if not client.login():
            print("[!] Login failed. Check credentials.")
            sys.exit(1)
        
        print("[+] Login successful.")
        
        # In this refactored version, we need a root path to list files from.
        # Since the old script hardcoded PATH from credentials, we should probably 
        # ask the user or use a default if not in .env (though .env variable for remote path wasn't explicitly planned, 
        # the old code had 'PATH' in credentials.py). 
        # Let's assume the user wants to list a specific folder or root. 
        # For now, I'll ask for a path if it's not clear, or default to root '/'.
        # However, the old script had a 'PATH' variable. Let's look if I missed adding a REMOTE_PATH to config.
        # I did not add REMOTE_PATH to Config in the plan, but it's needed functionality.
        # I will assume the user will input it or we start at root.
        # Let's ask the user for the remote folder to list, or default to '/'
        
        remote_path = input("[?] Enter remote folder path to list (default: /): ").strip() or "/"
        
        print(f"[*] Listing files in {remote_path}...")
        files = client.list_files(remote_path)
        
        if not files:
            print("[!] No files found or access denied.")
        else:
            print("\nAvailable files:")
            for index, filename in files.items():
                print(f"[{index}] {filename}")
            
            while True:
                try:
                    choice_input = input("\n[*] Choose a file number (or 'q' to quit): ")
                    if choice_input.lower() == 'q':
                        break
                        
                    choice = int(choice_input)
                    if choice in files:
                        filename = files[choice]
                        confirm = input(f"[*] Download '{filename}'? (y/n): ")
                        if confirm.lower() == 'y':
                            print(f"[*] Downloading {filename}...")
                            if client.download_file(remote_path, filename):
                                print(f"[+] Successfully downloaded to {client.download_path}")
                            else:
                                print("[!] Download failed.")
                    else:
                        print("[!] Invalid selection.")
                except ValueError:
                    print("[!] Please enter a number.")

    except KeyboardInterrupt:
        print("\n\n[*] Operation interrupted by user.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
    finally:
        print("[*] Logging out...")
        client.logout()

if __name__ == '__main__':
    main()