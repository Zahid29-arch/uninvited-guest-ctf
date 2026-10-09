#!/usr/bin/env python3
"""
Challenge Generation Script: Stage 3 (Locked Evidence)
Builds the encrypted forensic archive 'evidence_photos.zip' containing
investigation case notes, flag verification, and Juice Shop product images,
encrypted with Adrian Kessler's master password.
"""

import os
import pyzipper

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(SCRIPT_DIR, 'products')
OUTPUT_ZIP = os.path.join(SCRIPT_DIR, 'evidence_photos.zip')
PASSWORD = b'Kessler123!'

def build_zip():
    print(f"[*] Building encrypted archive: {OUTPUT_ZIP}")
    
    # Files to include in the evidence vault
    files_to_pack = [
        ('flag.txt', 'flag.txt'),
        ('case_notes.txt', 'case_notes.txt'),
        ('apple_juice.jpg', 'apple_juice.jpg'),
        ('banana_juice.jpg', 'banana_juice.jpg'),
        ('eggfruit_juice.jpg', 'eggfruit_juice.jpg'),
        ('green_smoothie.jpg', 'green_smoothie.jpg'),
        ('lemon_juice.jpg', 'lemon_juice.jpg'),
        ('orange_juice.jpg', 'orange_juice.jpg'),
        ('pomegranate_drink.jpg', 'pomegranate_drink.jpg'),
        ('quince.jpg', 'quince.jpg'),
        ('raspberry_juice.jpg', 'raspberry_juice.jpg'),
        ('sea_buckthorn_juice.jpg', 'sea_buckthorn_juice.jpg'),
    ]
    
    with pyzipper.AESZipFile(
        OUTPUT_ZIP,
        'w',
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(PASSWORD)
        for filename, arcname in files_to_pack:
            filepath = os.path.join(PRODUCTS_DIR, filename)
            if os.path.exists(filepath):
                zf.write(filepath, arcname=arcname)
                print(f" [+] Added: {arcname}")
            else:
                print(f" [!] Missing file: {filepath}")
                
    print(f"[+] Archive generated successfully with password: {PASSWORD.decode()}")
    print(f"[+] Size: {os.path.getsize(OUTPUT_ZIP)} bytes")

if __name__ == '__main__':
    build_zip()
