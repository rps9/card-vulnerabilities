"""
Import as nfc_functions into the file so we only have the one master script with all the NFC tag functionality.
- Keep your code in the same folder so python can find this file.

from nfc_functions import dump_full_card, write_dump_to_card, write_to_block, read_block, read_blocks, read_all_blocks, print_dump_contents
or just import the whole file:
import nfc_functions, then you have to calls as nfc_functions.dump_full_card()
"""

import subprocess
import os
import time

def dump_full_card(filename="full_card_dump.mfd", preview=True):
    print("[*] Starting card dump using nfc-mfclassic...")
    
    try:
        result = subprocess.run(
            ["nfc-mfclassic", "r", "a", "u", filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("[+] Dump successful. File saved as:", filename)
    except subprocess.CalledProcessError as e:
        print("[!] Failed to dump card.")
        print(e.stderr.decode())
        return False

    return True

def write_dump_to_card(filename="full_card_dump.mfd"):
    print("[*] Writing modified dump back to card...")
    try:
        subprocess.run(
            ["nfc-mfclassic", "w", "a", "u", filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("[+] Card written successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("[!] Failed to write card.")
        print(e.stderr.decode())
        return False

def write_to_block(block_number, data, filename="full_card_dump.mfd"):
    # Dump the current card contents to a file
    if not dump_full_card(filename):
        return False

    if len(data) > 16:
        print("[!] Data too long. Must be 16 bytes or fewer.")
        return False

    # Pad data to 16 bytes
    data = pad_data(data, 16)

    print(f"[*] Writing to block {block_number} in {filename}...")

    try:
        with open(filename, "r+b") as f:
            f.seek(block_number * 16)
            f.write(data)
        print("[+] Block modified successfully.")
    except Exception as e:
        print("[!] Failed to write to file:", str(e))
        return False

    if not write_dump_to_card(filename):
        return False
    return True


def read_block(block_number, filename="full_card_dump.mfd"):
    """
    Returns a 16 byte block of data
    """
    # Dump the current card contents
    if not dump_full_card(filename):
        return None
    try:
        with open(filename, "rb") as f:
            f.seek(block_number * 16)
            data = f.read(16)
            return data
    except Exception as e:
        print("[!] Failed to read block:", str(e))
        return None


def read_blocks(start_block, num_blocks, filename="full_card_dump.mfd"):
    """
    Returns a list of 16 byte blocks
    """
    if not dump_full_card(filename):
        return None
    blocks = []
    try:
        with open(filename, "rb") as f:
            f.seek(start_block * 16)
            for _ in range(num_blocks):
                block = f.read(16)
                if len(block) < 16:
                    break
                blocks.append(block)
        return blocks
    except Exception as e:
        print("[!] Failed to read blocks:", str(e))
        return None

def read_all_blocks(filename="full_card_dump.mfd"):
    if not dump_full_card(filename, preview=False):
        return None
    try:
        with open(filename, "rb") as f:
            data = f.read()
        num_blocks = len(data) // 16
        blocks = []
        print("\n[*] Full card dump:")
        for i in range(num_blocks):
            block = data[i*16:(i+1)*16]
            decoded = decode_block_data(block)
            print(f"Block {i:02}: {' '.join(f'{b:02x}' for b in block)} | Decoded: {decoded}")
            blocks.append(block)
        return blocks
    except Exception as e:
        print("[!] Failed to read entire dump:", e)
        return None


def print_dump_contents(filename="full_card_dump.mfd"):
    """
    Prints all blocks in the file
    returns a list of 16 byte blocks
    """
    if not dump_full_card(filename, preview=False):
        return None
    try:
        with open(filename, "rb") as f:
            data = f.read()
        num_blocks = len(data) // 16
        blocks = []
        print("\n[*] Full card dump:")
        for i in range(num_blocks):
            block = data[i*16:(i+1)*16]
            decoded = decode_block_data(block)
            print(f"Block {i:02}: {' '.join(f'{b:02x}' for b in block)} | Decoded: {decoded}")
            blocks.append(block)
        return blocks
    except Exception as e:
        print("[!] Failed to read entire dump:", e)
        return None


# ===== Helper functions =====

# just decodes block data by removing the null bytes
def decode_block_data(data):
    try:
        return data.decode("utf-8").rstrip('\x00')
    except UnicodeDecodeError:
        return "BAD DATA"

# pad data to 16 bytes or whatever u specify (probably going to be 16)
# -- write_to_block already does this so only used if directly modifying a dumped file
def pad_data(data, block_size=16):
    if len(data) > block_size:
        return data[:block_size] # trunc if too long
    return data.ljust(block_size, b'\x00')
