import socket
import threading
import time
import argparse
import csv
import json
import ipaddress

from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

results = []

start_time = time.time()

# -----------------------------
# ARGUMENT PARSER
# -----------------------------

parser = argparse.ArgumentParser(
    description="Advanced Port Scanner"
)

parser.add_argument(
    "target",
    help="Target IP / Domain / CIDR"
)

parser.add_argument(
    "start_port",
    type=int,
    help="Starting Port"
)

parser.add_argument(
    "end_port",
    type=int,
    help="Ending Port"
)

parser.add_argument(
    "--mode",
    choices=["fast", "normal", "full"],
    default="normal",
    help="Scan mode"
)

args = parser.parse_args()

# -----------------------------
# SCAN MODE CONFIGURATION
# -----------------------------

if args.mode == "fast":

    timeout = 0.2
    max_threads = 200

elif args.mode == "full":

    timeout = 1
    max_threads = 50

else:

    timeout = 0.5
    max_threads = 100

# -----------------------------
# TARGET HANDLING
# -----------------------------

def expand_targets(target_input):

    targets = []

    try:

        network = ipaddress.ip_network(
            target_input,
            strict=False
        )

        for ip in network.hosts():

            targets.append(str(ip))

    except ValueError:

        targets.append(target_input)

    return targets


targets = expand_targets(args.target)

# -----------------------------
# VULNERABILITY HINTS
# -----------------------------

vuln_hints = {

    21: "FTP may allow anonymous login",

    22: "Check SSH version and weak credentials",

    23: "Telnet is insecure",

    80: "Web server detected",

    443: "HTTPS service detected",

    3306: "MySQL service exposed",

    3389: "RDP service exposed"
}

# -----------------------------
# THREAD LOCK
# -----------------------------

lock = threading.Lock()

# -----------------------------
# PORT SCANNER FUNCTION
# -----------------------------

def scan_port(target, port):

    scanner = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    scanner.settimeout(timeout)

    try:

        result = scanner.connect_ex((target, port))

        if result == 0:

            try:

                service = socket.getservbyport(port)

            except:

                service = "Unknown"

            banner_data = "Banner unavailable"

            try:

                scanner.send(
                    b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
                )

                banner = scanner.recv(1024).decode(
                    errors="ignore"
                )

                banner_data = banner.split("\n")[0]

            except:

                pass

            vuln = vuln_hints.get(
                port,
                "No known basic hint"
            )

            result_data = {

                "target": target,

                "port": port,

                "service": service,

                "banner": banner_data,

                "hint": vuln
            }

            with lock:

                results.append(result_data)

                print(
                    Fore.GREEN +
                    f"\n[+] {target}:{port} OPEN"
                )

                print(
                    Fore.CYAN +
                    f"Service : {service}"
                )

                print(
                    Fore.YELLOW +
                    f"Banner  : {banner_data}"
                )

                print(
                    Fore.MAGENTA +
                    f"Hint    : {vuln}"
                )

    except:

        pass

    finally:

        scanner.close()

# -----------------------------
# START SCANNING
# -----------------------------

print(Fore.BLUE + "=" * 60)

print(Fore.GREEN + "ADVANCED PORT SCANNER")

print(Fore.BLUE + "=" * 60)

for target in targets:

    print(
        Fore.WHITE +
        f"\nScanning Target: {target}"
    )

    with ThreadPoolExecutor(
        max_workers=max_threads
    ) as executor:

        for port in range(
            args.start_port,
            args.end_port + 1
        ):

            executor.submit(
                scan_port,
                target,
                port
            )

# -----------------------------
# SAVE TXT RESULTS
# -----------------------------

with open(
    "scan_results.txt",
    "w"
) as txt_file:

    for item in results:

        txt_file.write(str(item) + "\n")

# -----------------------------
# SAVE CSV RESULTS
# -----------------------------

with open(
    "results.csv",
    "w",
    newline=""
) as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([

        "Target",

        "Port",

        "Service",

        "Banner",

        "Hint"
    ])

    for item in results:

        writer.writerow([

            item["target"],

            item["port"],

            item["service"],

            item["banner"],

            item["hint"]
        ])

# -----------------------------
# SAVE JSON RESULTS
# -----------------------------

with open(
    "results.json",
    "w"
) as json_file:

    json.dump(
        results,
        json_file,
        indent=4
    )

# -----------------------------
# TIMING METRICS
# -----------------------------

end_time = time.time()

total_time = end_time - start_time

print(Fore.BLUE + "\n" + "=" * 60)

print(Fore.GREEN + "SCAN COMPLETED")

print(
    Fore.YELLOW +
    f"Results Found : {len(results)}"
)

print(
    Fore.CYAN +
    f"Scan Time     : {total_time:.2f} seconds"
)

print(
    Fore.GREEN +
    "TXT Report    : scan_results.txt"
)

print(
    Fore.GREEN +
    "CSV Report    : results.csv"
)

print(
    Fore.GREEN +
    "JSON Report   : results.json"
)

print(Fore.BLUE + "=" * 60)

print(Style.RESET_ALL)
