import time
import requests

# KONFIGURASI
TELEGRAM_TOKEN = "8661668637:AAGAhINyaA6jPGCL_xAoyxpzNXaJ9rwynTE"
CHAT_ID = "5928694166"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# State Control
waktu_notif_terakhir = 0
harga_10_menit_lalu = 0
waktu_update_prediksi = 0

def kirim_notifikasi(pesan):
    print(f"[LOG] {pesan}")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[ERROR] Gagal kirim Telegram: {e}")

def ambil_harga_live_binance(simbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={simbol}"
    try:
        respon = requests.get(url, headers=HEADERS, timeout=10).json()
        if 'price' in respon:
            return float(respon['price'])
        return None
    except Exception as e:
        print(f"[ERROR] API Binance bermasalah: {e}")
        return None

def cek_struktur_pasar_pro():
    global waktu_notif_terakhir, waktu_update_prediksi, harga_10_menit_lalu
    
    harga_sekarang = ambil_harga_live_binance("BTCUSDT")
    if harga_sekarang is None:
        return

    # [DEBUG] Melihat sisa waktu di log Railway
    sisa_waktu = 600 - (time.time() - waktu_update_prediksi)
    print(f"[DEBUG] Sisa waktu prediksi: {int(sisa_waktu)} detik | Harga: {harga_sekarang}")

    # 1. Logika Notifikasi Rutin 5 Menit
    if time.time() - waktu_notif_terakhir >= 300:
        msg = f"🔄 [BOT STATUS UPDATE]\nHarga: ${harga_sekarang:,.2f}\nStatus: Menunggu validasi CHoCh & OB..."
        kirim_notifikasi(msg)
        waktu_notif_terakhir = time.time()

    # 2. Logika Prediksi Sinyal 10 Menit
    if time.time() - waktu_update_prediksi >= 600:
        if harga_10_menit_lalu != 0:
            prediksi = "BULLISH" if harga_sekarang > harga_10_menit_lalu else "BEARISH"
            sl = harga_sekarang - 100 if prediksi == "BULLISH" else harga_sekarang + 100
            tp = harga_sekarang + 300 if prediksi == "BULLISH" else harga_sekarang - 300
            
            msg = (f"🔮 [PREDIKSI 10 MENIT]\n"
                   f"Trend: {prediksi}\n"
                   f"Entry: ${harga_sekarang:,.2f}\n"
                   f"SL: ${sl:,.2f} | TP: ${tp:,.2f}")
            kirim_notifikasi(msg)
        
        harga_10_menit_lalu = harga_sekarang
        waktu_update_prediksi = time.time()

if __name__ == "__main__":
    kirim_notifikasi("🚀 Bot SMC PRO Aktif!")
    # Inisialisasi agar tidak spam saat awal
    waktu_notif_terakhir = time.time() - 300 
    waktu_update_prediksi = time.time() - 600
    
    while True:
        try:
            cek_struktur_pasar_pro()
            time.sleep(10)
        except Exception as e:
            print(f"Error utama: {e}")
            time.sleep(10)
            
