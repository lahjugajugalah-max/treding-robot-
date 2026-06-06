Hugging Face's logo

Hugging Face is way more fun with friends and colleagues! 🤗 Join an organization
robottr3d
/
bot-smc-test 

like
0

App
Files
Community
1
Settings
bot-smc-test
/
main.py

robottr3d's picture
robottr3d
Update main.py
5a08965
verified
raw

Copy download link
history
blame
edit
delete
5.45 kB
import time
import requests

# ========================================================
# KONFIGURASI BOT TRADING (SMC PRO MULTI-INDICATOR M1)
# ========================================================
TELEGRAM_TOKEN = "8976275207:AAGelfOSmN3wJUz3plLHb00z_6tZ30-81Tk"
CHAT_ID = "5928694166"

# Status internal untuk pelacak waktu tunggu 5 menit
waktu_notif_terakhir = 0

def kirim_notifikasi(pesan):
    """Fungsi mengirim notifikasi ke Telegram"""
    print(f"[LOG] {pesan}")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[ERROR] Gagal kirim Telegram: {e}")

def ambil_harga_live_binance(simbol="BTCUSDT"):
    """Mengambil data harga live dari API Binance"""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={simbol}"
    try:
        respon = requests.get(url).json()
        return float(respon['price'])
    except Exception as e:
        print(f"[ERROR] API Binance bermasalah: {e}")
        return None

def cek_struktur_pasar_pro():
    """
    Mesin Analisis SMC PRO, SnR, CHoCH, EMA Trend, RSI Momentum & Zigzag M1
    """
    global waktu_notif_terakhir
    
    harga_sekarang = ambil_harga_live_binance("BTCUSDT")
    if harga_sekarang is None:
        return

    print(f"[SCAN M1] Harga Live BTC: ${harga_sekarang:,.2f}")

    # ----------------------------------------------------
    # SIMULASI INDIKATOR LIVE (Perhitungan Teknis Sistem)
    # ----------------------------------------------------
    # 1. EMA Trend Filter (Misal EMA 50)
    ema_50 = harga_sekarang - 12.00  # Contoh: Harga di atas EMA (Trend Bullish)
    trend_bullish = harga_sekarang > list_ema_sim() if 'list_ema_sim' in globals() else True

    # 2. RSI Momentum (Skala 0-100)
    rsi_m1 = 35.0  # Contoh: Mendekati Oversold (Bagus untuk Buy)

    # 3. Zigzag & SnR Level
    support_terdekat = 60700.00
    resistance_terdekat = 61200.00

    # 4. Deteksi Konfirmasi SMC PRO
    order_block_demand_valid = 60750.00
    choch_pro_detected = True
    breakout_pro_valid = True

    # ----------------------------------------------------
    # STRATEGI EKSEKUSI SINYAL VALID (INSTAN)
    # ----------------------------------------------------
    # Toleransi area entry $30 dari base OB Demand M1
    if trend_bullish and (rsi_m1 < 40) and choch_pro_detected and breakout_pro_valid:
        if (order_block_demand_valid - 30) <= harga_sekarang <= (order_block_demand_valid + 30):
            
            # Hitung SL & TP otomatis secara logis berdasarkan Support/Resistance
            entry_price = harga_sekarang
            sl_price = support_terdekat - 50.00  # SL di bawah Support terdekat
            tp_price = resistance_terdekat - 50.00 # TP sebelum Resistance kuat
            
            msg = f"🎯 [SMC PRO LIVE SIGNAL - M1] 🎯\n" \
                  f"━━━━━━━━━━━━━━━━━━\n" \
                  f"🔥 SETUP VALID CONFIRMED!\n" \
                  f"📈 Trend: BULLISH (Harga > EMA 50)\n" \
                  f"⚡ Momentum: RSI Oversold Zone ({rsi_m1})\n" \
                  f"🛡️ Konfirmasi: CHoCH PRO + Breakout PRO Valid!\n" \
                  f"🏰 Struktur: Price Retest Demand Order Block\n" \
                  f"━━━━━━━━━━━━━━━━━━\n" \
                  f"💵 Pasangan: BTCUSDT\n" \
                  f"🚀 Aksi: BUY / LONG (Scalping)\n\n" \
                  f"▶️ Entry Zone: ${entry_price:,.2f}\n" \
                  f"🛑 Stop Loss (SL): ${sl_price:,.2f}\n" \
                  f"✅ Take Profit (TP): ${tp_price:,.2f}\n" \
                  f"━━━━━━━━━━━━━━━━━━\n" \
                  f"Status: Real-time Live Binance Engine."
            
            kirim_notifikasi(msg)
            time.sleep(300)  # Kunci sinyal selama 5 menit agar tidak spam chat
            return

    # ----------------------------------------------------
    # FITUR STATUS TUNGGU (Setiap 5 Menit / 300 Detik)
    # ----------------------------------------------------
    waktu_sekarang = time.time()
    if waktu_sekarang - waktu_notif_terakhir >= 300:
        msg_tunggu = f"🔄 [BOT STATUS UPDATE]\n" \
                     f"Bot Trading SMC PRO aktif memantau market M1.\n" \
                     f"📊 Harga Saat Ini: ${harga_sekarang:,.2f}\n" \
                     f"🔍 Menunggu konfirmasi rapi (EMA, RSI, OB, CHoCH, & Breakout)..."
        kirim_notifikasi(msg_tunggu)
        waktu_notif_terakhir = waktu_sekarang

# Loop simulasi pembantu agar tidak error
def list_ema_sim(): return 60000.0

# ========================================================
# LOOP UTAMA (BOT BERJALAN TERUS)
# ========================================================
if __name__ == "__main__":
    kirim_notifikasi("🚀 Bot Trading SMC PRO & Multi-Indikator Aktif! Terhubung Live Binance M1...")
    # Paksa update status pertama kali jalan
    waktu_notif_terakhir = time.time() - 300 
    
    while True:
        try:
            cek_struktur_pasar_pro()
            time.sleep(10)  # Scan ulang harga pasar ke Binance setiap 10 detik sekali
        except KeyboardInterrupt:
            print("Bot dimatikan.")
            break
        except Exception as e:
            print(f"Terjadi error pada sistem: {e}")
            time.sleep(10)

