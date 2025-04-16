'''
In this scenario, the running example will be a workplace that uses the mifare classic and is trying to be secure. 

Steps for protection:
    - the reader only expects certain unique cards that belong to each employee
    - scanning in is equivalent to clocking in, and scanning out is equivalent to clocking out
    - if someone has scanned in, that card cannot be used to scan in again unless it has been scanned out
    - if the card is used to scan in outside of regular work hours, it will not work
    - if the employee puts in for PTO or sick time, the card will not work
    - if a hypothetical attacker gets to the workplace before the worker and scans in, the system will alert that a non-employee
        scanned in
    - if the employee forgot to scan out the previous day, and can't get back in, the system will detect that they have been clocked
        in for a while and that it must have been an error on the employees part, not an attacker 
    - finally, when the employee scans out, it writes unique data to the card that it is expecting next time
    
Vulnerabilities/issues: 
    - If the employee leaves early, and an attacker clones their card after they leave work, the attacker then has a small window
        to enter the building undetected
        - this could be mitigated if we add a system for employees to say they are leaving work early, but this could become
            cumbersome
    - adding all of this custom logic could be expensive in the real world, so at that point it might not even be worth using the
        mifare classic 
'''

import pandas as pd
import os
import sys

# Adding the above directory and current directory to the path so we can use both
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, current_dir)
sys.path.insert(1, parent_dir)

from nfc_functions import dump_full_card, write_dump_to_card, write_to_block, read_block


def add_employee(card_uid, name):
    df = pd.read_csv("employee_database.csv")

    # Check if card_uid already exists
    if card_uid in df["card_uid"].values:
        print(f"[!] Employee with UID {card_uid} already exists.")
        return

    # Add new employee row
    new_entry = {
        "card_uid": card_uid,
        "name": name,
        "status": "OUT",       # Default: not clocked in
        "pto": False,          # Default: not on PTO
        "sick": False,         # Default: not sick
        "last_seen": ""        # No clock-in time yet
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("employee_database.csv", index=False)
    print(f"[+] Added employee '{name}' with card UID {card_uid}.")

add_employee(1234, "Ryan")
