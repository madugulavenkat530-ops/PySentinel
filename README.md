# PySentinel — System Health Monitor

PySentinel is a Python-based system monitoring tool that collects basic information about a computer's storage and files.

It generates a terminal-based system health report and automatically saves monitoring history in a log file.

## Features

- Displays total, used, and free disk space.
- Calculates the total size of a folder.
- Identifies the five largest files.
- Converts bytes into human-readable sizes (KB, MB, GB).
- Generates a system health report.
- Saves monitoring history in `health_log.txt`.
- Handles invalid folder paths gracefully.

## Technologies Used

- Python 3
- os
- shutil
- datetime




## How to Run

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Make sure Python 3 is installed.
4. Run the following command:

```bash
python monitor.py
```

## Project Structure

PySentinel/
├── monitor.py
├── health_log.txt
└── README.md

## Sample Output

The program displays:
- Disk information
- Folder size
- Five largest files
- Report generation timestamp

Monitoring history is saved in `health_log.txt`.

## Author

Venkat Ram Charan

GitHub: [@madugulaVenkat530]

