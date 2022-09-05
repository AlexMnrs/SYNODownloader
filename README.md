# 1.0.0

This application allows you to download files from a Synology NAS, specifically from the FileStation file management tool (tested with the DS218Play).

### Step 1: Install the requirements

```
$ pip install -r requirements.txt
```

### Step 2: Set your credentials

The credentials.py file contains the NAS access information. Change it to your own:

```
URL = 'https://nas.quickconnect.to:65375/webapi/entry.cgi'
USER = 'admin
PASS = 'password
PATH = 'videos'
```

### Step 3: Run the program

```
python main.py
```

### Known problems

- When the download finishes the percentage is not 100%.
