import requests
import time

# --- KONFIGURASI SCALPING ---
SYMBOL = "BTCUSDT"
SL_PERCENT = 0.002  # Stop Loss 0.2%
TP_PERCENT = 0.005  # Take Profit 0.5%
PREV_HIGH = 68000.00 # Harga acuan untuk Breakout

def get_market_data():
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"
        data = requests.get(url).json()
        return float(data['price'])
    except Exception as e:
        print(f"Error ambil data: {e}")
        return None

def main():
    print(f"Robot Scalping {SYMBOL} Aktif...")
    while True:
        price = get_market_data()
        if price:
            print(f"Harga Sekarang: {price:.2f} | Acuan Breakout: {PREV_HIGH}")
            
            # Logika Breakout
            if price > PREV_HIGH:
                sl = price * (1 - SL_PERCENT)
                tp = price * (1 + TP_PERCENT)
                print(f"!!! BREAKOUT TERDETEKSI !!!")
                print(f"Beli di: {price:.2f}")
                print(f"Pasang SL: {sl:.2f}")
                print(f"Pasang TP: {tp:.2f}")
                break # Berhenti setelah dapet sinyal
            else:
                print("Belum Breakout, memantau M1/M15...")
        
        time.sleep(10) # Cek tiap 10 detik

if __name__ == "__main__":
    main()

