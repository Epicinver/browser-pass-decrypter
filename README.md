# Simple password file decryption.
This is a simple Python repository designed to decrypt Firefox's saved login data files (logins.json & key4.db) as well as Chrome's Login Data file.
It was created quickly but is straightforward to use.

# Requirements

Python 3.6 or newer

Python package: cryptography

# Installation on Windows
Open the terminal in both folders, and type "pip install cryptography"
Then, simply just open the folder for your browser, then open the .exe
(You may need to open CMD and type "python LETTER:\PATH\TO\DECRYPTOR\BROWSER\SOURCE_CODE\decrypt.py")

# Installing on Linux/Mac OS (experimental)

Follow the same installation steps as for Windows to install the cryptography package.

Run the decryptor script using Python:
python decrypt.py
Note: Decryption might not work perfectly due to system differences and dependencies.

# Notes

Firefox must be installed on the system for nss3.dll (or equivalent libraries on Linux/macOS) to decrypt Firefox passwords.

The tool only works with your own data; unauthorized access is illegal and unethical.

Chrome decryption requires different handling and is only partially supported here.
