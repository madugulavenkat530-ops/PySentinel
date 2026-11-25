from config import load_config
from checks import DiskSpaceCheck, FolderSizeCheck, LargeFileCheck, WebsiteCheck
from datetime import datetime
import json
import os
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--summary", action="store_true")
parser.add_argument("--report", action="store_true")
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


def save_uptime(results):
    file_exists = os.path.exists("uptime.csv")

    with open("uptime.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists or os.path.getsize("uptime.csv") == 0:
            writer.writerow(
                ["time", "url", "status_code", "response_ms", "status"])

        for result in results:
            if "status_code" in result:
                writer.writerow([
                    result["time"],
                    result["name"],
                    result["status_code"],
                    result["response_ms"],
                    result["status"]
                ])


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


def show_uptime_report():
    if not os.path.exists("uptime.csv"):
        print("No uptime data found.")
        return

    website_data = {}

    with open("uptime.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            url = row["url"]

            if url not in website_data:
                website_data[url] = {
                    "total": 0,
                    "successful": 0,
                    "response_times": []
                }

            website_data[url]["total"] += 1

            if row["status"] in ["OK", "WARN"]:
                website_data[url]["successful"] += 1

            if row["response_ms"]:
                website_data[url]["response_times"].append(
                    float(row["response_ms"])
                )

    print("\n========= WEBSITE UPTIME REPORT =========")

    for url, data in website_data.items():
        uptime = (data["successful"] / data["total"]) * 100

        if data["response_times"]:
            average = sum(data["response_times"]) / len(data["response_times"])
        else:
            average = 0

        print(f"\nWebsite: {url}")
        print(f"Uptime: {uptime:.2f}%")
        print(f"Average Response Time: {average:.2f} ms")


if args.summary:
    show_summary()
    exit()

if args.report:
    show_uptime_report()
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
                   config["critical_file_mb"]),
    WebsiteCheck(
        config["websites"],
        config["slow_response_ms"]
    )
]
all_results = []

for check in checks:
    output = check.run()

    # If a check returns multiple results, handle them individually
    if isinstance(output, list):
        results = output
    else:
        results = [output]

    for result in results:
        all_results.append(result)

        if result["status"] == "OK":
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
save_uptime(all_results)
print("\n History saved successfully!")
print("Website uptime data saved successfully")
