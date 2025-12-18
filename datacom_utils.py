# datacom_utils.py - Hata Kontrol Fonksiyonları

# --- (1) METİNİ İKİLİ SAYIYA ÇEVİRME ---
def text_to_binary(text):
    """Metin girdisini 8 bitlik ASCII değerlerine göre ikili dizeye çevirir."""
    # 'A' -> 01000001
    return ''.join(format(ord(char), '08b') for char in text)

# --- (2) SADECE TEK EŞLİK BİTİ (PARITY) HESAPLAMA ---
def calculate_parity(binary_data):
    """Verilen ikili dize için Çift Eşlik Biti (Even Parity) hesaplar."""
    # Toplam 1 sayısını bul
    ones_count = binary_data.count('1')
    
    # 1'lerin sayısı tek ise, eşlik bitinin 1 olması gerekir (toplamı çift yapmak için).
    # 1'lerin sayısı çift ise, eşlik bitinin 0 olması gerekir.
    parity_bit = '1' if ones_count % 2 != 0 else '0'
    
    return parity_bit

# --- (3) CRC-16 (Cyclic Redundancy Check) HESAPLAMA ---
# Not: CRC karmaşık bir konudur. Burada standart bir üreteç polinomu (Generator Polynomial) kullanacağız.
# Üreteç Polinomu (G(x)): x^16 + x^15 + x^2 + 1 (16 bitlik veri)
# İkili karşılığı: 1 1000 0000 0000 0101
GENERATOR_POLYNOMIAL = '11000000000000101' # 17 bit

def crc_division(data, generator):
    """CRC'nin temelini oluşturan XOR tabanlı polinom bölmesi."""
    # Data'nın sonuna üretecin uzunluğundan 1 eksik sıfır ekle (17-1 = 16 sıfır)
    appended_data = data + '0' * (len(generator) - 1)
    
    # Bölme işlemini simüle et
    temp_data = list(appended_data)
    divisor_len = len(generator)
    data_len = len(appended_data)

    for i in range(data_len - divisor_len + 1):
        # Eğer ilk bit 1 ise bölme yap
        if temp_data[i] == '1':
            for j in range(divisor_len):
                # XOR işlemi (1 XOR 1 = 0, 1 XOR 0 = 1, 0 XOR 0 = 0)
                temp_data[i+j] = '0' if temp_data[i+j] == generator[j] else '1'
    
    # Kalan (remainder) CRC kodudur. (Son 16 bit)
    remainder = "".join(temp_data[-(len(generator) - 1):])
    return remainder

def calculate_crc16(text):
    """Metin girdisi için 16 bitlik CRC kodu üretir."""
    # Metni ikiliye çevir
    binary_data = text_to_binary(text)
    # CRC hesapla
    crc_code = crc_division(binary_data, GENERATOR_POLYNOMIAL)
    
    # Sonucu okunabilir Hex formatına çevir (Örn: 87AF)
    # 16 bitlik ikili sayıyı 4 haneli onaltılık sayıya çevir
    hex_code = hex(int(crc_code, 2))[2:].upper().zfill(4)
    return hex_code

# datacom_utils.py - Hata Enjeksiyon Fonksiyonları

import random

# ... (text_to_binary, calculate_parity, crc_division, calculate_crc16 fonksiyonları burada kalmalı) ...

def binary_to_text(binary_data):
    """8 bitlik ikili diziyi (string) metne çevirir."""
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        try:
            # 8 bitlik ikiliyi karaktere çevir
            chars.append(chr(int(byte, 2)))
        except ValueError:
            # Geçersiz bir ikili değer gelirse '?' ile değiştir
            chars.append('?') 
    return "".join(chars)

# --- (1) Tek Bit Çevirme (Bit Flip) ---
def inject_bit_flip(data):
    """Metin girdisinin ikili gösteriminde rastgele 1 bit çevirir."""
    binary_data = text_to_binary(data)
    if not binary_data:
        return data, "Veri çok kısa."

    index = random.randint(0, len(binary_data) - 1)
    
    # Biti tersine çevir
    flipped_bit = '0' if binary_data[index] == '1' else '1'
    corrupted_binary = binary_data[:index] + flipped_bit + binary_data[index+1:]
    
    corrupted_data = binary_to_text(corrupted_binary)
    return corrupted_data, f"Bit Flip uygulandı (Bozulan Bit Index: {index})"

# --- (2) Karakter Değiştirme (Substitution) ---
def inject_char_substitution(data):
    """Rastgele bir karakteri başka bir karakterle değiştirir."""
    if len(data) < 1:
        return data, "Veri çok kısa."
    
    index = random.randint(0, len(data) - 1)
    # Yeni bir rastgele ASCII karakteri seç (Görsel karakterler için 33-126 arası)
    new_char = chr(random.randint(33, 126)) 
    
    corrupted_list = list(data)
    corrupted_list[index] = new_char
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Değiştirme uygulandı (Index: {index}, Yeni Karakter: {new_char})"

# --- (3) Karakter Silme (Deletion) ---
def inject_char_deletion(data):
    """Rastgele bir karakteri siler."""
    if len(data) < 2:
        return data, "Veri çok kısa. Silme yapılamadı."
    
    index = random.randint(0, len(data) - 1)
    
    corrupted_list = list(data)
    del corrupted_list[index]
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Silme uygulandı (Silinen Index: {index})"

# --- (4) Karakter Ekleme (Insertion) ---
def inject_char_insertion(data):
    """Rastgele bir yere rastgele bir karakter ekler."""
    # Ekleme için herhangi bir pozisyon seçebiliriz (0'dan, metin uzunluğuna kadar)
    index = random.randint(0, len(data)) 
    new_char = chr(random.randint(33, 126)) 
    
    corrupted_data = data[:index] + new_char + data[index:]
    
    return corrupted_data, f"Karakter Ekleme uygulandı (Index: {index}, Yeni Karakter: {new_char})"

# --- (5) Karakter Yer Değiştirme (Swapping) ---
def inject_char_swapping(data):
    """Yan yana iki karakterin yerini değiştirir."""
    if len(data) < 2:
        return data, "Veri çok kısa. Yer değiştirme yapılamadı."
    
    # İlk karakterin indexini seç (sonuncu hariç)
    index = random.randint(0, len(data) - 2) 
    
    corrupted_list = list(data)
    # Yer değiştirme
    corrupted_list[index], corrupted_list[index+1] = corrupted_list[index+1], corrupted_list[index]
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Swapping uygulandı (Index: {index} ve {index+1} yer değiştirdi)"

# --- (6) Çoklu Bit Çevirme (Multiple Bit Flips) ---
def inject_multiple_bit_flip(data):
    """İkili veride rastgele 2 ila 4 bit çevirir."""
    binary_data = text_to_binary(data)
    if len(binary_data) < 4:
        return data, "Veri çok kısa."

    num_flips = random.randint(2, 4)
    corrupted_binary = list(binary_data)
    flipped_indices = []

    for _ in range(num_flips):
        index = random.randint(0, len(binary_data) - 1)
        # Biti tersine çevir
        corrupted_binary[index] = '0' if corrupted_binary[index] == '1' else '1'
        flipped_indices.append(index)
    
    corrupted_data = binary_to_text("".join(corrupted_binary))
    return corrupted_data, f"Çoklu Bit Flip uygulandı ({num_flips} adet) (Indexler: {flipped_indices})"

# --- (7) Ardışık Hata (Burst Error) ---
def inject_burst_error(data):
    """Rastgele bir başlangıç noktasından itibaren 3 ila 8 karakteri bozar."""
    if len(data) < 8:
        return data, "Veri çok kısa. Burst Error uygulanamadı."
    
    burst_length = random.randint(3, 8)
    
    # Başlangıç noktasını seç
    start_index = random.randint(0, len(data) - burst_length)
    
    # Bozulan kısmı rastgele karakterlerle doldur
    corrupted_section = "".join(chr(random.randint(33, 126)) for _ in range(burst_length))
    
    corrupted_data = list(data)
    # Bozulan kısmı orijinal veriye yerleştir
    corrupted_data[start_index:start_index + burst_length] = list(corrupted_section)
    corrupted_data = "".join(corrupted_data)
    
    return corrupted_data, f"Burst Error uygulandı (Başlangıç: {start_index}, Uzunluk: {burst_length})"

# datacom_utils.py'ye eklenecekler
# ... (Mevcut fonksiyonların altına ekleyin)

# --- (4) 2D PARITY (MATRIX PARITY) HESAPLAMA ---
def calculate_2d_parity(text, block_size=8):
    """Metin girdisi için 2D Parity (Matrix Parity) kodunu hesaplar."""
    
    binary_data = text_to_binary(text)
    
    # Veriyi block_size (varsayılan 8 bit/1 byte) uzunluğunda parçalara ayır
    blocks = [binary_data[i:i + block_size] for i in range(0, len(binary_data), block_size)]
    
    if not blocks:
        return "0" * (block_size + 1) # Boş veri için varsayılan dönüş
    
    # Satır Parity'lerini hesapla
    row_parities = ""
    for block in blocks:
        ones_count = block.count('1')
        row_parities += '1' if ones_count % 2 != 0 else '0' # Çift Parity (Even Parity)
        
    # Sütun Parity'lerini hesapla (Blokların aynı uzunlukta olduğunu varsayıyoruz)
    column_parities = ""
    for j in range(len(blocks[0])): # block_size (sütun sayısı)
        col_ones_count = 0
        for block in blocks:
            # Eğer block boyutu tam değilse, eksik bitleri 0 kabul et
            if j < len(block) and block[j] == '1':
                col_ones_count += 1
        
        column_parities += '1' if col_ones_count % 2 != 0 else '0'
        
    # 2D Parity kodu: Row Parities + Column Parities
    parity_code = row_parities + column_parities
    return parity_code

# datacom_utils.py'ye eklenecekler
# ... (Mevcut fonksiyonların altına ekleyin)

# --- (5) INTERNET CHECKSUM (SAĞLAMA TOPLAMI) HESAPLAMA ---
def calculate_checksum(text, segment_size=16):
    """Metin girdisi için 16 bitlik Internet Checksum'ı hesaplar."""
    
    binary_data = text_to_binary(text)
    
    # Segmentler halinde böl (varsayılan 16 bit)
    segments = [binary_data[i:i + segment_size] for i in range(0, len(binary_data), segment_size)]
    
    # Eğer son segment segment_size'dan kısaysa, sonuna sıfır ekle (padding)
    if len(segments[-1]) < segment_size:
        segments[-1] += '0' * (segment_size - len(segments[-1]))

    total_sum = 0
    
    # Segmentleri topla
    for segment in segments:
        total_sum += int(segment, 2)

    # Toplamın 16 bitten büyükse taşma bitlerini ekle
    # Örneğin: 16 bitlik sayı (0xFFFF) = 65535
    # Eğer toplam 65536'dan büyükse, fazlalığı geri sar
    max_16_bit = 2**segment_size - 1 # 65535
    while total_sum > max_16_bit:
        overflow = total_sum >> segment_size # Taşma bitleri
        total_sum = (total_sum & max_16_bit) + overflow # Taşmayı başa sar

    # Sonucun 1'e tümleyenini (complement) al
    # 1'e tümleyeni almak için: sonucun XOR'unu max_16_bit ile al (1'leri 0, 0'ları 1 yapar)
    checksum = total_sum ^ max_16_bit
    
    # Sonucu okunabilir Hex formatına çevir (4 haneli Hex)
    hex_code = hex(checksum)[2:].upper().zfill(4)
    return hex_code

# datacom_utils.py'ye eklenecekler
# ... (Mevcut fonksiyonların altına ekleyin)

# --- (6) HAMMING CODE (Kontrol Biti Hesaplama) ---
# Not: Hata düzeltme kısmı Client 2'de daha sonra eklenebilir. Şimdilik sadece Kontrol bitlerini hesaplıyoruz.

def calculate_hamming_control_bits(binary_data):
    """Hamming (7,4) veya (12,8) mantığına benzer şekilde kontrol bitlerini hesaplar."""
    
    if len(binary_data) < 4:
        # Çok kısa veri için basit parity döndür
        return calculate_parity(binary_data)
        
    # Basit bir 4 bitlik blok (7,4) Hamming kontrol biti mantığıyla ilerleyelim.
    # Bu, sadece bir kontrol kodu üretmek için basitleştirilmiş bir gösterimdir.
    
    p1 = (int(binary_data[0]) + int(binary_data[1]) + int(binary_data[3])) % 2
    p2 = (int(binary_data[0]) + int(binary_data[2]) + int(binary_data[3])) % 2
    p3 = (int(binary_data[1]) + int(binary_data[2]) + int(binary_data[3])) % 2
    
    # Daha fazla bit için bu çok karmaşıklaşır. Basitçe, verinin ilk 4 bitini kullanıp
    # 3 kontrol biti döndürüyoruz.
    
    return f"{p1}{p2}{p3}" 

def calculate_hamming(text):
    """Tüm metin için Hamming Kontrol Kodunu döndürür."""
    binary_data = text_to_binary(text)
    
    # Tüm veriyi 4 bitlik bloklara bölerek kontrol bitlerini toplayalım
    control_code = ""
    for i in range(0, len(binary_data), 4):
        block = binary_data[i:i+4]
        if len(block) == 4:
            control_code += calculate_hamming_control_bits(block)
        elif len(block) > 0:
            # Eksik bloklar için Parity kullanalım
            control_code += calculate_parity(block)
            
    # Sonucu Hex'e çevirelim (daha kısa görünmesi için)
    try:
        hex_code = hex(int(control_code, 2))[2:].upper()
    except ValueError:
        return "00" # Boş veya hatalı ise
        
    return hex_code