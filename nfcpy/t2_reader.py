"""
Successful handshake with UDP transport
- uses nfcpy UDP driver 
- doesnt work for custom handshake as originally hoped, crashes program -- since there is no way to add custom data to the handshake within the simulator.
"""

import nfc
import time

def discover_tag():
    # sense on udp in a loop.
    # repeat exchange calls to talk2 the tag

    from nfc.clf import RemoteTarget
    remote_target = RemoteTarget("106A")

    with nfc.ContactlessFrontend('udp:localhost:54321') as clf:
        print("Reader on udp:localhost:54321. Searching for a Tag...")

        while True:
            # sense() returns either a discovered RemoteTarget or None
            found_target = clf.sense(remote_target, iterations=5, interval=0.5)
            # try 5x, 0.5sec apart

            if found_target is None:
                print("No Tag found in this round, sleeping then retry...")
                time.sleep(2)
                continue

            print("Discovered a Tag!", found_target)

            # Now we attempt repeated exchange calls.
            # The first time, we pass None to see if the Tag wants to send anything first.
            try:
                tag_reply = clf.exchange(None, timeout=2.0)
                if tag_reply is None:
                    print("Tag didn't send anything initially. We'll send a command anyway.")
                else:
                    print("Tag said initially:", tag_reply)

                # Let’s do a small loop of commands
                for i in range(3):
                    command = b"Reader command #%d" % i
                    print("Sending to Tag:", command)
                    response = clf.exchange(command, timeout=3.0)
                    if response is None:
                        print("No response from Tag. Possibly deactivated.")
                        break
                    print("Tag responded:", response)

                # Done with our 3 commands. Optionally see if Tag has more to say:
                leftover = clf.exchange(None, timeout=2.0)
                if leftover:
                    print("Tag had some leftover message:", leftover)
                else:
                    print("No leftover message from Tag.")

            except nfc.clf.CommunicationError:
                print("CommunicationError: Tag link broke unexpectedly.")
            except nfc.clf.BrokenLinkError:
                print("BrokenLinkError: Tag link is gone.")

            print("Done interacting with Tag, restarting discovery...")
            time.sleep(2)

discover_tag()
