import time
import requests
import sys

# KONFIGURASI
TELEGRAM_TOKEN = "8661668637:AAGAhINyaA6jPGCL_xAoyxpzNXaJ9rwynTE"
CHAT_ID = "5928694166"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def kirim_notifikasi(pesan):
    print(f"[LOG] {pesan}")
    sys.stdout.flush() # Memastikan log tampil di Railway
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": pesan}, timeout=10)
    except Exception as e:
        print(f"[ERROR TG] {e}")
        sys.stdout.flush()

def ambil_harga():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return float(response.json().get('price', 0))
    except Exception as e:
        print(f"[ERROR API] {e}")
        sys.stdout.flush()
    return None

def main():
    print("--- BOT SMC PRO STARTING ---")
    sys.stdout.flush()
    kirim_notifikasi("🚀 Bot SMC PRO Aktif (Mode Prediksi TP/SL)!")
    
    last_status = time.time()
    last_prediksi = time.time()
    harga_lalu = 0

    while True:
        try:
            harga = ambil_harga()
            
            if harga:
                # DEBUG LOG untuk memastikan bot jalan
                print(f"[DEBUG] Harga: ${harga:,.2f} | Detik Prediksi: {int(time.time() - last_prediksi)}")
                sys.stdout.flush()

                # Logika Prediksi setiap 10 Menit (600 detik)
                if time.time() - last_prediksi >= 600:
                    if harga_lalu != 0:
                        pred = "BULLISH" if harga > harga_lalu else "BEARISH"
                        
                        # Kalkulasi SL dan TP
                        if pred == "BULLISH":
                            sl = harga - 150
                            tp = harga + 450
                        else:
                            sl = harga + 150
                            tp = harga - 450
                            
                        msg = (f"🔮 [PREDIKSI 10 MENIT]\n"
                               f"Trend: {pred}\n"
                               f"Entry: ${harga:,.2f}\n"
                               f"🛑 SL: ${sl:,.2f}\n"
                               f"✅ TP: ${tp:,.2f}")
                        kirim_notifikasi(msg)
                    
                    harga_lalu = harga
                    last_prediksi = time.time()

                # Status Update setiap 5 menit
                if time.time() - last_status >= 300:
                    kirim_notifikasi(f"🔄 [BOT STATUS]\nHarga: ${harga:,.2f}\nMemantau Market...")
                    last_status = time.time()
            else:
                print("[DEBUG] Gagal ambil harga, mencoba lagi...")
                sys.stdout.flush()
        
        except Exception as e:
            print(f"Error loop: {e}")
            sys.stdout.flush()
        
        time.sleep(10)

if __name__ == "__main__":
    main()
                  
