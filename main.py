import sys
from time import monotonic
import requests
import os
import credentials

URL  =  credentials.URL
USER =  credentials.USER
PASS =  credentials.PASS
PATH =  credentials.PATH

def login(url, id, pw):
    sid = 0
    response = requests.get(url, 
                            params={'api': 'SYNO.API.Auth', 'version': 3, 'method':'login','account':id, 'passwd': pw, 'session':'FileStation', 'format': 'cookie'})
    response_dict = response.json()
    sid = response_dict['data']['sid']
    return sid

def list(url, path, sid):
    list_files = requests.get(url, 
                            params={'api':'SYNO.FileStation.List', 'version': 2, 'method':'list','additional':'','folder_path':"/" + path, '_sid':sid}
                            )
    response_dict = list_files.json()
    files = response_dict['data']['files']

    # Get all content in the path is not a directory
    index = 1
    tmp_files = {}
    for file in files:
        if file['isdir'] is not True:
            tmp_files[index] = file['name']
            index += 1
    
    # Print all files found in the path 
    for key, value in tmp_files.items():
        print("[{}] {}".format(str(key), str(value)))
    
    return tmp_files

def download(url, path, file, sid):
    download_request = requests.get(url, 
                                    params={'api':'SYNO.FileStation.Download', 'version': 2, 'method':'download', 'path':"/"+path+"/"+file, 'mode':'open', '_sid':sid},
                                    stream=True)
    code = download_request.status_code
    total = download_request.headers.get('content-length')

    # Check if the file requested to download exists 
    if total is None or code != 200:
        print("[*] The file doesn't exist.")
        return False

    with open(file, 'wb') as tmp_file:
        
        downloaded = 0
        total = int(total)
        start = last_print = monotonic()
        for chunk in download_request.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
            downloaded += len(chunk)
            now = monotonic()
            if chunk:
                tmp_file.write(chunk)
                done = int(100 * downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (100-done)))
                sys.stdout.flush()
                
            if now - last_print > 1:
                speed = round((downloaded / (now - start) / 1024) / 125)
                sys.stdout.write(f' - [{done}%, {speed} Mbps]')
                sys.stdout.flush()
                last_print = now
                
    sys.stdout.write('\n')
    

    print("\n[*] Download has been completed.\n")

def logout(url):
    response = requests.get(url, 
                            params={'api': 'SYNO.API.Auth', 'version': 1, 'method':'logout', 'session':'FileStation'})
    return response

def currDir():
    curr_dir = os.getcwd()
    return curr_dir

def setDownloadsFolder():
    user_folder = os.environ['USERPROFILE']
    os.chdir("{}\{}".format(user_folder, "Downloads"))
    
    print("[*] Your current directory is: {}".format(currDir()))
    
    downloads_folder = input("[*] Enter the name of the folder to download files: ")
    while os.path.isdir(downloads_folder):
         dec = input("[*] Folder already exists. Do you want to download files in -> {}? (y/n)".format(downloads_folder))
         if dec == 'y':
             os.chdir("{}\{}".format(currDir(), downloads_folder))
             print("[*] Download folder set to: {}\n".format(currDir()))
             break
         else:
            downloads_folder = input("[*] Enter different folder name than {}: ".format(downloads_folder))
            
    if not downloads_folder in currDir():
        os.mkdir(downloads_folder)
        print("[*] Folder {} created.".format(downloads_folder))
        os.chdir("{}\{}".format(currDir(), downloads_folder))
        print("[*] Current directory: {}\n".format(currDir()))

if __name__ == '__main__':
    os.system('cls')
        
    try:
        sid = login(URL, USER, PASS)
        setDownloadsFolder()
        try:
            files = list(URL, PATH, sid)
            while files:
                choice = int(input("\n[*] Choose a file (e.g. 6): "))
                verify_choice = str(input("\n[*] You have selected: {}. Are you sure? (y/n): ".format(files.get(choice))))
                if verify_choice in "y":
                    print("\n[*] Please, wait...\n")
                    download(url=URL, path=PATH, file=files.get(choice), sid=sid)
                    break     
            else:
                print("[*] That file doesn't exist.")
        except ValueError:
            print("[*] Invalid answer.")
            sys.exit(1) 
        logout(URL)
    except KeyboardInterrupt:
        print("\n\n[*] Download interrupted!")