import nfc
try:
    with nfc.ContactlessFrontend('tty:USB0:pn532') as clf:
        print("Connected to:", clf.device)
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print("Detected:", tag)
except Exception as e:
    print("Error:", str(e))