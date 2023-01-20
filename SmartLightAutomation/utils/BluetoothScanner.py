"""Link to the original source:
https://stackoverflow.com/questions/43418193/how-to-use-python-to-scan-and-communicate-with-ble-device-under-windows-environm

Documentation for bleak:
https://bleak.readthedocs.io/en/latest/
"""
import asyncio
from bleak import BleakScanner

class BluetoothScanner:
    """ Class for scanning for BLE devices. the run() method takes a list of MAC addresses to scan for.
     If any of the devices provided in the parameters are found, the method returns True. Otherwise, it returns False."""
    def __init__(self, target_addresses):
        self.target_addresses = target_addresses

    async def run(self):
        # Scan for devices for 20 seconds. The default is 5 seconds.
        devices = await BleakScanner.discover(timeout=15) 
        for d in devices:
            if d.address in self.target_addresses:
                print(f"Target device found with MAC address {d.address} found!")
                if d.address == "1E3B8B89-D2ED-5403-D2B2-03CDBE7F432B":
                    print("ARMAN tag found.")
                return True
        return False

if __name__ == "__main__":
    BLE_TAG_MAC = "1E3B8B89-D2ED-5403-D2B2-03CDBE7F432B"  # iTag
    #ALDO_TAG_MAC = "FF:FF:10:5B:54:94"   # Aldo tag

    scanner = BluetoothScanner(BLE_TAG_MAC)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scanner.run())
    loop.close()
