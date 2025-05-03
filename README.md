# Card-Vulnerabilities
EC521 Project

Ryan, Alan, James, Jerry


In this repository we study the vulnerabilities of MIFARE Classic cards and offer some potential protections. These cards are trivial to clone so we offer 3 practical mitigations that make it more difficult for an attacker.

None of these mitigations provide perfect security (the only real fix is migrating to
DESFire EV1/EV3 or some other encrypted card), but each mitigation blocks a different attack surface and strategy.

# Vulnerabilities

- MIFARE Classic cards use Crypto-1, a proprietary cipher that is completely broken.
- You need real encryption (ie AES) for a secure card as that would have non-clonable blocks because the blocks are hidden from cloners. 
- The main issue is there are **no hidden blocks** in MIFARE Classic cards, so any data written to the card can be read by a cloner.
- We tackle these vulnerabilities to mitigate the concern of cloning.

# Mitigations

## Mitigation 1: Counter 

`counter_write/`

Store a counter (A->B->C->D->A...) in a single data block and in a server DB. Each valid tap must show the next letter. A cloned card will have a letter that does not match the DB, and is rejected. Each tap writes the next letter to the card and the server so a cloned card will get out of sync after the next legit tap.

## Mitigation 2: Clock in / Clock out

`clock_in_and_out/`

Treat every tap as an entry/exit like clocking in and out. You cannot cannot tap in someone already "clocked in" until that person has clocked out. A cloned card would be the same person clocking in twice, creating an alarm that the card has been cloned. 

## Mitigation 3: Dual Tags

`dual_tag_access/`

Requrire a two factor tag authentication, with both MIFARE Classics, but one goes in your wallet and one on your keychain. This is mitigation mainly that it is less likely to lose both or have both tags be stolen. 

Writing the tags:
1. Generate random 16-byte key K.
2. Encrypt user data P with AES-ECB, C = AES_ECB(P, K).
3. Write C to primary tag (wallet).
4. Write K to secondary tag (keychain). 

Reader:
- demand both tags to be present to decrypt data
- no encrypted data is stored server side as encryption key is on the second tag

![image](https://github.com/user-attachments/assets/e47be977-4fe2-4d30-a4aa-c44c8193f6bc)


# Usage 

- We use a [PN532](https://www.aliexpress.us/item/3256805076433294.html?spm=a2g0o.order_list.order_list_main.5.72d51802xzONmF&gatewayAdapt=glo2usa) NFC reader/writer to read and write the MIFARE Classic cards.
- Repo uses the [nfc-mfclassic](https://www.mankier.com/1/nfc-mfclassic) toolset from [libnfc](https://github.com/nfc-tools/libnfc). Ensure it is installed before running the python code.
- Use the main `nfc_functions.py` to run all the tests. Replace the `counter_write/counter.py` below with whatever function you are trying to run. This way subfolders can access the main nfc functions file.
```sh
PYTHONPATH=. python3 counter_write/counter.py
```

# References

- [Making the Best of Mifare Classic](https://www.cs.ru.nl/~wouter/papers/2008-thebest.pdf)  
- [Hardening NFC tags for authentication – Security StackExchange](https://security.stackexchange.com/questions/234637/hardening-nfc-tags-for-authentication)
- [How do NFC tags prevent copying? – Security StackExchange](https://security.stackexchange.com/questions/63483/how-do-nfc-tags-prevent-copying)
- [Is it possible to provide security in passive RFID tags? – Electronics StackExchange](https://electronics.stackexchange.com/questions/103741/is-it-possible-to-provide-security-in-passive-rfid-tags)
- [Prevent NFC tag cloning – Arduino Forum](https://forum.arduino.cc/t/prevent-nfc-tag-cloning/276786)
- [NFC Tag Authentication Explained – Seritag](https://seritag.com/learn/using-nfc/nfc-tag-authentication-explained)
