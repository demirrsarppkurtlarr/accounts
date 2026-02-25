import os
import sys
import time
import random
import json
import requests
import pyperclip
from datetime import datetime

# ==============================
# AYARLAR
# ==============================

LOCAL_VERSION = "3.3.0"
DATA_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/accounts.json"
VERSION_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/version.json"

ADMIN_PASSWORD = "demir1003"

LOG_FILE = "system_logs.json"
CONSENT_FILE = os.path.join(os.path.expanduser("~"), "valacc_consent.json")

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ==============================
# ANİMASYONLAR
# ==============================

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def buyuk_logo():
    logo = """
██████╗ ██████╗ ███╗   ███╗  ██████╗ 
██╔══██╗╚════██╗████╗ ████║ ██╔═══██╗
██║  ██║ █████╔╝██╔████╔██║ ██║   ██║
██║  ██║ ╚═══██╗██║╚██╔╝██║ ██║   ██║
██████╔╝██████╔╝██║ ╚═╝ ██║ ╚██████╔╝
╚═════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═════╝ 
"""
    for line in logo.split("\n"):
        print(CYAN + line + RESET)
        time.sleep(0.05)

def loader_bar(text="Yukleniyor", length=30):
    print(YELLOW + text + RESET)
    for i in range(length + 1):
        bar = "█" * i + "-" * (length - i)
        sys.stdout.write(f"\r[{bar}] {int((i/length)*100)}%")
        sys.stdout.flush()
        time.sleep(0.08)
    print("\n")

# ==============================
# LOG SİSTEMİ
# ==============================

def log_event(event_type, key_used="none", extra=""):
    log_data = []

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except:
            log_data = []

    log_entry = {
        "timestamp": str(datetime.now()),
        "event": event_type,
        "key": key_used,
        "version": LOCAL_VERSION,
        "extra": extra
    }

    log_data.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4)

# ==============================
# CONSENT
# ==============================

def onay_al():
    if os.path.exists(CONSENT_FILE):
        return True

    print(CYAN + "\nBu yazilim anonim kullanim loglari toplar." + RESET)
    sec = input("Devam etmek icin onayliyor musunuz? (E/H): ").lower()

    if sec == "e":
        with open(CONSENT_FILE, "w", encoding="utf-8") as f:
            json.dump({"consent": True}, f)
        return True
    else:
        print(RED + "Onay verilmedi. Program kapatiliyor." + RESET)
        time.sleep(2)
        sys.exit()

# ==============================
# AUTO UPDATE
# ==============================

def update_program(file_url):
    try:
        print("Yeni sürüm indiriliyor...")
        r = requests.get(file_url, timeout=10)
        r.raise_for_status()

        current_file = sys.argv[0]
        backup_file = current_file + ".backup"

        with open(current_file, "r", encoding="utf-8") as f:
            old_code = f.read()

        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(old_code)

        with open(current_file, "w", encoding="utf-8") as f:
            f.write(r.text)

        print("Güncelleme tamamlandı. Yeniden başlatılıyor...")
        time.sleep(2)

        os.execv(sys.executable, ['python'] + sys.argv)

    except Exception as e:
        print("Update başarısız:", e)

def check_for_update():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        data = r.json()

        online_version = data.get("version")
        file_url = data.get("file_url")

        if online_version != LOCAL_VERSION:
            print(YELLOW + f"Yeni sürüm bulundu: {online_version}" + RESET)
            sec = input("Güncellemek ister misiniz? (E/H): ").lower()
            if sec == "e":
                update_program(file_url)
    except:
        pass

# ==============================
# BAŞLANGIÇ
# ==============================

temizle()
buyuk_logo()
loader_bar("Sistem Baslatiliyor")

onay_al()
log_event("program_start")

check_for_update()

# ==============================
# DATA ÇEKME
# ==============================

try:
    loader_bar("Sunucuya Baglaniliyor")
    response = requests.get(DATA_URL, timeout=5)
    data = response.json()
except:
    print(RED + "Veri cekilemedi!" + RESET)
    log_event("data_fetch_failed")
    input("Enter...")
    sys.exit()

keys = data.get("keys", {})
accounts = data.get("accounts", {})

# ==============================
# KEY KONTROL
# ==============================

def key_kontrol():
    while True:
        key_input = input("Erisim Key: ").strip().lower()

        key_match = [k for k in keys if k.lower() == key_input]
        if not key_match:
            print(RED + "Gecersiz key!" + RESET)
            log_event("invalid_key", key_input)
            continue

        key_info = keys[key_match[0]]

        key_info["used_attempt"] += 1
        log_event("key_approved", key_match[0])

        return key_info["tier"], key_match[0]

# ==============================
# ADMIN PANEL
# ==============================

def admin_panel():
    while True:
        temizle()
        print(CYAN + "=== ADMIN PANEL ===" + RESET)
        print("1 - Loglari gor")
        print("2 - Loglari temizle")
        print("3 - Cikis")

        sec = input("Secim: ")

        if sec == "1":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    logs = json.load(f)
                    for l in logs:
                        print(l)
            input("Enter...")

        elif sec == "2":
            with open(LOG_FILE, "w") as f:
                json.dump([], f)
            print("Loglar temizlendi.")
            input("Enter...")

        elif sec == "3":
            break

# ==============================
# ADMIN GİRİŞ
# ==============================

admin_input = input("Admin sifre (bos gec): ")
if admin_input == ADMIN_PASSWORD:
    log_event("admin_login")
    admin_panel()
    sys.exit()

tier, used_key = key_kontrol()

kalan_hesaplar = accounts.get(tier, []).copy()

# ==============================
# ANA MENU
# ==============================

while True:
    temizle()
    print(GREEN + "1 - Rastgele Hesap Al" + RESET)
    print("2 - Kalan Hesap")
    print(RED + "3 - Cikis" + RESET)

    secim = input("Secim: ")

    if secim == "1":
        if not kalan_hesaplar:
            print(RED + "Hesap kalmadi." + RESET)
            log_event("no_accounts", used_key)
            time.sleep(1)
            continue

        secilen = random.choice(kalan_hesaplar)
        kalan_hesaplar.remove(secilen)

        pyperclip.copy(secilen)
        print(GREEN + "Hesap panoya kopyalandi!" + RESET)

        log_event("account_taken", used_key, secilen)

        time.sleep(1)

    elif secim == "2":
        print(f"Kalan hesap: {len(kalan_hesaplar)}")
        log_event("check_remaining", used_key)
        input("Enter...")

    elif secim == "3":
        log_event("program_exit", used_key)
        break
