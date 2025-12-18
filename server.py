# server.py - Düşman Sinyal Bozucu (Server)
import socket
import time
import sys # Ekledik: Sadece temiz çıkış için
# datacom_utils'dan tüm hata enjeksiyon fonksiyonlarını import ediyoruz
from datacom_utils import (
    inject_bit_flip, inject_char_substitution, inject_char_deletion, 
    inject_char_insertion, inject_char_swapping, inject_multiple_bit_flip, 
    inject_burst_error
)

# Ayarlar (Değişmedi)
HOST = '127.0.0.1'
LISTEN_PORT = 6001  
TARGET_PORT = 6002  

# Hata Enjeksiyon Fonksiyonları ve İsimleri
ERROR_METHODS = {
    '1': ('Bit Flip', inject_bit_flip),
    '2': ('Karakter Değiştirme', inject_char_substitution),
    '3': ('Karakter Silme', inject_char_deletion),
    '4': ('Karakter Ekleme', inject_char_insertion),
    '5': ('Karakter Swapping', inject_char_swapping),
    '6': ('Çoklu Bit Flip', inject_multiple_bit_flip),
    '7': ('Burst Error', inject_burst_error),
    '0': ('Hata Yok', lambda data: (data, "Veri sağlam iletildi."))
}

def start_server():
    # ... (Soket kurma ve dinleme kısmı) ...
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_listen:
        s_listen.bind((HOST, LISTEN_PORT))
        s_listen.listen()
        print(f"😈 [DÜŞMAN] Jammer aktif. Sinyal aranıyor ({LISTEN_PORT} portu)...")
        
        while True:
            # Server, Komutan'dan gelen sinyali bloklayarak bekler
            conn, addr = s_listen.accept()
            with conn:
                print(f"\n⚡ [DÜŞMAN] Sinyal yakalandı: {addr}")
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    continue
                
                try:
                    original_data, method, control_info = data.split('|')
                except ValueError:
                    print("⚠️ [DÜŞMAN] Paket formatı hatalı. İletim durduruldu.")
                    continue

                print(f"📥 [DÜŞMAN] Alınan Paket: {data}")
                print(f"   (Orijinal Veri: {original_data}, Yöntem: {method}, Kod: {control_info})")
                
                # --- HATA ENJEKSİYONU SEÇİMİ VE UYGULAMASI ---
                
                print("\n--- Hata Enjeksiyon Menüsü ---")
                for key, (name, _) in ERROR_METHODS.items():
                    print(f"{key}: {name}")
                print("-----------------------------")

                choice = input("🔧 [DÜŞMAN] Uygulanacak hata türünü seçin (0-7): ")
                
                if choice not in ERROR_METHODS:
                    print("⚠️ Geçersiz seçim. Hata uygulanmadı.")
                    choice = '0'

                error_name, error_func = ERROR_METHODS[choice]
                
                # Hata fonksiyonunu uygula
                corrupted_data, report = error_func(original_data)
                
                print(f"\n⚙️  [DÜŞMAN] {error_name} uygulanıyor...")
                time.sleep(1)
                
                print(f"   [JAMMER RAPORU] Bozulan Veri: {corrupted_data}")
                print(f"   [JAMMER RAPORU] Detay: {report}")
                
                # Yeni bozuk paketi oluştur (Kontrol Kodu DEĞİŞMEZ!)
                corrupted_packet = f"{corrupted_data}|{method}|{control_info}"
                
                # --- Gemiye (Receiver) İlet ---
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_send:
                        s_send.connect((HOST, TARGET_PORT))
                        s_send.sendall(corrupted_packet.encode('utf-8'))
                        print(f"📤 [DÜŞMAN] Bozulan veri hedefe yollandı: {corrupted_packet}")
                except ConnectionRefusedError:
                    print("❌ [HATA] Hedef Gemiye ulaşılamadı! Receiver çalışıyor mu?")
                
                print("-" * 30)

if __name__ == "__main__":
    start_server()