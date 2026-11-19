from datetime import datetime
import shutil
import os


def disk_usage(path):
    total, used, free = shutil.disk_usage(path)
    total_gb = total/(1024**3)
    used_gb = used/(1024**3)
    free_gb = free/(1024**3)
    return total_gb, used_gb, free_gb


def folder_size(path):
    total_size = 0
    for current_folder, subfolders, files in os.walk(path):
        for file in files:
            file_path = os.path.join(current_folder, file)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                continue
    return total_size


def human_size(num_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = num_bytes
    for unit in units:
        if size < 1024:
            break
        else:
            size = size/1024
    return f"{size:.2f} {unit}"


def largest_files(path, n):
    file_list = []
    for current_folder, subfolders, files in os.walk(path):
        for file in files:
            file_path = os.path.join(current_folder, file)
            try:
                size = os.path.getsize(file_path)
                file_list.append((size, file_path))
            except OSError:
                continue
    file_list.sort(reverse=True)
    return file_list[:n]


def generate_report(path):

    if not os.path.isdir(path):
        print("ERROR : The specified folder does not exist.")
        with open("health_log.txt", "a") as file:
            file.write(
                f"{datetime.now()} | Free Disk: N/A | "
                f"Folder Size: N/A (Invalid path)\n"
            )

        return
    print("="*45)
    print("            PYSENTINEL")
    print("      SYSTEM HEALTH REPORT")
    print("="*45)

    print(datetime.now())

    total, used, free = disk_usage(path)
    print("DISK INFORMATION")
    print(f"Total Space: {total:.2f} GB")
    print(f"Used Space: {used:.2f} GB")
    print(f"Free Space : {free:.2f} GB")

    size = folder_size(path)
    free_percentage = (free/total)*100
    save_log(free_percentage, size)
    files = largest_files(path, 5)
    print("\nFOLDER INFORMATION")
    print(f"Folder Size: {human_size(size)}")

    print("\nTOP 5 LARGEST FILES")

    for file_size, file_path in files:
        print(f"{human_size(file_size)} - {file_path}")

    print("=" * 45)


def save_log(free_percentage, folder_size_bytes):
    current_time = datetime.now()
    with open("health_log.txt", 'a') as file:
        file.write(
            f"{current_time} | Free Disk: {free_percentage:.2f}% | "
            f"Folder Size: {human_size(folder_size_bytes)}\n"
        )


folder = input("Enter folder path (Press Enter for current folder): ")

if folder == "":
    folder = "."

generate_report(folder)
