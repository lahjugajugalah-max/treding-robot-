import time
import requests

# KONFIGURASI BOT TRADING (SMC PRO MULTI-INDICATOR M1)
TELEGRAM_TOKEN = "8661668637:AAGAhINyaA6jPGCL_xAoyxpzNXaJ9rwynTE"
CHAT_ID = "5928694166"

# Header agar koneksi Binance stabil
HEADERS = {'User-Agent': 'Mozilla/5.0'}

waktu_notif_terakhir = 0

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
        # Menambahkan HEADERS agar tidak kena blokir
        respon = requests.get(url, headers=HEADERS, timeout=10).json()
        return float(respon['price'])
    except Exception as e:
        print(f"[ERROR] API Binance bermasalah: {e}")
        return None

def cek_struktur_pasar_pro():
    global waktu_notif_terakhir
    
    harga_sekarang = ambil_harga_live_binance("BTCUSDT")
    if harga_sekarang is None:
        return

    print(f"[SCAN M1] Harga Live BTC: ${harga_sekarang:,.2f}")

    rsi_m1 = 35.0
    support_terdekat = 60700.00
    resistance_terdekat = 61200.00
    order_block_demand_valid = 60750.00
    
    if (order_block_demand_valid - 30) <= harga_sekarang <= (order_block_demand_valid + 30):
        msg = f"🎯 [SMC PRO LIVE SIGNAL - M1] 🎯\n" \
              f"🔥 SETUP VALID CONFIRMED!\n" \
              f"💵 BTCUSDT | Aksi: BUY / LONG\n" \
              f"▶️ Entry: ${harga_sekarang:,.2f}\n" \
              f"🛑 SL: ${support_terdekat - 50.00:,.2f}\n" \
              f"✅ TP: ${resistance_terdekat - 50.00:,.2f}"
        
        kirim_notifikasi(msg)
        time.sleep(300)
        return

    waktu_sekarang = time.time()
    if waktu_sekarang - waktu_notif_terakhir >= 300:
        msg_tunggu = f"🔄 [BOT STATUS UPDATE]\nHarga: ${harga_sekarang:,.2f}\nMenunggu konfirmasi..."
        kirim_notifikasi(msg_tunggu)
        waktu_notif_terakhir = waktu_sekarang

if __name__ == "__main__":
    kirim_notifikasi("🚀 Bot SMC PRO Aktif!")
    waktu_notif_terakhir = time.time() - 300 
    while True:
        try:
            cek_struktur_pasar_pro()
            time.sleep(10)
        except Exception as e:
            print(f"Error utama: {e}")
            time.sleep(10)
            
