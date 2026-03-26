import psutil
import os

# Known safe programs that live in AppData
WHITELIST = ["code.exe", "discord.exe", "greenshot.exe", "razerwdl.exe", "adb.exe"]

def advanced_scan():
    print(f"{'PID':<8} | {'Name':<20} | {'Status/Path'}")
    print("-" * 60)
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            name = proc.info['name'] or "System Protected"
            exe_path = proc.info['exe']
            
            # If we can't get the path, it's a high-level system process
            if not exe_path:
                continue

            # Check if it's in a sensitive folder
            is_in_appdata = "AppData" in exe_path
            is_whitelisted = name.lower() in WHITELIST

            if is_in_appdata and not is_whitelisted:
                print(f"[!] UNKNOWN APP IN APPDATA: {name} (PID: {proc.info['pid']})")
                print(f"    Path: {exe_path}")
            
        except (psutil.AccessDenied, psutil.ZombieProcess):
            # These are usually just the core Windows processes (like your PID 428)
            pass

if __name__ == "__main__":
    advanced_scan()
    print("\nScan complete. Known developer tools were filtered out.")