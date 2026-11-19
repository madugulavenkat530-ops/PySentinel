from config import load_config
from checks import DiskSpaceCheck, FolderSizeCheck, LargeFileCheck
from datetime import datetime
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--summary", action="store_true")
args = parser.parse_args()


def save_history(results):
    history_file = "history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = json.load(file)
    else:
        history = []

    new_entry = {
        "timestamp": str(datetime.now()),
        "results": results
    }
    history.append(new_entry)
    history = history[-50:]
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def show_summary():
    if not os.path.exists("history.json"):
        print("No monitoring history found.")
        return
    with open("history.json", "r") as file:
        history = json.load(file)
    failure_counts = {}
    for entry in history:
        for result in entry["results"]:
            name = result["name"]
            if name not in failure_counts:
                failure_counts[name] = 0
            if result["status"] == "FAIL":
                failure_counts[name] += 1
    print("\n========= PYSENTINEL SUMMARY =========")
    for name, count in failure_counts.items():
        print(f"{name}: Failed {count} times")


if args.summary:
    show_summary()
    exit()


config = load_config()

path = config["folders_to_watch"][0]

checks = [
    DiskSpaceCheck(path,
                   config["min_free_percent"],
                   config["critical_free_percent"]),
    FolderSizeCheck(path,
                    config["max_folder_mb"],
                    config["critical_folder_mb"]),
    LargeFileCheck(path,
                   config["max_file_mb"],
                   config["critical_file_mb"])
]
all_results = []
for check in checks:
    result = check.run()
    all_results.append(result)
    if result["status"] == 'OK':
        color = "\033[92m"
    elif result["status"] == "WARN":
        color = "\033[93m"
    else:
        color = "\033[91m"
    reset = "\033[0m"
    print(
        f"{color}[{result['status']}]{reset} "
        f"{result['name']} - {result['detail']}"
    )
save_history(all_results)
print("\n History saved successfully!")
