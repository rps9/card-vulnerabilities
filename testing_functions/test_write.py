import subprocess
import os
import time

from nfc_functions import dump_full_card, write_dump_to_card, write_to_block, read_block

block_to_write = 4

def main():
    user_text = input("Enter text to write to block "+str(block_to_write)+" (max 16 characters): ")
    text_bytes = user_text.encode("utf-8")
    text_bytes = user_text
    print("\n--- Writing to Tag ---")
    if not write_to_block(block_to_write, text_bytes):
        print("[!] Write operation failed. Exiting.")
        return

    print("\nWaiting 5 seconds for the write operation to complete...")
    time.sleep(5)

    print("\n--- Reading from Tag ---")
    block_data = read_block(block_to_write)
    if block_data is not None:
        print("[+] Read block "+str(block_to_write)+"  data:")
        print("Hex:", " ".join(f"{b:02x}" for b in block_data))
        try:
            # Decode and strip padding (null bytes)
            print("decoded text:", block_data.decode("utf-8").rstrip('\x00'))
        except UnicodeDecodeError:
            print("Text (raw):", block_data)
    else:
        print("[!] Could not read block data.")

if __name__ == "__main__":
    main()
