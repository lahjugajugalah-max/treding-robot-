import time
import requests
import sys

# KONFIGURASI
TELEGRAM_TOKEN = "8661668637:AAGAhINyaA6jPGCL_xAoyxpzNXaJ9rwynTE"
CHAT_ID = "5928694166"

def kirim_notifikasi(pesan):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": pesan}, timeout=10)
    except:
        pass

def main():
    print("Bot Starting...")
    sys.stdout.flush()
    kirim_notifikasi("🚀 Bot Trading Aktif - Mode 10 Menit!")
    
    last_price = 0
    
    while True:
        try:
            # 1. Ambil Harga
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            r = requests.get(url, timeout=10)
            price = float(r.json()['price'])
            
            print(f"Harga saat ini: {price}")
            sys.stdout.flush()

            # 2. Analisis Sederhana (Jika harga naik = Buy, Turun = Sell)
            if last_price != 0:
                trend = "BUY" if price > last_price else "SELL"
                
                # RR 1:2 (SL 100 poin, TP 200 poin)
                sl = price - 100 if trend == "BUY" else price + 100
                tp = price + 200 if trend == "BUY" else price - 200
                
                msg = (f"📈 SIGNAL: {trend}\n"
                       f"Entry: ${price:,.2f}\n"
                       f"SL: ${sl:,.2f} | TP: ${tp:,.2f}")
                kirim_notifikasi(msg)
            
            last_price = price
            
            # 3. Tunggu 10 Menit
            time.sleep(600)
            
        except Exception as e:
            print(f"Error: {e}")
            sys.stdout.flush()
            time.sleep(60) # Tunggu 1 menit jika error

if __name__ == "__main__":
    main()
    
