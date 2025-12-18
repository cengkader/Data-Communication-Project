**Battleship Data Communication System**
![Python](https://img.shields.io/badge/Python-3.9-blue) 

# Proje Amacı:
Bu proje, veri haberleşmesinde kullanılan Hata Kontrol (Error Control) mekanizmalarını ve bu mekanizmaların farklı Hata Enjeksiyon (Error Injection) türleri altındaki performansını askeri bir senaryo (Komutan - Düşman - Savaş Gemisi) üzerinden simüle etmeyi amaçlar.

## İşlev ve Kapsam:
Sistem, akademik düzeydeki tüm temel hata yönetim tekniklerini içerir:

Hata Kontrol Yöntemleri: CRC-16, Hamming Code, Checksum, Parity Check, LRC.

Hata Enjeksiyon Yöntemleri: Bit Flip, Çoklu Bit Flip, Karakter Değiştirme, Noise, Burst Error, Veri Silme, Gecikme.

## Sistem Mimarisi
Proje, üç katmanlı bir Socket Programming mimarisi üzerine kurulmuştur:

sender.py (Komutan): Veriyi oluşturur, seçilen algoritma ile paketler ve gönderir.

server.py (Düşman Sinyal Bozucu): İletim hattını temsil eder. Gelen veriye kullanıcı müdahalesiyle hata eklenmesini sağlar.

receiver.py (Savaş Gemisi): Gelen paketi doğrular. Hata yoksa veriyi işler, hata varsa reddeder.

Çalıştırma Talimatı
Sistemi başlatmak için 3 ayrı terminal açın ve sırasıyla şu komutları çalıştırın:

```
python receiver.py  # 1. Önce Alıcı (Gemi)
python server.py    # 2. Sonra Sunucu (Düşman)
python sender.py    # 3. En son Gönderici (Komutan)
```
## Demo Senaryoları

**Senaryo 1:**  
Başarılı İletim (Hata Yok)
Komutan: Mesajı yazar ve 1: CRC16 yöntemini seçer.

Düşman: 0: Hata Yok seçeneğini belirler.

Gemi: ✅ "DATA CORRECT" uyarısı vererek mesajı hatasız kabul eder.

**Senaryo 2:** 
Kritik Hata Tespiti (Hata Var)
Komutan: Mesajı gönderir.

Düşman: 7: Burst Error seçeneği ile veriyi manipüle eder.

Gemi: ❌ "DATA CORRUPTED" uyarısı verir. Alınan kod ile hesaplanan kodun uyuşmadığını göstererek veriyi reddeder.