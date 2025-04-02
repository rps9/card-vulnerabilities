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

    if preview and os.path.exists(filename):
        print("\n[*] Preview of first 10 blocks (160 bytes):\n")
        with open(filename, "rb") as f:
            data = f.read(160)  # First 10 blocks (16 bytes per block)
            for i in range(0, len(data), 16):
                block = data[i:i+16]
                print(f"Block {i//16:02}: {' '.join(f'{b:02x}' for b in block)}")
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
    data = data.ljust(16, b'\x00')

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

def main():
    user_text = input("Enter text to write to block 4 (max 16 characters): ")
    text_bytes = user_text.encode("utf-8")
    
    print("\n--- Writing to Tag ---")
    if not write_to_block(4, text_bytes):
        print("[!] Write operation failed. Exiting.")
        return

    print("\nWaiting 5 seconds for the write operation to complete...")
    time.sleep(5)

    print("\n--- Reading from Tag ---")
    block_data = read_block(4)
    if block_data is not None:
        print("[+] Read block 4 data:")
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
