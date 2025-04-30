"""
In this file we tried to do raw data byte transfer rather than specific tag type.
- much simpler compared to the t2 tags, but also doesn't work as it crashes any emulated tag when
attached to this reader.
- ideally we build a base on top of this but this functionality wasn't documented well enough to pursue.
- crashes the tag whenever both run together.
"""

import nfc
import time
from nfc.clf import RemoteTarget

# basic reader impl
def raw_reader():
    # Use sense to find the 106A target we setup,
    # do 1 request and wait for response

    rt_106A = RemoteTarget("106A")

    with nfc.ContactlessFrontend('udp:localhost:54321') as clf:
        print("Raw Reader on udp:localhost:54321. Looping forever...")

        while True:
            found = clf.sense(rt_106A, iterations=5, interval=0.5)
            if found is None:
                print("No Tag found re-trying sense()...")
                time.sleep(1)
                continue

            print("Found a Tag!", found) # tag found here

            try:
                # We send a request
                request = b"Hello from Reader!"
                print("Reader sending request:", request)

                response = clf.exchange(request, timeout=3.0) # send request
                print("Tag responded with:", response)

                second = clf.exchange(None, timeout=3.0)
                print("Tag's second frame:", second)

            except nfc.clf.CommunicationError as e:
                print("Reader CommunicationError:", e)
            except nfc.clf.BrokenLinkError as e:
                print("Reader BrokenLinkError:", e)

            print("Done handshake with Tag, going back to sense...\n")

raw_reader()
