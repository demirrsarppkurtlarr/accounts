import os
import sys
import time
import random
import requests
import json
import hashlib
from datetime import datetime

# ==============================
# AYARLAR
# ==============================

LOCAL_VERSION = "3.2.0"

VERSION_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/version.json"
DATA_URL = "https://raw.githubusercontent.com/demirrsarppkurtlarr/accounts/main/accounts.json"

CONSENT_FILE = os.path.join(os.getenv("APPDATA"), "d3m0_consent.json")

# ==============================
# RENKLER
# ==============================

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# ==============================
# TEMİZLE
# ==============================

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

# ==============================
# DEVASA D3m0 ASCII
# ==============================

def d3m0_logo():
    temizle()
    logo = f"""{MAGENTA}
██████╗ ██████╗ ███╗   ███╗  ██████╗ 
██╔══██╗╚════██╗████╗ ████║ ██╔═══██╗
██║  ██║ █████╔╝██╔████╔██║ ██║   ██║
██║  ██║ ╚═══██╗██║╚██╔╝██║ ██║   ██║
██████╔╝██████╔╝██║ ╚═╝ ██║ ╚██████╔╝
╚═════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═════╝ 
{RESET}"""
    print(logo)
    time.sleep(1.2)

# ==============================
# SİNEMATİK YAZI
# ==============================

def yaz_efekt(metin, renk=CYAN, hiz=0.02):
    sys.stdout.write(renk)
    for harf in metin:
        sys.stdout.write(harf)
        sys.stdout.flush()
        time.sleep(hiz)
    print(RESET)

# ==============================
# YAVAŞ PREMIUM LOADER
# ==============================

def premium_loader(metin):
    yaz_efekt(metin, YELLOW, 0.015)
    bar_uzunluk = 30
    for i in range(bar_uzunluk + 1):
        dolu = "█" * i
        bos = "░" * (bar_uzunluk - i)
        yuzde = int((i / bar_uzunluk) * 100)
        sys.stdout.write(f"\r{GREEN}[{dolu}{bos}] %{yuzde}")
        sys.stdout.flush()
        time.sleep(0.08)
    print("\n")

# ==============================
# BOOT SEKANSLARI
# ==============================

def sistem_boot():
    d3m0_logo()
    premium_loader("Çekirdek modüller yükleniyor...")
    premium_loader("Şifreleme katmanı başlatılıyor...")
    premium_loader("Güvenlik doğrulama sistemi aktif ediliyor...")
    premium_loader("Sunucu bağlantısı kuruluyor...")
    premium_loader("Veri senkronizasyonu yapılıyor...")
    yaz_efekt("Sistem Hazır.\n", GREEN, 0.03)

# ==============================
# ONAY SİSTEMİ
# ==============================

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
            yaz_efekt("Onay verilmedi. Program kapatılıyor.", RED)
            time.sleep(2)
            sys.exit()

# ==============================
# GITHUB VERİ ÇEKME
# ==============================

def github_get(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        yaz_efekt("Sunucuya bağlanılamadı!", RED)
        time.sleep(3)
        sys.exit()

# ==============================
# VERSION CHECK
# ==============================

def version_check():
    data = github_get(VERSION_URL)
    server_version = data.get("version", LOCAL_VERSION)

    if server_version != LOCAL_VERSION:
        yaz_efekt(f"Yeni sürüm mevcut: {server_version}", YELLOW)
    else:
        yaz_efekt("Sürüm güncel.", GREEN)

# ==============================
# KEY KONTROL
# ==============================

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
            yaz_efekt("Key hakkı dolmuş.", RED)
            continue

        if datetime.now() > datetime.strptime(info["expires"], "%Y-%m-%d"):
            yaz_efekt("Key süresi dolmuş.", RED)
            continue

        info["used_attempt"] += 1
        yaz_efekt("Key onaylandı!", GREEN)
        return info["tier"]

# ==============================
# ANA PROGRAM
# ==============================

def main():
    sistem_boot()
    onay_al()
    version_check()

    data = github_get(DATA_URL)

    keys = data.get("keys", {})
    accounts = data.get("accounts", {})

    tier = key_kontrol(keys)

    if tier not in accounts:
        yaz_efekt("Bu tier için hesap yok.", RED)
        sys.exit()

    kalan = accounts[tier].copy()

    while True:
        temizle()
        d3m0_logo()
        yaz_efekt("1 - Rastgele Hesap Al", GREEN)
        yaz_efekt("2 - Kalan Hesap", CYAN)
        yaz_efekt("3 - Çıkış", RED)

        secim = input("\n>> ")

        if secim == "1":
            if not kalan:
                yaz_efekt("Hesap kalmadı.", RED)
                time.sleep(1.5)
                continue

            secilen = random.choice(kalan)
            kalan.remove(secilen)

            yaz_efekt(f"Hesap: {secilen}", GREEN)
            time.sleep(2)

        elif secim == "2":
            yaz_efekt(f"Kalan hesap: {len(kalan)}", CYAN)
            input("Devam için Enter...")

        elif secim == "3":
            yaz_efekt("Program kapatılıyor...", RED)
            time.sleep(2)
            sys.exit()

if __name__ == "__main__":
    main()
