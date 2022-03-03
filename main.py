import sys
from turtle import down
import requests
import os

#DO NOT MODIFY
LOGIN_API    = 'webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account={}&passwd={}&session=FileStation&format=cookie'
LOGOUT_API   = 'webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=FileStation'
LIST_API     = 'webapi/entry.cgi?api=SYNO.FileStation.List&version=2&method=list&additional=&folder_path=/{}&_sid={}'
DOWNLOAD_API = 'webapi/entry.cgi?api=SYNO.FileStation.Download&version=2&method=download&path=/{}/{}&mode=open&_sid={}'

# CHANGE THIS
URL  =  'https://nas.quickconnect.to:65375/'
USER =  'admin'
PASS =  'password'
PATH =  'your_folder'

def login(url, id, pw):
    sid = 0
    response = requests.get(url+LOGIN_API.format(id, pw))
    response_dict = response.json()
    sid = response_dict['data']['sid']
    return sid

def list(url, path, sid):
    list_files = requests.get(url+LIST_API.format(path, sid))
    response_dict = list_files.json()
    files = response_dict['data']['files']

    index = 1
    tmp_files = {}
    for file in files:
        if file['isdir'] is not True:
            tmp_files[index] = file['name']
            index += 1
    
    for key, value in tmp_files.items():
        print("[{}] {}".format(str(key), str(value)))
    
    return tmp_files

def download(url, path, file, sid):
    download_request = requests.get(url+DOWNLOAD_API.format(path, file, sid), stream=True)
    code = download_request.status_code
    total = download_request.headers.get('content-length')

    if total is None or code != 200:
        print("[*] The file doesn't exist.")
        return False

    with open(file, 'wb') as tmp_file:
        
        downloaded = 0
        total = int(total)
        for chunk in download_request.iter_content(chunk_size=max(int(total/1000), 1024*1024)): #chunk_size=8192
            downloaded += len(chunk)
            if chunk:
                tmp_file.write(chunk)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()

    sys.stdout.write('\n')
    print("\n[*] Download has been completed.\n")

def logout(url, api):
    response = requests.get(url+api)
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
        logout(URL, LOGOUT_API)
    except KeyboardInterrupt:
        print("\n\n[*] Download interrupted!")