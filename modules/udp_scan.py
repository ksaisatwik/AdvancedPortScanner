# =========================
# FILE: modules/udp_scan.py
# =========================

from scapy.all import IP, UDP, sr1
from colorama import Fore

def udp_scan(target, port):

    try:

        packet = IP(dst=target) / UDP(
            dport=port
        )

        response = sr1(
            packet,
            timeout=2,
            verbose=0
        )

        if response is None:

            print(
                Fore.BLUE +
                f"[UDP OPEN|FILTERED] "
                f"{target}:{port}"
            )

            return True

        return False

    except:
        return False
