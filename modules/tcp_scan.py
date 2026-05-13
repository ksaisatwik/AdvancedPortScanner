# =========================
# FILE: modules/tcp_scan.py
# =========================

import socket
from colorama import Fore

# Common Services
common_ports = {

    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy",
    9090: "HTTP Alternate"

}

# Vulnerability Database
vulnerable_services = {

    "OpenSSH_7.2": {
        "cve": "CVE-2016-0777",
        "severity": "HIGH"
    },

    "Apache/2.4.49": {
        "cve": "CVE-2021-41773",
        "severity": "CRITICAL"
    },

    "vsFTPd 2.3.4": {
        "cve": "CVE-2011-2523",
        "severity": "CRITICAL"
    }

}

def tcp_scan(target, port):

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:

            service = common_ports.get(
                port,
                "Unknown Service"
            )

            print(
                Fore.GREEN +
                f"[TCP OPEN] {target}:{port} --> {service}"
            )

            banner = ""

            try:

                sock.send(b"HELLO\r\n")

                banner = sock.recv(
                    1024
                ).decode(
                    errors="ignore"
                ).strip()

                if banner:

                    print(
                        Fore.MAGENTA +
                        f" Banner: {banner}"
                    )

                    # Vulnerability Detection
                    for service_name in vulnerable_services:

                        if service_name in banner:

                            vulnerability = vulnerable_services[
                                service_name
                            ]["cve"]

                            severity = vulnerable_services[
                                service_name
                            ]["severity"]

                            print(
                                Fore.RED +
                                f" [VULNERABILITY] "
                                f"{vulnerability}"
                            )

                            print(
                                Fore.RED +
                                f" Severity: {severity}"
                            )

            except:
                pass

            sock.close()

            return True

        sock.close()

        return False

    except:
        return False
