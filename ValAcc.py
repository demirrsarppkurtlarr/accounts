import os
import sys
import time
import random
import requests
import pyperclip
import json
from datetime import datetime

# =========================================
# AYARLAR
# =========================================
LOCAL_VERSION = "3.2.0"

BASE_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/"
DATA_URL = BASE_URL + "accounts.json"
VERSION_URL = BASE_URL + "version.json"

ADMIN_PASSWORD = "demir1003"

LOG_FILE = "activity_logs.json"
CONSENT_FILE = "consent.json"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# =========================================
# YARDIMCI
# =========================================
def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def yaz(metin, renk=GREEN):
    print(renk + metin + RESET)

def loader_bar():
    print(YELLOW + "\nSistem Baslatiliyor...\n" + RESET)
    bar_length = 30
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = "█" * i + "-" * (bar_length - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n")

def ascii_logo():
    print(CYAN + r"""
██████╗ ██████╗ ███╗   ███╗  ██████╗ 
██╔══██╗╚════██╗████╗ ████║ ██╔═══██╗
██║  ██║ █████╔╝██╔████╔██║ ██║   ██║
██║  ██║ ╚═══██╗██║╚██╔╝██║ ██║   ██║
██████╔╝██████╔╝██║ ╚═╝ ██║ ╚██████╔╝
╚═════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═════╝
            D3m0 Secure System
""" + RESET)

# =========================================
# LOG SISTEMI
# =========================================
def log_ekle(event, key_used=None, extra=None):
    log_entry = {
        "timestamp": str(datetime.now()),
        "event": event,
        "key": key_used,
        "extra": extra
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

# =========================================
# ONAY SISTEMI
# =========================================
def onay_al():
    while True:
        print("\nVerileriniz loglanabilir. Devam etmek istiyor musunuz? (E/H)")
        secim = input("Secim: ").lower()

        if secim == "e":
            with open(CONSENT_FILE, "w", encoding="utf-8") as f:
                json.dump({"consent": True}, f)
            return True
        elif secim == "h":
            print("Onay verilmedi. Program kapatiliyor...")
            time.sleep(2)
            sys.exit()

# =========================================
# VERSION CHECK
# =========================================
def version_check(local, server):
    try:
        lv = tuple(map(int, local.split(".")))
        sv = tuple(map(int, server.split(".")))
        if lv < sv:
            yaz(f"Yeni versiyon mevcut: {server}", YELLOW)
    except:
        pass

# =========================================
# BASLANGIC
# =========================================
try:
    temizle()
    ascii_logo()
    loader_bar()

    onay_al()

    # Version çek
    version_response = requests.get(VERSION_URL, timeout=10)
    version_data = version_response.json()
    server_version = version_data.get("version", LOCAL_VERSION)

    # Accounts çek
    response = requests.get(DATA_URL, timeout=10)
    data = response.json()

except Exception as e:
    yaz("KRITIK HATA!", RED)
    print("Detay:", e)
    input("Enter bas...")
    sys.exit()

version_check(LOCAL_VERSION, server_version)

keys = data.get("keys", {})
accounts = data.get("accounts", {})

# =========================================
# ADMIN PANEL
# =========================================
def admin_panel():
    while True:
        temizle()
        yaz("=== ADMIN PANEL ===", CYAN)
        print("1 - Tum keyler")
        print("2 - Loglari gor")
        print("3 - Versiyon bilgisi")
        print("4 - Cikis")

        secim = input("Secim: ")

        if secim == "1":
            for k, v in keys.items():
                print(f"{k} | Tier: {v['tier']}")
            input("Enter...")

        elif secim == "2":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                for log in logs:
                    print(log)
            else:
                print("Log yok.")
            input("Enter...")

        elif secim == "3":
            print("Local:", LOCAL_VERSION)
            print("Server:", server_version)
            input("Enter...")

        elif secim == "4":
            break

# =========================================
# KEY KONTROL
# =========================================
def key_kontrol():
    while True:
        key_input = input("Erisim Key: ").strip().lower()
        key_match = [k for k in keys if k.lower() == key_input]

        if not key_match:
            yaz("Gecersiz key!", RED)
            log_ekle("invalid_key", key_input)
            continue

        key_info = keys[key_match[0]]
        log_ekle("key_login", key_match[0])

        return key_info["tier"], key_match[0]

# =========================================
# ADMIN GIRIS
# =========================================
admin_input = input("Admin sifre (bos gec): ")
if admin_input == ADMIN_PASSWORD:
    admin_panel()
    sys.exit()

tier, used_key = key_kontrol()

if tier not in accounts:
    yaz("Bu tier icin hesap yok.", RED)
    sys.exit()

kalan_hesaplar = accounts[tier].copy()

# =========================================
# ANA MENU
# =========================================
while True:
    temizle()
    yaz("1 - Rastgele Hesap Al", GREEN)
    yaz("2 - Kalan Hesap")
    yaz("3 - Cikis", RED)

    secim = input("Secim: ")

    if secim == "1":
        if not kalan_hesaplar:
            yaz("Hesap kalmadi.", RED)
            time.sleep(1)
            continue

        secilen = random.choice(kalan_hesaplar)
        kalan_hesaplar.remove(secilen)

        pyperclip.copy(secilen)
        yaz("Hesap panoya kopyalandi!", GREEN)

        log_ekle("account_given", used_key, secilen)
        time.sleep(2)

    elif secim == "2":
        yaz(f"Kalan hesap: {len(kalan_hesaplar)}")
        input("Enter...")

    elif secim == "3":
        log_ekle("program_exit", used_key)
        break
