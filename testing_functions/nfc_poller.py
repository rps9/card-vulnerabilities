from nfc_functions import dump_full_card, read_block, print_dump_contents

def continuous_poll(block=4, poll_interval=2, filename="full_card_dump.mfd"):
    try:
        while True:
            print("\n--- Updating Card Dump ---")
            dump_full_card(filename, preview=False)
            
            print("--- Reading from Tag ---")
            # block_data = read_block(block, filename)
            # if block_data is not None:
            #     print("[+] Read block", block, "data:")
            #     print("Hex:", " ".join(f"{b:02x}" for b in block_data))
            #     try:
            #         # Decode and strip padding (null bytes)
            #         print("Decoded text:", block_data.decode("utf-8").rstrip('\x00'))
            #     except UnicodeDecodeError:
            #         print("Text (raw):", block_data)
            # else:
            #     print("[!] Could not read block data")

            print_dump_contents(filename)
            
            print("Press enter to poll again")
            input()
    except KeyboardInterrupt:
        print("\nexit poller")

if __name__ == "__main__":
    continuous_poll()
