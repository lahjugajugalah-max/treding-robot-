import time
import requests

# KONFIGURASI
TELEGRAM_TOKEN = "8661668637:AAGAhINyaA6jPGCL_xAoyxpzNXaJ9rwynTE"
CHAT_ID = "5928694166"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def kirim_notifikasi(pesan):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": pesan}, timeout=10)
    except:
        pass

def ambil_harga():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return float(response.json().get('price', 0))
    except:
        pass
    return None

def main():
    kirim_notifikasi("🚀 Bot SMC PRO Aktif (Mode Prediksi TP/SL)!")
    
    last_status = time.time()
    last_prediksi = time.time()
    harga_lalu = 0

    while True:
        try:
            harga = ambil_harga()
            
            if harga:
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
        
        except Exception as e:
            print(f"Error loop: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
    
