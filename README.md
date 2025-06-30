# MalCodeX Network Scanner 🔍

A professional multi-threaded port scanner for security assessments, built with Python.

## Features
- 🚀 Fast multi-threaded scanning
- 🔍 Service detection for common ports
- 🎨 Color-coded terminal output
- ⚙️ Customizable scan parameters
- 📁 Clean CLI interface

## Installation

### Kali Linux (Recommended)
```bash
git clone https://github.com/yourusername/malcodex-scanner.git
cd malcodex-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 malcodex-scanner.py
```

## Usage
```bash
python3 malcodex_scanner.py -t <TARGET> [OPTIONS]
```

## Basic Scan
```bash
python3 malcodex_scanner.py -t scanme.nmap.org
```
## Advanced Options
## Option	Description	Example
-t TARGET	Target IP/Domain (required)	-t 192.168.1.1
-p PORTS	Port range (1-1000) or list	-p 20-80 or -p 22,80,443
-T THREADS	Thread count (default: 100)	-T 200
-to TIMEOUT	Timeout in seconds (default: 1.0)	-to 0.5
