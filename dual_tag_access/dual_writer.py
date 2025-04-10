"""
This script uses two NFC tags that are both easily clonable (thus insecure)
- By requiring two tags - one tag is the encrypted data and the other is the anchor or encryption key
- So cloning of any one tag does not give access -- you would need to clone both AND know the correct order to sign in. 
"""

import time
import os
from nfc_functions import write_to_block, pad_data
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# for now it's just a basic AES-ECB enc
def aes_ecb_encrypt(plaintext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def main():
    print("=== Dual-Tag Writer ===")
    
    data_pt = input("Enter data (max 16 characters): ").strip() # plaintext
    
    # convert to bytes
    data_bytes = data_pt.encode("utf-8")
    
    data_padded = pad_data(data_bytes, 16)

    # the enryption key is currently just random 16 bytes generated
    key_rand = os.urandom(16) # random 16 bytes
    
    # encrypt the primary data using AES-ECB with key from secondary tag.
    ciphertext = aes_ecb_encrypt(data_padded, key_rand)
    
    # write ciphertext to the primary tag (using onlys block 4 for now)
    input("\nPlace the PRIMARY tag on the writer and press Enter to write")
    if write_to_block(4, ciphertext):
        print("Primary tag written successfully.")
    else:
        print("Error writing primary tag.")
        return
    
    time.sleep(2)
    
    #  write dec key to secondary tag
    input("\nPlace the SECONDARY tag on the writer and press Enter to write")
    if write_to_block(4, key_rand):
        print("Secondary tag written successfully.")
    else:
        print("Error writing secondary tag.")

if __name__ == "__main__":
    main()
