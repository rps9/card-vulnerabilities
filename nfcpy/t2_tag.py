"""
- works for basic handshake but send_rsp_recv_cmd fails as it seems to not be 
implemented in the source code fully to work with the UDP simulator, we would need actual hardware.
"""

import nfc

def emulate_fake_type2():

    # Added read block command (0x30)
    # return ascii block for b0 (doesn't work)

    local_target = nfc.clf.LocalTarget("106A") # same params as custom_tag
    local_target.sens_res = b"\x01\x01"
    local_target.sdd_res  = b"\x08\x01\x02\x03"
    local_target.sel_res  = b"\x00"

    with nfc.ContactlessFrontend('udp:localhost:54321') as clf:
        print("Fake Type2 Tag on udp:localhost:54321. Loop forever...")

        while True:
            activated = clf.listen(local_target, timeout=10.0)
            if not activated:
                print("No Reader discovered in 10s. Re-listening...")
                continue

            print("Reader discovered me!")
            print("Activated target info:", activated)

            next_cmd = None

            while True:
                try:
                    # wait for the next T2 command from the Reader
                    if next_cmd is None:

                        if hasattr(activated, 'tt2_cmd') and activated.tt2_cmd: # check if tt2_cmd is set
                            next_cmd = activated.tt2_cmd # use it
                        else:
                            # otherwise, wait for a command
                            next_cmd = clf.send_rsp_recv_cmd(activated, b"", timeout=2.0)
                            if next_cmd is None:
                                print("No T2 command from Reader, done.")
                                break
                    else:
                        pass # already have a pending command

                    # Code never reaches here, as send_rsp_recv_cmd fails
                    # may be completely wrong below -- no response is able to be recieved

                    print(f"Tag sees T2 command: {next_cmd.hex()}") 

                    # The minimal Type 2 read command is 0x30 + block number
                    if len(next_cmd) == 2 and next_cmd[0] == 0x30: # 30 is read command
                        block_no = next_cmd[1]
                        if block_no == 0x00:
                            block_data = b"Hello TagBlock0!"

                        # Respond
                        print(f"Tag responding with block {block_no}, data={block_data}")
                        next_cmd = clf.send_rsp_recv_cmd(activated, block_data, timeout=2.0)
                        if next_cmd is None:
                            print("No follow-up command, done with T2.")
                            break

                except nfc.clf.CommunicationError as e:
                    print("Tag CommunicationError:", e)
                    break
                except nfc.clf.BrokenLinkError as e:
                    print("Tag BrokenLinkError:", e)
                    break

            print("Done handling T2 commands, back to listen.\n")

emulate_fake_type2()
