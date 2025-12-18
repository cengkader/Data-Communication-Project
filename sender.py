# sender.py - Komuta Merkezi (Client 1)
import socket
# datacom_utils'dan yeni fonksiyonları import ediyoruz
from datacom_utils import (
    calculate_crc16, calculate_parity, text_to_binary, 
    calculate_2d_parity, calculate_checksum, calculate_hamming
)

# Ayarlar
HOST = '127.0.0.1'
TARGET_PORT = 6001 # Server'ın dinlediği port

def start_sender():
    print("---------------------------------------")
    print("🛰️ Komuta Sistemi: Hata Kontrolü Seçenekleri")
    print("1: CRC-16 (Güçlü Tespit)")
    print("2: Parity Bit (Tek Bit Tespit)")
    print("3: 2D Parity (Matris Parity - Çift Bit Tespit)")
    print("4: Hamming Code (Hata Düzeltme Yeteneği)")
    print("5: Internet Checksum (Sağlama Toplamı)")
    print("---------------------------------------")
    
    while True:
        # Kullanıcıdan mesaj al
        command = input("\n📝 [KOMUTAN] Emriniz nedir? (Örn: VUR A1): ")
        if command.lower() == 'q':
            break
        
        method_choice = input("🔢 [KOMUTAN] Hangi yöntemi kullanalım? (1-5): ")
        
        method_name = ""
        control_info = ""
        
        # Seçime göre kontrol bilgisini hesapla
        if method_choice == '1':
            method_name = "CRC16"
            control_info = calculate_crc16(command)
        elif method_choice == '2':
            method_name = "PARITY"
            binary_data = text_to_binary(command)
            control_info = calculate_parity(binary_data)
        elif method_choice == '3':
            method_name = "2DPARITY"
            control_info = calculate_2d_parity(command)
        elif method_choice == '4':
            method_name = "HAMMING"
            control_info = calculate_hamming(command)
        elif method_choice == '5':
            method_name = "CHECKSUM"
            control_info = calculate_checksum(command)
        else:
            print("⚠️ Geçersiz seçim. Lütfen 1 ile 5 arasında bir sayı girin.")
            continue

        # ... (Geri kalan paket oluşturma ve gönderme kısmı değişmedi)
        
        # Paketi oluştur: DATA|METHOD|CONTROL_INFO
        packet = f"{command}|{method_name}|{control_info}"
        
        # Bilgi mesajı
        print(f"\n📦 Hazırlanan Paket:")
        print(f"   Veri: {command}")
        print(f"   Yöntem: {method_name}")
        print(f"   Kontrol Kodu: {control_info}")
        
        # Gönderme işlemi (değişmedi)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, TARGET_PORT))
                s.sendall(packet.encode('utf-8')) 
                print(f"🚀 [KOMUTAN] Sinyal gönderildi.")
        except ConnectionRefusedError:
            print("❌ [HATA] Düşman istasyonuna (Server) bağlanılamadı! Server çalışıyor mu?")

        # Paketi oluştur: DATA|METHOD|CONTROL_INFO
        packet = f"{command}|{method_name}|{control_info}"
        
        # Bilgi mesajı
        print(f"\n📦 Hazırlanan Paket:")
        print(f"   Veri: {command}")
        print(f"   Yöntem: {method_name}")
        print(f"   Kontrol Kodu: {control_info}")
        
        # Gönderme işlemi (değişmedi)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, TARGET_PORT))
                s.sendall(packet.encode('utf-8')) # UTF-8 kullanmak iyi bir pratik
                print(f"🚀 [KOMUTAN] Sinyal gönderildi.")
        except ConnectionRefusedError:
            print("❌ [HATA] Düşman istasyonuna (Server) bağlanılamadı! Server çalışıyor mu?")

if __name__ == "__main__":
    start_sender()