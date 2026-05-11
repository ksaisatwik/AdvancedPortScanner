# Advanced Port Scanner

## Description

Advanced Port Scanner is a multi-threaded Python-based network scanner developed for educational and authorized security testing purposes.

The tool performs:
- TCP port scanning
- Service detection
- Banner grabbing
- CIDR-based scanning
- CSV/JSON/TXT report generation

---

# Features

- Multi-threaded scanning
- Banner grabbing
- Service fingerprinting
- CLI argument parsing
- Scan timing metrics
- Colored terminal output
- CSV export
- JSON export
- TXT logging
- CIDR support
- Vulnerability hints

---

# Technologies Used

- Python
- Socket Programming
- Threading
- argparse
- colorama

---

# Installation

## Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Virtual Environment

```bash
source venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# Usage

## Basic Scan

```bash
python3 scanner.py 127.0.0.1 8000 8100
```

## Fast Mode

```bash
python3 scanner.py 127.0.0.1 1 1000 --mode fast
```

## Full Mode

```bash
python3 scanner.py 127.0.0.1 1 1000 --mode full
```

---

# Example Output

```text
============================================================
ADVANCED PORT SCANNER
============================================================

Scanning Target: 127.0.0.1

[+] 127.0.0.1:8080 OPEN
Service : http-alt
Banner  : HTTP/1.0 200 OK
Hint    : No known basic hint

============================================================
SCAN COMPLETED
============================================================
```

---

# Output Files

The scanner generates:

- scan_results.txt
- results.csv
- results.json

---

# Disclaimer

This project is intended ONLY for:
- educational purposes
- lab environments
- authorized systems

Unauthorized scanning is illegal.

---

# Author

K SAI SATWIK
