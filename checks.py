import shutil
import os
import requests
import time
from datetime import datetime


class Check:
    def __init__(self, name):
        self.name = name

    def run(self):
        return {
            "name": self.name,
            "status": "OK",
            "detail": "Check completed Successfully"
        }


class DiskSpaceCheck(Check):
    def __init__(self, path, min_free_percent, critical_free_percent):
        super().__init__("Disk Space")
        self.path = path
        self.min_free_percent = min_free_percent
        self.critical_free_percent = critical_free_percent

    def run(self):
        total, used, free = shutil.disk_usage(self.path)

        free_percent = (free/total)*100
        if free_percent < self.critical_free_percent:
            status = "FAIL"

        elif free_percent < self.min_free_percent:
            status = "WARN"
        else:
            status = "OK"

        return {
            "name": self.name,
            "status": status,
            "detail": f"Free disk space : {free_percent:.2f}%"
        }


class FolderSizeCheck(Check):
    def __init__(self, path, max_folder_mb, critical_folder_mb):
        super().__init__("Folder Size")
        self.path = path
        self.max_folder_mb = max_folder_mb
        self.critical_folder_mb = critical_folder_mb

    def run(self):
        total_size = 0

        for current_folder, subfolders, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(current_folder, file)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    continue
        folder_size_mb = total_size/(1024**2)
        if folder_size_mb > self.critical_folder_mb:
            status = "FAIL"
        elif folder_size_mb > self.max_folder_mb:
            status = "WARN"
        else:
            status = "OK"

        return {
            "name": self.name,
            "status": status,
            "detail": f"Folder size:{folder_size_mb:.2f} MB"
        }


class LargeFileCheck(Check):
    def __init__(self, path, max_file_mb, critical_file_mb):
        super().__init__("Large Files")
        self.path = path
        self.max_file_mb = max_file_mb
        self.critical_file_mb = critical_file_mb

    def run(self):
        large_files = []
        critical_files = []
        for current_folder, subfolders, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(current_folder, file)
                try:
                    size_mb = os.path.getsize(file_path)/(1024**2)
                    if size_mb > self.critical_file_mb:
                        critical_files.append(file)
                    elif size_mb > self.max_file_mb:
                        large_files.append(file)
                except OSError:
                    continue
        if critical_files:
            status = "FAIL"
            detail = f"{len(critical_files)} critical large file(s) found"
        elif large_files:
            status = "WARN"
            detail = f"{len(large_files)} large file(s) found"
        else:
            status = "OK"
            detail = "No large files found"
        return {
            "name": self.name,
            "status": status,
            "detail": detail
        }


class WebsiteCheck(Check):
    def __init__(self, websites, slow_response_ms):
        self.websites = websites
        self.slow_response_ms = slow_response_ms

    def run(self):
        results = []
        for url in self.websites:
            status_code = ""
            response_time = ""
            try:
                start_time = time.perf_counter()
                response = requests.get(url, timeout=5)
                status_code = response.status_code
                end_time = time.perf_counter()
                response_time = (end_time-start_time)*1000
                if response.status_code >= 200 and response.status_code < 300:
                    if response_time > self.slow_response_ms:
                        status = "WARN"
                        detail = f"Slow response:{response_time:.2f} ms"
                    else:
                        status = "OK"
                        detail = f"Website responded in {response_time:.2f} ms"
                else:
                    status = "FAIL"
                    detail = f"HTTP Error: {response.status_code}"
            except requests.exceptions.Timeout:
                status = "FAIL"
                detail = "Request timed out"
            except requests.exceptions.ConnectionError:
                status = "FAIL"
                detail = "Connection failed"
            except requests.exceptions.RequestException as error:
                status = "FAIL"
                detail = str(error)

            results.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": url,
                "status_code": status_code,
                "response_ms": response_time,
                "status": status,
                "detail": detail


            })
        return results
