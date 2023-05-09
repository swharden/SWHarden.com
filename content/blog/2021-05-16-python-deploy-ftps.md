---
title: Deploy a Website with Python and FTPS
description: How to use Python, keyring, and TLS to securely deploy website content using FTP (FTPS)
Date: 2021-05-16 11:00:00
tags: ["python"]
---

**Python can be used to securely deploy website content using FTPS.** Many people have used a FTP client like [FileZilla](https://en.wikipedia.org/wiki/FileZilla) to drag-and-drop content from their local computer to a web server, but this method requires manual clicking and is error-prone. If you write a script to accomplish this task it lowers the effort barrier for deployment (encouraging smaller iterations) and reduces the risk you'll accidentally do something unintentional (like deleting an important folder by accident).

**This post reviews how I use Python, keyring, and TLS to securely manage login credentials and deploy builds from my local computer to a remote server using FTP.** The strategy discussed here will be most useful in servers that use the [LAMP stack](https://en.wikipedia.org/wiki/LAMP_(software_bundle)), and it's worth noting that .NET and Node have their own deployment paradigms. I hope you find the code on this page useful, but you should carefully review your deployment script and create something specific to your needs. Just as you could accidentally delete an important folder using a graphical client, an incorrectly written deployment script could cause damage to your website or leak secrets.

## Use Keyring to Manage Your Password

I recently wrote about [several ways to manage credentials with Python](https://swharden.com/blog/2021-05-15-python-credentials/). 

In these examples I will use the [keyring package](https://pypi.org/project/keyring/) to store and recall my FTP password securely.

```bash
pip install keyring
```

### Storing Credentials

Store your password using an interactive interpreter to ensure you don't accidentally save it in a plain text file somewhere. This only needs to be done once.

```py
>>> import keyring
>>> keyring.set_password("system", "me@swharden.com", "P455W0RD")
```

### Recalling Credentials

```py
import keyring
hostname = "swharden.com"
username = "me@swharden.com"
password = keyring.get_password("system", username)
```

## FTP vs. FTPS vs. SFTP

**FTP was not designed to be a secure - it transfers login credentials in plain text!** Traditionally FTP in Python was achieved using `ftplib.FTP` from the standard library, but logging-in using this protocol allows anyone sniffing traffic on your network to capture your password. In Python 2.7 `ftplib.FTP_TLS` was added which adds transport layer security to FTP (FTPS), improving protection of your login credentials. 

```py
# ⚠️ This is insecure (password transferred in plain text)
from ftplib import FTP
with FTP(hostname, username, password) as ftp:
    print(ftp.nlst())
```

```py
# 👍 This is better (password is encrypted)
from ftplib import FTP_TLS
with FTP_TLS(hostname, username, password) as ftps:
    print(ftps.nlst())
```

By default `ftplib.FTP_TLS` only encrypts the username and password. You can call `prot_p()` to encrypt all transferred data, but in this post I'm only interested in encrypting my login credentials.

FTP over SSL (FTPS) is different than FTP over SSH (SFTP), but both use encryption to transfer usernames and passwords, making them superior to traditional FTP which transfers these in plain text.

## Recursively Delete a Folder with FTP

This method deletes each of the contents of a folder, then deletes the folder itself. If one of the contents is a subfolder, it calls itself. This example uses modern Python practices, favoring `pathlib` over `os.path`.

Note that I define the remote path using `pathlib.PurePosixPath()` to ensure it's formatted as a unix-type path since my remote server is a Linux machine.

```py
import ftplib
import pathlib

def removeRecursively(ftp: ftplib.FTP, remotePath: pathlib.PurePath):
    """
    Remove a folder and all its contents from a FTP server
    """

    def removeFile(remoteFile):
        print(f"DELETING FILE {remoteFile}")
        ftp.delete(str(remoteFile))

    def removeFolder(remoteFolder):
        print(f"DELETING FOLDER {remoteFolder}/")
        ftp.rmd(str(remoteFolder))

    for (name, properties) in ftp.mlsd(remotePath):
        fullpath = remotePath.joinpath(name)
        if name == '.' or name == '..':
            continue
        elif properties['type'] == 'file':
            removeFile(fullpath)
        elif properties['type'] == 'dir':
            removeRecursively(ftp, fullpath)

    removeFolder(remotePath)

if __name__ == "__main__":
    remotePath = pathlib.PurePosixPath('/the/remote/folder')
    with ftplib.FTP_TLS("swharden.com", "scott", "P455W0RD") as ftps:
        removeFolder(ftps, remotePath)
```

## Recursively Upload a Folder with FTP

This method recursively uploads a local folder tree to the FTP server. It first creates the folder tree, then uploads all files individually. This example uses modern Python practices, favoring `pathlib` over `os.walk()` and `os.path`.

Like before I define the remote path using `pathlib.PurePosixPath()` since the server is running Linux, but I can use `pathlib.Path()` for the local path and it will auto-detect how to format it based on which system I'm currently running on.

```py
import ftplib
import pathlib

def uploadRecursively(ftp: ftplib.FTP, remoteBase: pathlib.PurePath, localBase: pathlib.PurePath):
    """
    Upload a local folder to a remote path on a FTP server
    """

    def remoteFromLocal(localPath: pathlib.PurePath):
        pathParts = localPath.parts[len(localBase.parts):]
        return remoteBase.joinpath(*pathParts)

    def uploadFile(localFile: pathlib.PurePath):
        remoteFilePath = remoteFromLocal(localFile)
        print(f"UPLOADING FILE {remoteFilePath}")
        with open(localFile, 'rb') as localBinary:
            ftp.storbinary(f"STOR {remoteFilePath}", localBinary)

    def createFolder(localFolder: pathlib.PurePath):
        remoteFolderPath = remoteFromLocal(localFolder)
        print(f"CREATING FOLDER {remoteFolderPath}/")
        ftp.mkd(str(remoteFolderPath))

    createFolder(localBase)
    for localFolder in [x for x in localBase.glob("**/*") if x.is_dir()]:
        createFolder(localFolder)
    for localFile in [x for x in localBase.glob("**/*") if not x.is_dir()]:
        uploadFile(localFile)

if __name__ == "__main__":
    localPath = pathlib.Path(R'C:\my\project\folder')
    remotePath = pathlib.PurePosixPath('/the/remote/folder')
    with ftplib.FTP_TLS("swharden.com", "scott", "P455W0RD") as ftps:
        uploadRecursively(ftps, remotePath, localPath)
```

## Minimize Disruption by Renaming

Because walking remote folder trees deleting and upload files can be slow, this process may be disruptive to a website with live traffic. For low-traffic websites this isn't an issue, but as traffic increases (or the size of the deployment increases) it may be worth considering how to achieve the swap faster.

An improved method of deployment could involve uploading the new website to a temporary folder, switching the names of the folders, then deleting the old folder. There is brief downtime between the two FTP rename calls.

```py
remotePath = "/live"
remotePathNew = "/live-new"
remotePathOld = "/live-old"
localPath = R"C:\dev\site\live"

upload(localPath, remotePathNew)
ftpRename(remotePath, remotePathOld)
ftpRename(remotePathNew, remotePath)
delete(remotePathOld)
```

Speed could be improved by handling the renaming with a shell script that runs on the server. This would require some coordination to execute though, but is worth considering. It could be executed by a HTTP endpoint.

```bash
mv /live /live-old;
mv /live-new /live;
rm -rf /live-old;
```

## Deploy a React App with FTP and Python

**You can automate deployment of a React project using Python and FTPS.** After [creating a new React app](https://reactjs.org/docs/create-a-new-react-app.html) add a `deploy.py` in the project folder that uses FTPS to upload the build folder to the server, then edit your project's `package.json` to add `predeploy` and `deploy` commands.

```json
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "predeploy": "npm run build",
    "deploy" : "python deploy.py"
  },
```

Then you can create a production build and deploy with one command:

```
npm run deploy
```

## Consider Using Git to Deploy Content

This post focused on how to automate uploading local content to a remote server using FTP, but don't overlook the possibility that this may not be the best method for deployment for your application.

**You can maintain a website as a git repository and use `git pull` on the server to update it.** GitHub Actions can be used to trigger the pull step automatically using an HTTP endpoint. If this method is available to you, it should be strongly considered.

This method is very popular, but it (1) requires `git` to be on the server and (2) requires all the build tools/languages to be available on the server if a build step is required. I'm reminded that [only SiteGround's most expensive shared hosting plan](https://www.siteground.com/shared-hosting-features.htm) even has `git` available at all. 

## Resources
* [ftplib.FTP_TLS official documentation](https://docs.python.org/2/library/ftplib.html#ftplib.FTP_TLS)
* [SFTP vs. FTPS: What's the Best Protocol for Secure FTP?](https://www.goanywhere.com/blog/2011/10/20/sftp-ftps-secure-ftp-transfers)
* [Managing Credentials with Python](https://swharden.com/blog/2021-05-15-python-credentials/)
* [Create React App: Deployment](https://create-react-app.dev/docs/deployment/) is useful but never mentions FTP
* [ftp-deploy](https://www.npmjs.com/package/ftp-deploy) is a Node.js package to help with deploying code using FTP
