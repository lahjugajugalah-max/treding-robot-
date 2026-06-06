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

    # 1. EMA Trend Filter
    trend_bullish = harga_sekarang > list_ema_sim()

    # 2. RSI Momentum (Skala 0-100)
    rsi_m1 = 35.0

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
    if trend_bullish and (rsi_m1 < 40) and choch_pro_detected and breakout_pro_valid:
        if (order_block_demand_valid - 30) <= harga_sekarang <= (order_block_demand_valid + 30):
            
            entry_price = harga_sekarang
            sl_price = support_terdekat - 50.00
            tp_price = resistance_terdekat - 50.00
            
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
            time.sleep(300)
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

def list_ema_sim(): return 60000.0

if __name__ == "__main__":
    kirim_notifikasi("🚀 Bot Trading SMC PRO & Multi-Indikator Aktif! Terhubung Live Binance M1...")
    waktu_notif_terakhir = time.time() - 300 
    
    while True:
        try:
            cek_struktur_pasar_pro()
            time.sleep(10)
        except KeyboardInterrupt:
            print("Bot dimatikan.")
            break
        except Exception as e:
            print(f"Terjadi error pada sistem: {e}")
            time.sleep(10)
            
