import os
import sys
import time
import json
import hashlib
import random
import requests
import pyperclip
from datetime import datetime

# =====================================================
# AYARLAR
# =====================================================
LOCAL_VERSION = "3.3.0"

BASE_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/valacc-release/main/"
VERSION_URL = BASE_URL + "version.json"
ACCOUNTS_URL = BASE_URL + "accounts.json"

ADMIN_PASSWORD = "demir1003"

# =====================================================
# RENKLER
# =====================================================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# =====================================================
# GIZLI KLASOR
# =====================================================
def get_hidden_folder():
    base = os.getenv("LOCALAPPDATA")
    path = os.path.join(base, "D3m0Secure")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

HIDDEN_DIR = get_hidden_folder()
LOG_FILE = os.path.join(HIDDEN_DIR, "activity_logs.json")
CONSENT_FILE = os.path.join(HIDDEN_DIR, "consent.json")

# =====================================================
# YARDIMCI
# =====================================================
def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def yaz(text, color=GREEN):
    print(color + text + RESET)

def ascii_logo():
    print(CYAN + r"""
██████╗ ██████╗ ███╗   ███╗ ██████╗ 
██╔══██╗██╔══██╗████╗ ████║██╔═══██╗
██║  ██║██████╔╝██╔████╔██║██║   ██║
██║  ██║██╔═══╝ ██║╚██╔╝██║██║   ██║
██████╔╝██║     ██║ ╚═╝ ██║╚██████╔╝
╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝ 
              D3m0 Secure System
""" + RESET)

def loader():
    print(YELLOW + "\nSistem Baslatiliyor...\n" + RESET)
    for i in range(31):
        percent = int((i/30)*100)
        bar = "█"*i + "-"*(30-i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.04)
    print("\n")

# =====================================================
# LOG SISTEMI
# =====================================================
def log_event(event, key=None, extra=None):
    entry = {
        "time": str(datetime.now()),
        "event": event,
        "key": key,
        "extra": extra,
        "version": LOCAL_VERSION
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)
    except:
        pass

# =====================================================
# HASH
# =====================================================
def file_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

# =====================================================
# UPDATE SISTEMI (SAFE)
# =====================================================
def check_update():
    try:
        r = requests.get(VERSION_URL, timeout=10)
        if r.status_code != 200:
            return
        data = r.json()

        server_version = data.get("version")
        server_hash = data.get("sha256")
        exe_name = data.get("exe")

        if not server_version:
            return

        if server_version > LOCAL_VERSION:
            yaz(f"Yeni surum mevcut: {server_version}", YELLOW)

            # PY test modunda update yapma
            if not getattr(sys, 'frozen', False):
                yaz("Update sadece EXE modunda aktif.", YELLOW)
                return

            secim = input("Guncellemek ister misiniz? (E/H): ").lower()
            if secim == "e":
                download_update(exe_name, server_hash)

    except Exception as e:
        log_event("update_error", extra=str(e))

def download_update(exe_name, expected_hash):
    try:
        temp_path = os.path.join(os.getenv("TEMP"), exe_name)
        r = requests.get(BASE_URL + exe_name)
        with open(temp_path, "wb") as f:
            f.write(r.content)

        if file_hash(temp_path) != expected_hash:
            yaz("Hash dogrulama basarisiz!", RED)
            return

        create_updater(temp_path)

    except Exception as e:
        log_event("download_update_error", extra=str(e))

def create_updater(new_exe):
    current_exe = sys.executable
    bat = os.path.join(os.getenv("TEMP"), "update.bat")

    with open(bat, "w") as f:
        f.write("@echo off\n")
        f.write("timeout /t 2 > nul\n")
        f.write(f'del "{current_exe}"\n')
        f.write(f'move "{new_exe}" "{current_exe}"\n')
        f.write(f'start "" "{current_exe}"\n')
        f.write('del "%~f0"\n')

    os.startfile(bat)
    sys.exit()

# =====================================================
# CONSENT
# =====================================================
def consent():
    if os.path.exists(CONSENT_FILE):
        return

    while True:
        secim = input("Program log tutabilir. Kabul ediyor musunuz? (E/H): ").lower()
        if secim == "e":
            with open(CONSENT_FILE, "w") as f:
                json.dump({"consent": True}, f)
            log_event("consent_given")
            return
        elif secim == "h":
            log_event("consent_denied")
            sys.exit()

# =====================================================
# MAIN
# =====================================================
try:
    temizle()
    ascii_logo()
    loader()
    log_event("program_start")

    consent()
    check_update()

    r = requests.get(ACCOUNTS_URL, timeout=10)
    if r.status_code != 200:
        raise Exception("accounts.json cekilemedi")

    data = r.json()

except Exception as e:
    yaz("KRITIK HATA", RED)
    print(e)
    input("Enter...")
    sys.exit()

keys = data.get("keys", {})
accounts = data.get("accounts", {})

# =====================================================
# ADMIN PANEL
# =====================================================
def admin_panel():
    while True:
        temizle()
        yaz("=== ADMIN PANEL ===", CYAN)
        print("1 - Keyler")
        print("2 - Loglar")
        print("3 - Cikis")

        secim = input("Secim: ")

        if secim == "1":
            for k, v in keys.items():
                print(k, v)
            input("Enter...")

        elif secim == "2":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE) as f:
                    logs = json.load(f)
                for log in logs[-50:]:
                    print(log)
            input("Enter...")

        elif secim == "3":
            break

# =====================================================
# LOGIN
# =====================================================
admin = input("Admin sifre (bos gec): ")
if admin == ADMIN_PASSWORD:
    log_event("admin_login")
    admin_panel()
    sys.exit()

while True:
    key_input = input("Erisim Key: ").lower()
    match = [k for k in keys if k.lower() == key_input]
    if match:
        used_key = match[0]
        log_event("key_login_success", used_key)
        tier = keys[used_key]["tier"]
        break
    else:
        log_event("key_login_fail", key_input)
        yaz("Gecersiz key!", RED)

# =====================================================
# MENU
# =====================================================
kalan = accounts.get(tier, []).copy()

while True:
    temizle()
    print("1 - Rastgele Hesap")
    print("2 - Kalan Hesap")
    print("3 - Cikis")

    secim = input("Secim: ")

    if secim == "1":
        if not kalan:
            yaz("Hesap kalmadi.", RED)
            log_event("account_empty", used_key)
            time.sleep(1)
            continue

        acc = random.choice(kalan)
        kalan.remove(acc)
        pyperclip.copy(acc)
        yaz("Hesap kopyalandi!", GREEN)
        log_event("account_given", used_key, acc)
        time.sleep(2)

    elif secim == "2":
        print("Kalan:", len(kalan))
        input("Enter...")

    elif secim == "3":
        log_event("program_exit", used_key)
        break
