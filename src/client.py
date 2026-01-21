import requests
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from tqdm import tqdm
import time

class SynologyClient:
    def __init__(self, url: str, user: str, password: str, download_path: str):
        self.url = url
        self.user = user
        self.password = password
        self.download_path = Path(download_path)
        self.sid: Optional[str] = None
        self.session = requests.Session()

    def login(self) -> bool:
        """Authenticates with the Synology NAS."""
        try:
            params = {
                'api': 'SYNO.API.Auth',
                'version': 3,
                'method': 'login',
                'account': self.user,
                'passwd': self.password,
                'session': 'FileStation',
                'format': 'cookie'
            }
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success'):
                self.sid = data['data']['sid']
                return True
            else:
                print(f"Login failed: {data}")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def list_files(self, remote_path: str) -> Dict[int, str]:
        """Lists files in a remote directory, excluding subdirectories."""
        if not self.sid:
            raise Exception("Not logged in")

        # Ensure remote path starts with /
        if not remote_path.startswith("/"):
            remote_path = "/" + remote_path

        params = {
            'api': 'SYNO.FileStation.List',
            'version': 2,
            'method': 'list',
            'additional': '',
            'folder_path': remote_path,
            '_sid': self.sid
        }
        
        try:
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                print(f"List files failed: {data}")
                return {}

            files = data['data']['files']
            file_map = {}
            index = 1
            for file in files:
                if not file.get('isdir'):
                    file_map[index] = file['name']
                    index += 1
            
            return file_map
        except Exception as e:
            print(f"List files error: {e}")
            return {}

    def download_file(self, remote_path: str, filename: str) -> bool:
        """Downloads a file with a progress bar."""
        if not self.sid:
            raise Exception("Not logged in")
            
        full_remote_path = f"/{remote_path.strip('/')}/{filename}"
        local_file_path = self.download_path / filename

        # Create download directory if it doesn't exist
        self.download_path.mkdir(parents=True, exist_ok=True)

        params = {
            'api': 'SYNO.FileStation.Download',
            'version': 2,
            'method': 'download',
            'path': full_remote_path,
            'mode': 'open',
            '_sid': self.sid
        }

        try:
            with self.session.get(self.url, params=params, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(local_file_path, 'wb') as f, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        bar.update(size)
            return True
        except Exception as e:
            print(f"Download error: {e}")
            # Clean up partial file
            if local_file_path.exists():
                local_file_path.unlink()
            return False

    def logout(self):
        """Logs out from the session."""
        if not self.sid:
            return

        try:
            params = {
                'api': 'SYNO.API.Auth',
                'version': 1,
                'method': 'logout',
                'session': 'FileStation'
            }
            self.session.get(self.url, params=params)
            self.sid = None
        except Exception:
            pass
