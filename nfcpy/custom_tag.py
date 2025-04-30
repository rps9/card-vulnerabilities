"""
Simpler tag emulator that emulates a raw tag with defined bytes.
- could be a workaround to the crashing issue in the t2 tags as it is more controllable,
however we found no way to simulate fully implement a more complex handshake.
"""

import nfc

def emulate_raw_tag():
    # just do clf.listen 

    # Prepare a LocalTarget for 106A (type A comm at 106kbps)
    local_target = nfc.clf.LocalTarget('106A')
    local_target.sens_res = b"\x01\x01" # means T2/T4 compatible
    local_target.sdd_res  = b"\x08\x01\x02\x03" # uid is 123: 8 indiciates 4 byte uid
    local_target.sel_res  = b"\x00" # SAK response byte (T2)

    with nfc.ContactlessFrontend('udp:localhost:54321') as clf:
        print("Raw Tag on udp:localhost:54321. Looping forever...")

        while True:
            activated = clf.listen(local_target, timeout=5.0)
            if not activated:
                print("No Reader discovered in 5s, re-listening.")
                continue

            print("Reader discovered me!")
            print("Activated target info:", activated)

            # handshake:
            # 1 Reader -> Tag command
            # 2 Tag sends a reply
            try:
                # i) wait for the Reader's request frame by passing None
                request = clf.exchange(None, timeout=3.0)
                if request is None:
                    print("No request from Reader, maybe they disconnected.")
                    continue
                print("Tag got request:", request)

                # ii) craft a response
                response = b"Hello from Tag side!"
                next_frame = clf.exchange(response, timeout=3.0)
                print("Tag got next frame (if any):", next_frame)

            except nfc.clf.CommunicationError as e:
                print("Tag CommunicationError:", e)
            except nfc.clf.BrokenLinkError as e:
                print("Tag BrokenLinkError:", e)

            print("Done one handshake, back to listening.\n")

emulate_raw_tag()
