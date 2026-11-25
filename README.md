# PySentinel — System Health & Website Monitor

PySentinel is a Python-based monitoring tool that checks system storage health and website availability. It monitors disk space, folder size, large files, and website response times.

Built using Python and Object-Oriented Programming (OOP), PySentinel uses configurable JSON settings to identify potential system and website issues.

## Features

### System Monitoring

- **Disk Space Monitoring:** Checks available disk space and reports OK, WARN, or FAIL.
- **Folder Size Monitoring:** Tracks the total size of monitored folders.
- **Large File Detection:** Identifies unusually large files.
- **Configurable Thresholds:** Modify monitoring limits through `config.json` without changing Python code.
- **Colour-Coded Output:** Displays monitoring results using different terminal colours.

### Website Monitoring

- **Website Availability:** Checks multiple websites using HTTP requests.
- **Response Time Monitoring:** Measures website response times in milliseconds.
- **Slow Response Detection:** Identifies slow websites using configurable thresholds.
- **Error Handling:** Handles timeouts, connection errors, and HTTP errors without crashing.
- **Uptime Logging:** Automatically records website monitoring results in `uptime.csv`.
- **Uptime Report:** Calculates website uptime percentages and average response times.

### Monitoring History

- **History Tracking:** Saves timestamped system monitoring results in `history.json`.
- **History Limit:** Retains only the latest 50 monitoring runs.
- **Failure Summary:** Counts how many times each system check has failed.

## Project Structure

```text
PySentinel/
│
├── checks.py
├── config.py
├── config.json
├── main.py
├── monitor.py
├── requirements.txt
├── README.md
└── .gitignore
```

Generated monitoring files such as `history.json`, `uptime.csv`, and `health_log.txt` are stored locally and excluded from Git tracking.

## Requirements

- Python 3.x
- Requests library

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/madugulavenkat530-ops/PySentinel.git
```

Navigate into the project folder:

```bash
cd PySentinel
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the monitoring tool:

```bash
python main.py
```

View system failure statistics:

```bash
python main.py --summary
```

View website uptime report:

```bash
python main.py --report
```

## Configuration

Modify `config.json` to adjust monitoring thresholds, folders, and websites.

Example:

```json
{
  "min_free_percent": 20,
  "critical_free_percent": 10,
  "max_folder_mb": 500,
  "critical_folder_mb": 1000,
  "max_file_mb": 100,
  "critical_file_mb": 500,
  "folders_to_watch": ["."],
  "websites": [
    "https://google.com",
    "https://github.com",
    "https://example.com",
    "https://wikipedia.org",
    "https://youtube.com"
  ],
  "slow_response_ms": 2000
}
```

You can add or remove websites and change the slow-response threshold according to your requirements.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Requests library
- JSON
- CSV
- OS and file-system modules
- Argparse
- ANSI terminal colour codes
- Git and GitHub

## Author

Venkat Ram Charan

GitHub: https://github.com/madugulavenkat530-ops
