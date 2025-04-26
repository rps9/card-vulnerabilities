import csv
from nfc_functions import dump_full_card, read_block, write_block

LETTER_CYCLE = ["a", "b", "c", "d"]
DUMP_FILE = "full_card_dump.mfd"
DB_FILE = "data.csv"
COUNTER_BLOCK = 4

def load_db(path):
    data = {}
    try:
        with open(path, newline="") as f:
            for uid, letter in csv.reader(f):
                data[uid] = letter
    except FileNotFoundError:
        pass
    return data

def save_db(path, data):
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(data.items())


def counter_check():
    while True:
        print("Polling for card...")
        ## read from card
        if not dump_full_card(DUMP_FILE):
            return
        uid_blk = read_block(0, DUMP_FILE)
        letter_blk= read_block(COUNTER_BLOCK, DUMP_FILE)
        if not uid_blk or not letter_blk:
            print("Failed to read card")
            return

        uid = uid_blk[:4].hex()
        card_letter = letter_blk[:1].decode("utf-8", errors="ignore") or ""
        print(f"Card UID:    {uid}")
        print(f"Card Letter: '{card_letter}'")

        ## read from CSV database
        db = load_db(DB_FILE)

        ## compare
        if uid not in db:
            print("Access denied! No such card")
            return

        expected = db[uid]
        if card_letter != expected:
            print(f"⚠️⚠️⚠️⚠️⚠️ Clone detected! Database='{expected}' vs Card='{card_letter}'")
            print("police are on their way!")
            return
        print("✨ Access granted ✨ --  Welcome {uid}!".format(uid=uid))

        ## add one and record it both in card and database
        idx = LETTER_CYCLE.index(expected)
        next_letter = LETTER_CYCLE[(idx + 1) % len(LETTER_CYCLE)]
        db[uid] = next_letter
        save_db(DB_FILE, db)

        # write to card
        # print(f"[*] Writing '{next_letter}' to block {COUNTER_BLOCK}…")
        if not write_block(COUNTER_BLOCK, next_letter, DUMP_FILE):
            print("Write failed.")
            return

        # # confirm
        # time.sleep(0.5)
        # dump_full_card(DUMP_FILE)
        # confirm_blk = read_block(COUNTER_BLOCK, DUMP_FILE)
        # confirmed   = confirm_blk[:1].decode("utf-8", errors="ignore") or ""
        # print(f"[CONFIRM] Block {COUNTER_BLOCK} now reads: '{confirmed}'")

        input("Press enter to poll again...")

if __name__ == "__main__":
    counter_check()
