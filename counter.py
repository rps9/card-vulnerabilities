""" 
This function will use a counter to prevent cloneing the card. 
Each time a card is scanned to the system, the system will check if the counter in database macthes the one in card
And it will add one to the counter in database and write the new counter to the card.
If it finds out the both counter are different, it will sent an alarm message. 
"""
from nfc_functions import dump_full_card, write_dump_to_card, write_to_block, read_block

def counter_check(filename="full_card_dump.mfd"):
    ## read from card
    if not dump_full_card(filename):
        return None
    try:
        with open(filename, "rb") as f:
            f.seek(16)  # assume the first block is the uid
            uid = f.read(4)
            card_uid=uid.hex()
            f.seek(32)  # assume the second block is the count
            count = f.read(16)
            card_count=int.from_bytes(count, 'big')
    except Exception as e:
        print("[!] Failed to read block:", str(e))
        return None
    ## read from database
    database="data.txt"
    data = {}
    with open(database, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                id_str = parts[0]
                number = int(parts[1])
                data[id_str] = number 
    ## compare
    if card_uid not in data:
        print("Accessd denied! No such card")
        return None
    if card_count != data[card_uid]:
        print("Card getting cloned!")
        return None
    else:
        print("Access granted successfully")
    
    ## add one and record it both in card and database
    data[card_uid]+=1

    with open("data.txt", "w") as file:
        for id_str, number in data.items():
            file.write(f"{id_str:<10} {number}\n")
    
    card_count+=1
    block_count=card_count.to_bytes(16, 'big')
    write_to_block(1,block_count)
    return None
    
