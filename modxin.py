import psutil
import socket
import tkinter as tk
from tkinter import messagebox
import os

# 設定
LISTEN_IP = "0.0.0.0" # すべての接続を受け入れる
LISTEN_PORT = 50005
KILL_SWITCH = os.path.join(os.path.expanduser("~"), "Desktop", "stop.txt")

def kill_edge():
    killed = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == "msedge.exe":
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if killed:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showerror("System Error", "リモート指令によりEdgeは終了されました。")
        root.destroy()

def main():
    # UDPソケットの作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    sock.settimeout(1.0) # 1秒ごとにループを回して安全装置をチェック

    print(f"待機中... 終了するにはデスクトップに stop.txt を作成してください。")

    while True:
        if os.path.exists(KILL_SWITCH):
            try: os.remove(KILL_SWITCH)
            except: pass
            break

        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            
            if message == "KILL_EDGE":
                print(f"指令受信: {addr} からの命令を実行します。")
                kill_edge()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"エラー: {e}")

    sock.close()

if __name__ == "__main__":
    main()
