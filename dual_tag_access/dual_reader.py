"""
- The custom NFC reader application expects the anchor first then the key. 
- you only have 30sec after the first tag to show the second, otherwise it forgets everything

"""

import time
from nfc_functions import dump_full_card, read_block, pad_data
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def aes_ecb_decrypt(ciphertext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def wait_for_tag(block, timeout, filename):
    # once read_block returns someth, we know there is a tag present
    start_time = time.time()
    while time.time() - start_time < timeout: # only wait max 30 sec between tags

        if not dump_full_card(filename, preview=False):
            time.sleep(1) # wait 1s before poll again
            continue
        data = read_block(block, filename)
        if data is not None:
            return data
        time.sleep(1) # wait 1s before poll again
    return None

def dual_tag_read():
    print("present the SECONDARY tag")
    secondary_filename = "secondary_dump.mfd"
    secondary_block = 4
    key_data = wait_for_tag(secondary_block, timeout=30, filename=secondary_filename)
    
    if key_data is None:
        print("Timeout waiting for secondary tag. Aborting.")
        return
    
    # For demonstration, we assume that the key is stored as raw bytes;
    # if it's text, you can decode it.
    # Ensure the key is exactly 16 bytes (it should be if written correctly).
    if len(key_data) != 16:
        print("Unexpected key length from secondary tag. Aborting.")
        return
    key = key_data  # key is a 16-byte value.
    print("Secondary tag detected. Key (hex):", key.hex())

    # Now, wait for the primary tag within 30 seconds
    print("\nPlease present the PRIMARY tag (holds encrypted data) within 30 seconds.")
    primary_filename = "primary_dump.mfd"
    primary_block = 4
    ciphertext = wait_for_tag(primary_block, timeout=30, filename=primary_filename)
    
    if ciphertext is None:
        print("Timeout waiting for primary tag. Discarding secondary tag and restarting.")
        return

    if len(ciphertext) != 16:
        print("Unexpected ciphertext length from primary tag. Aborting.")
        return

    # Decrypt the primary tag data using the key from the secondary tag
    plaintext = aes_ecb_decrypt(ciphertext, key)
    try:
        decrypted_text = plaintext.decode("utf-8").rstrip('\x00')
    except Exception:
        decrypted_text = "<Undecodable data>"
    
    print("\nDecrypted Primary Tag Data:", decrypted_text)

def main():
    while True:
        dual_tag_read()
        print("\n--- Restarting Dual-Tag Read Process ---\n")
        # Sleep a moment before re-running (optional)
        time.sleep(2)

if __name__ == "__main__":
    main()