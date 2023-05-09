---
title: Managing Credentials with Python
description: How to safely work with secret passwords in python scripts that are committed to source control
Date: 2021-05-15 21:00:00
tags: ["python"]
---



**I enjoy contributing to open-source, but I'd prefer to keep my _passwords_ to myself!** Python is a great glue language for automating tasks, and recently I've been using it to log in to my web server using SFTP and automate log analysis, file management, and software updates. The Python scripts I'm working on need to know my login information, but I want to commit them to source control and share them on GitHub so I have to be careful to use a strategy which minimizes risk of inadvertently leaking these secrets onto the internet.

**This post explores various options for managing credentials in Python scripts in public repositories.** There are many different ways to manage credentials with Python, and I was surprised to learn of some new ones as I was researching this topic. This post reviews the most common options, starting with the most insecure and working its way up to the most highly regarded methods for managing secrets.

## Plain-Text Passwords in Code

> **⚠️☠️ DANGER:** Never do this

You could put a password or API key directly in your python script, but even if you intend to remove it later there's always a chance you'll accidentally commit it to source control without realizing it, posing a security risk forever. This method is to be avoided at all costs!

```python
username = "myUsername"
password = "S3CR3T_P455W0RD"
logIn(username, password)
```

## Obfuscated Passwords in Code

> **⚠️☠️ DANGER:** Never do this

A _slightly_ less terrible idea is to obfuscate plain-text passwords by storing them as base 64 strings. You won't know the password just by seeing it, but anyone who has the string can easily decode it. Websites like https://www.base64decode.org are useful for this.

```py
"""Demonstrate conversion to/from base 64"""

import base64

def obfuscate(plainText):
    plainBytes = plainText.encode('ascii')
    encodedBytes = base64.b64encode(plainBytes)
    encodedText = encodedBytes.decode('ascii')
    return encodedText


def deobfuscate(obfuscatedText):
    obfuscatedBytes = obfuscatedText.encode('ascii')
    decodedBytes = base64.b64decode(obfuscatedBytes)
    decodedText = decodedBytes.decode('ascii')
    return decodedText
```

```py
original = "S3CR3T_P455W0RD"
obfuscated = obfuscate(original)
deobfuscated = deobfuscate(obfuscated)

print("original: " + original)
print("obfuscated: " + obfuscated)
print("deobfuscated: " + deobfuscated)
```

```
original: S3CR3T_P455W0RD
obfuscated: UzNDUjNUX1A0NTVXMFJE
deobfuscated: S3CR3T_P455W0RD
```

## Passwords in Plain Text Files

> **⚠️ WARNING:** This method is prone to mistakes. Ensure the text file is never committed to source control.

You could store username/password on the first two lines of a plain text file, then use python to read it when you need it.

```py
with open("secrets.txt") as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
    print(f"USERNAME={username}, PASSWORD={password}")
```


If the text file is in the repository directory you should modify `.gitignore` to ensure it's not tracked by source source control. There is a risk that you may forget to do this, exposing your credentials online! A better idea may be to place the secrets file outside your repository folder entirely.

💡 There are libraries which make this easier. One example is [Python Decouple](https://pypi.org/project/python-decouple/) which implements a lot of this logic gracefully and can even combine settings from multiple files (e.g., `.ini` vs `.env` files) for environments that can benefit from more advanced configuration options. See the notes below about helper libraries that environment variables and `.env` files

## Passwords in Python Modules

> **⚠️ WARNING:** This method is prone to mistakes. Ensure the secrets module is never committed to source control.

Similar to a plain text file not tracked by source control (ideally outside the repository folder entirely), you could store passwords as variables in a Python module then import it.

```py
from mySecrets import username, password
print(f"USERNAME={username}, PASSWORD={password}")
```

If your secrets file is in an obscure folder, you will have to add it to your path so the module can be found when importing.

```py
import sys
sys.path.append("C:/path/to/secrets/folder")

from mySecrets import username, password
print(f"USERNAME={username}, PASSWORD={password}")
```

Don't name your module `secrets` because the [secrets module](https://docs.python.org/3/library/secrets.html) is part of the standard library and that will likely be imported in stead.

## Passwords as Program Arguments

> **⚠️ WARNING:** This method may store plain text passwords in your command history.

This isn't a great idea because passwords are seen in plain text in the console and also may be stored in the command history. However, you're unlikely to accidentally commit passwords to source control.

```py
import sys
username = sys.argv[1]
password = sys.argv[2]
print(f"USERNAME={username}, PASSWORD={password}")
```

```bash
python test.py myUsername S3CR3T_P455W0RD
```

## Type Passwords in the Console

You could request the user to type their password in the console, but the characters would be visible as they're typed.

```py
# ⚠️ This code displays the typed password
password = input("Password: ")
```

Python has a [getpass module](https://docs.python.org/3/library/getpass.html) in its standard library made for prompting the user for passwords as console input. Unlike `input()`, characters are not visible as the password is typed.

```py
# 👍 This code hides the typed password
import getpass
password = getpass.getpass('Password: ')
```

## Extract Passwords from the Clipboard

This is an interesting method. It's fast and simple, but a bit quirky. Downsides are (1) it requires the password to be in the clipboard which may expose it to other programs, (2) it requires installation of a nonstandard library, and (3) it won't work easily in server environments.

Note that I trust [pyperclip](https://pypi.org/project/pyperclip/) more than [clipboard](https://pypi.org/project/clipboard/) (which is just [another developer wrapping pyperclip](https://github.com/terryyin/clipboard/blob/master/clipboard.py))

```bash
pip install pyperclip
```

Run after copying a password to the clipboard:

```py
import pyperclip
password = pyperclip.paste()
```

## Request Credentials with Tk

The [Tk graphics library](https://docs.python.org/3/library/tk.html) is a cross-platform graphical widget toolkit that comes with Python. A login window that collects username and password can be created programmatically and wrapped in a function for easily inclusion in scripts that otherwise don't have a GUI.

I find this technique particularly useful when the username and password are stored in a password manager.

<div class="text-center">

![](https://swharden.com/static/2021/05/15/tk-password-dialog.png)

</div>

```py
def getCredentials(defaultUser):
    """Request login credentials using a GUI."""
    import tkinter
    root = tkinter.Tk()
    root.eval('tk::PlaceWindow . center')
    root.title('Login')
    uv = tkinter.StringVar(root, value=defaultUser)
    pv = tkinter.StringVar(root, value='')
    userEntry = tkinter.Entry(root, bd=3, width=35, textvariable=uv)
    passEntry = tkinter.Entry(root, bd=3, width=35, show="*", textvariable=pv)
    btnClose = tkinter.Button(root, text="OK", command=root.destroy)
    userEntry.pack(padx=10, pady=5)
    passEntry.pack(padx=10, pady=5)
    btnClose.pack(padx=10, pady=5, side=tkinter.TOP, anchor=tkinter.NE)
    root.mainloop()
    return [uv.get(), pv.get()]
```

```py
username, password = getCredentials("user@site.com")
```

## Manage Passwords with a Keyring

The [keyring package](https://pypi.org/project/keyring/) provides an easy way to access the system's keyring service from python. On MacOS it uses [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29), on Windows it uses the [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker), and on Linux it can use KDE's [KWallet](https://en.wikipedia.org/wiki/KWallet) or GNOME's [Secret Service](https://specifications.freedesktop.org/secret-service/latest).

Downsides of keyrings are (1) it requires a nonstandard library, (2) implementation may be OS-specific, (3) it may not function easily in cloud environments.

```bash
pip install keyring
```

```py
# store the password once
import keyring
keyring.set_password("system", "myUsername", "S3CR3T_P455W0RD")
```

```py
# recall the password at any time
import keyring
password = keyring.get_password("system", "myUsername")
```

## Passwords in Environment Variables

Environment variables are one of the better ways of managing credentials with Python. There are many articles on this topic, including Twilio's [How To Set Environment Variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) and [Working with Environment Variables in Python](https://www.twilio.com/blog/environment-variables-python). Environment variables are one of the preferred methods of credential management when working with cloud providers.

<div class="text-center">

![](https://swharden.com/static/2021/05/15/environment-variables.png)

</div>

Be sure to restart your console session after editing environment variables before attempting to read them from within python.

```py
import os
password = os.getenv('demoPassword')
```

There are many helper libraries such as [python-dotenv](https://pypi.org/project/python-dotenv/) and [Python Decouple](https://pypi.org/project/python-decouple/) which can use local `.env` files to dynamically set environment variables as your program runs. As noted in previous sections, when storing passwords in plain-text in the file structure of your repository be extremely careful not to commit these files to source control!


Example `.env` file:
```txt
demoPassword2=superSecret
```

The `dotenv` package can load `.env` variables as environment variables when a Python script runs:

```py
import dotenv
dotenv.load_dotenv()
password2 = os.getenv('demoPassword2')
print(password2)
```

## Additional Resources
* [Using .env Files for Environment Variables in Python Applications](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1)
* [Environment Variables vs. Secrets In Python](https://www.activestate.com/blog/python-environment-variables-vs-secrets/)
* [How To Set Environment Variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)
* [Working with Environment Variables in Python](https://www.twilio.com/blog/environment-variables-python)
* [How to Set and Get Environment Variables in Python](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5)
* [python-dotenv](https://pypi.org/project/python-dotenv/) reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the 12-factor principles.
* [Python Decouple](https://pypi.org/project/python-decouple/) helps you to organize your settings so that you can change parameters without having to redeploy your app.

_How do you manage credentials in Python? If you wish to share feedback or a creative method you use that I haven't discussed above, send me an email and I can include your suggestions in this document._