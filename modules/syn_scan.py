# =========================
# FILE: modules/syn_scan.py
# =========================

from scapy.all import IP, TCP, sr1
from colorama import Fore

def syn_scan(target, port):

    try:

        packet = IP(dst=target) / TCP(
            dport=port,
            flags="S"
        )

        response = sr1(
            packet,
            timeout=1,
            verbose=0
        )

        if response:

            if response.haslayer(TCP):

                # SYN-ACK = OPEN
                if response[TCP].flags == 18:

                    print(
                        Fore.YELLOW +
                        f"[SYN OPEN] {target}:{port}"
                    )

                    return True

        return False

    except:
        return False
