""" 
This function will use a counter to prevent cloneing the card. 
Each time a card is scanned to the system, the system will check if the counter in database macthes the one in card
And it will add one to the counter in database and write the new counter to the card.
If it finds out the both counter are different, it will sent an alarm message. 
"""
from nfc_functions import dump_full_card, write_dump_to_card, write_to_block, read_block

import csv

def counter_check(filename="full_card_dump.mfd"):
    ## read from card
    if not dump_full_card(filename):
        return None
    try:
        with open(filename, "rb") as f:
            f.seek(16)  # assume the  block 0 is the uid
            uid = f.read(4)
            card_uid = uid.hex()
            f.seek(16*6)  # assume the block 5 is the count
            count = f.read(16)
            card_count = int.from_bytes(count, 'big')
    except Exception as e:
        print("[!] Failed to read block:", str(e))
        return None

    ## read from CSV database
    database = "data.csv"
    data = {}
    try:
        with open(database, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    id_str, number = row
                    data[id_str] = int(number)
    except FileNotFoundError:
        print("[!] Database file not found.")
        return None

    ## compare
    if card_uid not in data:
        print("Access denied! No such card")
        return None
    if card_count != data[card_uid]:
        print("Card getting cloned!")
        return None
    else:
        print("Access granted successfully")

    ## add one and record it both in card and database
    data[card_uid] += 1

    with open(database, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for id_str, number in data.items():
            writer.writerow([id_str, number])

    card_count += 1
    block_count = card_count.to_bytes(16, 'big')
    write_to_block(6, block_count)
    return None
