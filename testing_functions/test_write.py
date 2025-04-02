import subprocess
import os

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
        return

    if preview and os.path.exists(filename):
        print("\n[*] Preview of first 10 blocks (160 bytes):\n")
        with open(filename, "rb") as f:
            data = f.read(160)  # First 10 blocks
            for i in range(0, len(data), 16):
                block = data[i:i+16]
                print(f"Block {i//16:02}: {' '.join(f'{b:02x}' for b in block)}")

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
    except subprocess.CalledProcessError as e:
        print("[!] Failed to write card.")
        print(e.stderr.decode())

def write_to_block(block_number, data, filename="full_card_dump.mfd"):
    dump_full_card(filename="full_card_dump.mfd")

    if len(data) > 16:
        print("[!] Data too long. Must be 16 bytes or fewer.")
        return

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
    
    write_dump_to_card(filename="full_card_dump.mfd")

if __name__ == "__main__":
    dump_full_card()
    #write_to_block(4, b"test")
