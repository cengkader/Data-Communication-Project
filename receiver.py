# receiver.py - Savaş Gemisi (Client 2)
import socket
# datacom_utils.py dosyasından tüm gerekli fonksiyonları import ediyoruz
from datacom_utils import (
    calculate_crc16, calculate_parity, text_to_binary, 
    calculate_2d_parity, calculate_checksum, calculate_hamming
) 

# Ayarlar
HOST = '127.0.0.1'  # Localhost
PORT = 6002         # Geminin dinleme portu

# Hata Kontrol Fonksiyonları Sözlüğü (Sender'daki ile aynı olmalı)
# Lambda fonksiyonları, hesaplama fonksiyonlarına sadece veriyi (data) göndermek için kullanılır.
CHECK_FUNCTIONS = {
    "CRC16": calculate_crc16,
    "PARITY": lambda data: calculate_parity(text_to_binary(data)),
    "2DPARITY": calculate_2d_parity,
    "HAMMING": calculate_hamming,
    "CHECKSUM": calculate_checksum,
}

def start_receiver():
    # Soket oluştur (IPv4 ve TCP protokolü)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"🚢 [GEMİ] Sistemler aktif. Komut bekleniyor ({PORT} portu dinleniyor)...")
        
        while True:
            conn, addr = s.accept() # Bağlantıyı kabul et
            with conn:
                print(f"\n📡 [GEMİ] Bağlantı sağlandı: {addr}")
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    continue
                
                # Gelen paketi ayrıştır: DATA|METHOD|CONTROL_INFO
                try:
                    corrupted_data, method, incoming_control = data.split('|')
                except ValueError:
                    print(f"⚠️ Hata: Paket formatı hatalı: {data}")
                    print("-" * 30)
                    continue

                # --- HATA KONTROLÜ VE KARŞILAŞTIRMA ---
                
                computed_control = "HATA"
                
                if method in CHECK_FUNCTIONS:
                    # Gelen bozuk veri (corrupted_data) ile yeniden kontrol kodu hesapla
                    # Örn: calculate_crc16("BOZUK VERİ")
                    computed_control = CHECK_FUNCTIONS[method](corrupted_data)
                
                # Karşılaştırma (Gemi'de hesaplanan kod == Server'dan gelen orijinal kod)
                # Not: Kodu büyük harfe çevirerek karşılaştırmak iyi bir pratik olabilir.
                if computed_control.upper() == incoming_control.upper():
                    status = "✅ DATA CORRECT (Veri Sağlam)"
                else:
                    status = "❌ DATA CORRUPTED (Veri Bozuk!)"
                
                # --- SONUÇ RAPORU (Hocanın İstediği Format) ---
                
                print("\n--- Gelen Sinyal Raporu ---")
                print(f"1. Gelen Veri: {corrupted_data}")
                print(f"2. Yöntem: {method}")
                print(f"3. Gönderilen Kontrol Kodu (Server'dan): {incoming_control}")
                print(f"4. Hesaplanan Kontrol Kodu (Gemi'de):  {computed_control}")
                print(f"5. Durum: {status}")
                
                # Oyun çıktısı:
                if "CORRECT" in status:
                    print(f"\n📢 [GEMİ] Emir SAĞLAM! Komut Uygulanıyor: {corrupted_data}")
                else:
                    print("\n🚨 [GEMİ] KRİTİK HATA! Sinyal BOZUK! Tekrar Emir İsteniyor.")
                    
                print("-" * 30)

if __name__ == "__main__":
    start_receiver()