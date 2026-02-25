import os
import sys
import time
import random
import requests
import json
import pyperclip
from datetime import datetime

# =====================================================
# AYARLAR
# =====================================================

LOCAL_VERSION = "3.2.0"

VERSION_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/version.json"
DATA_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/accounts.json"

ADMIN_PASSWORD = "demir1003"

LOG_FILE = os.path.join(os.getenv("APPDATA"), "d3m0_master_log.json")
CONSENT_FILE = os.path.join(os.getenv("APPDATA"), "d3m0_consent.json")

# =====================================================
# RENKLER
# =====================================================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# =====================================================
# GÜVENLİ PRINT
# =====================================================

def safe_write(text):
    if sys.stdout:
        sys.stdout.write(text)
        sys.stdout.flush()

# =====================================================
# TEMİZLE
# =====================================================

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

# =====================================================
# D3m0 ASCII
# =====================================================

def d3m0_logo():
    temizle()
    logo = f"""{MAGENTA}
██████╗ ██████╗ ███╗   ███╗ ██████╗ 
██╔══██╗██╔══██╗████╗ ████║██╔═══██╗
██║  ██║██████╔╝██╔████╔██║██║   ██║
██║  ██║██╔══██╗██║╚██╔╝██║██║   ██║
██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ 
{RESET}"""
    print(logo)
    time.sleep(1.2)

# =====================================================
# YAZI EFEKT
# =====================================================

def yaz_efekt(metin, renk=CYAN, hiz=0.015):
    if not sys.stdout:
        return
    safe_write(renk)
    for harf in metin:
        safe_write(harf)
        time.sleep(hiz)
    print(RESET)

# =====================================================
# LOADER
# =====================================================

def premium_loader(metin):
    yaz_efekt(metin, YELLOW, 0.01)
    bar_uzunluk = 25
    for i in range(bar_uzunluk + 1):
        dolu = "█" * i
        bos = "░" * (bar_uzunluk - i)
        yuzde = int((i / bar_uzunluk) * 100)
        safe_write(f"\r{GREEN}[{dolu}{bos}] %{yuzde}")
        time.sleep(0.09)
    print("\n")

# =====================================================
# BOOT SEKANSLARI
# =====================================================

def sistem_boot():
    d3m0_logo()
    premium_loader("Çekirdek modüller yükleniyor...")
    premium_loader("Şifreleme katmanı aktif ediliyor...")
    premium_loader("Güvenlik duvarı senkronize ediliyor...")
    premium_loader("Sunucu bağlantısı kuruluyor...")
    premium_loader("Veri doğrulama başlatılıyor...")
    yaz_efekt("Sistem Hazır.\n", GREEN, 0.02)

# =====================================================
# LOG SİSTEMİ
# =====================================================

def log_yaz(event, key_used="None"):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        "key": key_used,
        "pc_user": os.getenv("USERNAME"),
        "pc_name": os.getenv("COMPUTERNAME")
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except:
        pass

# =====================================================
# ONAY
# =====================================================

def onay_al():
    while True:
        yaz_efekt("Log kaydı alınacaktır. Onaylıyor musunuz? (E/H)", CYAN)
        cevap = input(">> ").lower()

        if cevap == "e":
            try:
                with open(CONSENT_FILE, "w") as f:
                    json.dump({"approved": True}, f)
            except:
                pass
            return True

        elif cevap == "h":
            yaz_efekt("Onay verilmedi.", RED)
            time.sleep(1)

# =====================================================
# GITHUB VERİ
# =====================================================

def github_get(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        yaz_efekt("Veri çekilemedi!", RED)
        time.sleep(3)
        sys.exit()

# =====================================================
# VERSION CHECK
# =====================================================

def version_check():
    data = github_get(VERSION_URL)
    server_version = data.get("version", LOCAL_VERSION)

    if server_version != LOCAL_VERSION:
        yaz_efekt(f"Yeni sürüm mevcut: {server_version}", YELLOW)
    else:
        yaz_efekt("Sürüm güncel.", GREEN)

# =====================================================
# ADMIN PANEL
# =====================================================

def admin_panel(keys, accounts):
    while True:
        temizle()
        d3m0_logo()
        yaz_efekt("=== GELİŞMİŞ ADMIN PANEL ===", MAGENTA)
        print("1 - Tüm Keyleri Listele")
        print("2 - Key Detay Görüntüle")
        print("3 - Tier İstatistik")
        print("4 - Hesap Sayıları")
        print("5 - Logları Görüntüle")
        print("6 - Çıkış")

        secim = input("\nSeçim: ")

        if secim == "1":
            for k, v in keys.items():
                kalan = v["max_attempt"] - v["used_attempt"]
                print(f"{k} | Tier: {v['tier']} | Kalan: {kalan}")
            input("Enter...")

        elif secim == "2":
            key_adi = input("Key: ")
            if key_adi in keys:
                print(keys[key_adi])
            input("Enter...")

        elif secim == "3":
            stats = {}
            for v in keys.values():
                stats[v["tier"]] = stats.get(v["tier"], 0) + 1
            print(stats)
            input("Enter...")

        elif secim == "4":
            for tier, liste in accounts.items():
                print(f"{tier}: {len(liste)} hesap")
            input("Enter...")

        elif secim == "5":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
                for l in logs:
                    print(l)
            else:
                print("Log yok.")
            input("Enter...")

        elif secim == "6":
            break

# =====================================================
# KEY KONTROL
# =====================================================

def key_kontrol(keys):
    while True:
        key_input = input("Erişim Key: ").strip().lower()
        key_match = [k for k in keys if k.lower() == key_input]

        if not key_match:
            yaz_efekt("Geçersiz key!", RED)
            continue

        info = keys[key_match[0]]

        if not info.get("active", True):
            yaz_efekt("Key pasif.", RED)
            continue

        if info["used_attempt"] >= info["max_attempt"]:
            yaz_efekt("Hak dolmuş.", RED)
            continue

        if datetime.now() > datetime.strptime(info["expires"], "%Y-%m-%d"):
            yaz_efekt("Süre dolmuş.", RED)
            continue

        info["used_attempt"] += 1
        log_yaz("Key giriş yapıldı", key_match[0])
        yaz_efekt("Key onaylandı!", GREEN)
        return info["tier"], key_match[0]

# =====================================================
# MAIN
# =====================================================

def main():
    sistem_boot()
    onay_al()
    version_check()

    data = github_get(DATA_URL)
    keys = data.get("keys", {})
    accounts = data.get("accounts", {})

    admin_input = input("Admin panel için şifre (boş geç): ")
    if admin_input == ADMIN_PASSWORD:
        admin_panel(keys, accounts)

    tier, used_key = key_kontrol(keys)

    if tier not in accounts:
        yaz_efekt("Tier bulunamadı.", RED)
        sys.exit()

    kalan = accounts[tier].copy()

    while True:
        temizle()
        d3m0_logo()
        print("1 - Rastgele Hesap Al")
        print("2 - Kalan Hesap")
        print("3 - Çıkış")

        secim = input("\n>> ")

        if secim == "1":
            if not kalan:
                yaz_efekt("Hesap kalmadı.", RED)
                time.sleep(1)
                continue

            secilen = random.choice(kalan)
            kalan.remove(secilen)

            try:
                pyperclip.copy(secilen)
                yaz_efekt("Hesap panoya kopyalandı!", GREEN)
            except:
                yaz_efekt("Kopyalama başarısız.", YELLOW)

            log_yaz("Hesap alındı", used_key)
            yaz_efekt(f"Hesap: {secilen}", CYAN)
            time.sleep(2)

        elif secim == "2":
            yaz_efekt(f"Kalan hesap: {len(kalan)}", CYAN)
            input("Enter...")

        elif secim == "3":
            log_yaz("Program çıkışı", used_key)
            yaz_efekt("Program kapatılıyor...", RED)
            time.sleep(2)
            sys.exit()

if __name__ == "__main__":
    main()
