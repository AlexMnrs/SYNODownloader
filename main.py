import sys
import requests 

#DO NOT MODIFY
LOGIN_API    = 'webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account={}&passwd={}&session=FileStation&format=cookie'
LOGOUT_API   = 'webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=FileStation'
DOWNLOAD_API = 'webapi/entry.cgi?api=SYNO.FileStation.Download&version=2&method=download&path=/{}/{}&mode=open&_sid={}'

# CHANGE THIS
URL  =  'https://nas.quickconnect.to:65375/'
USER =  'admin'
PASS =  'password'
PATH =  'videos'

def login(url, id, pw):
    sid = 0
    response = requests.get(url+LOGIN_API.format(id, pw))
    response_dict = response.json()
    sid = response_dict['data']['sid']
    return sid

def download(url, path, file, sid):
    download_request = requests.get(url+DOWNLOAD_API.format(path, file, sid), stream=True)
    code = download_request.status_code
    total = download_request.headers.get('content-length')

    if total is None or code != 200:
        print("[*] El archivo no existe.")
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

if __name__ == '__main__':
    try:
        filename = str(input("\nWhat do you want to download? (Enter the exact file name, ie. file.exe)\n"))
        print("\n[*] Please, wait...\n")
        sid = login(URL, USER, PASS)
        download(url=URL, path=PATH, file=filename, sid=sid)
        logout(URL, LOGOUT_API)
    except KeyboardInterrupt:
        print("\n\n[*] Download interrupted!")