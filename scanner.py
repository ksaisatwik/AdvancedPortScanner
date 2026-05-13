# =========================
# FILE: scanner.py
# =========================

from modules.tcp_scan import tcp_scan
from modules.syn_scan import syn_scan
from modules.udp_scan import udp_scan

from colorama import init, Fore

import argparse
import ipaddress

# Initialize Colorama
init(autoreset=True)

print(Fore.CYAN + "=" * 80)
print(Fore.CYAN + " AdvancedPortScanner - Offensive Recon Framework")
print(Fore.CYAN + "=" * 80)

# Argument Parser
parser = argparse.ArgumentParser(
    description="Advanced Offensive Recon Framework"
)

parser.add_argument(
    "-t",
    "--target",
    required=True,
    help="Target IP or CIDR Range"
)

parser.add_argument(
    "-s",
    "--start",
    type=int,
    default=1,
    help="Start Port"
)

parser.add_argument(
    "-e",
    "--end",
    type=int,
    default=1024,
    help="End Port"
)

parser.add_argument(
    "--udp",
    action="store_true",
    help="Enable UDP Scanning"
)

args = parser.parse_args()

target_input = args.target
start_port = args.start
end_port = args.end
udp_enabled = args.udp

# Generate Target List
targets = []

try:

    network = ipaddress.ip_network(
        target_input,
        strict=False
    )

    for ip in network.hosts():
        targets.append(str(ip))

except:

    targets.append(target_input)

# Start Scanning
for target in targets:

    print(Fore.CYAN + "\n" + "=" * 80)
    print(Fore.CYAN + f" Scanning Target : {target}")
    print(Fore.CYAN + "=" * 80)

    # TCP Scan
    print(Fore.YELLOW + "\n[*] Starting TCP Scan...\n")

    for port in range(start_port, end_port + 1):
        tcp_scan(target, port)

    # SYN Scan
    print(Fore.YELLOW + "\n[*] Starting SYN Stealth Scan...\n")

    for port in range(start_port, end_port + 1):
        syn_scan(target, port)

    # UDP Scan
    if udp_enabled:

        print(Fore.YELLOW + "\n[*] Starting UDP Scan...\n")

        for port in range(start_port, end_port + 1):
            udp_scan(target, port)

print(Fore.CYAN + "\n" + "=" * 80)
print(Fore.CYAN + " Scan Completed")
print(Fore.CYAN + "=" * 80)
