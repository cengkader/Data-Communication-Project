def text_to_binary(text):
    """Metin girdisini 8 bitlik ASCII değerlerine göre ikili dizeye çevirir."""
    
    return ''.join(format(ord(char), '08b') for char in text)


def calculate_parity(binary_data):
    """Verilen ikili dize için Çift Eşlik Biti (Even Parity) hesaplar."""
    
    ones_count = binary_data.count('1')
    

    parity_bit = '1' if ones_count % 2 != 0 else '0'
    
    return parity_bit


GENERATOR_POLYNOMIAL = '11000000000000101' 

def crc_division(data, generator):
    """CRC'nin temelini oluşturan XOR tabanlı polinom bölmesi."""
    
    appended_data = data + '0' * (len(generator) - 1)
    
    
    temp_data = list(appended_data)
    divisor_len = len(generator)
    data_len = len(appended_data)

    for i in range(data_len - divisor_len + 1):
        
        if temp_data[i] == '1':
            for j in range(divisor_len):
                
                temp_data[i+j] = '0' if temp_data[i+j] == generator[j] else '1'
    
    
    remainder = "".join(temp_data[-(len(generator) - 1):])
    return remainder

def calculate_crc16(text):
    """Metin girdisi için 16 bitlik CRC kodu üretir."""
    
    binary_data = text_to_binary(text)
    
    crc_code = crc_division(binary_data, GENERATOR_POLYNOMIAL)
   
    hex_code = hex(int(crc_code, 2))[2:].upper().zfill(4)
    return hex_code



import random



def binary_to_text(binary_data):
    """8 bitlik ikili diziyi (string) metne çevirir."""
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        try:
            
            chars.append(chr(int(byte, 2)))
        except ValueError:
            
            chars.append('?') 
    return "".join(chars)


def inject_bit_flip(data):
    """Metin girdisinin ikili gösteriminde rastgele 1 bit çevirir."""
    binary_data = text_to_binary(data)
    if not binary_data:
        return data, "Veri çok kısa."

    index = random.randint(0, len(binary_data) - 1)
    
    
    flipped_bit = '0' if binary_data[index] == '1' else '1'
    corrupted_binary = binary_data[:index] + flipped_bit + binary_data[index+1:]
    
    corrupted_data = binary_to_text(corrupted_binary)
    return corrupted_data, f"Bit Flip uygulandı (Bozulan Bit Index: {index})"


def inject_char_substitution(data):
    """Rastgele bir karakteri başka bir karakterle değiştirir."""
    if len(data) < 1:
        return data, "Veri çok kısa."
    
    index = random.randint(0, len(data) - 1)
   
    new_char = chr(random.randint(33, 126)) 
    
    corrupted_list = list(data)
    corrupted_list[index] = new_char
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Değiştirme uygulandı (Index: {index}, Yeni Karakter: {new_char})"


def inject_char_deletion(data):
    """Rastgele bir karakteri siler."""
    if len(data) < 2:
        return data, "Veri çok kısa. Silme yapılamadı."
    
    index = random.randint(0, len(data) - 1)
    
    corrupted_list = list(data)
    del corrupted_list[index]
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Silme uygulandı (Silinen Index: {index})"


def inject_char_insertion(data):
    """Rastgele bir yere rastgele bir karakter ekler."""
    
    index = random.randint(0, len(data)) 
    new_char = chr(random.randint(33, 126)) 
    
    corrupted_data = data[:index] + new_char + data[index:]
    
    return corrupted_data, f"Karakter Ekleme uygulandı (Index: {index}, Yeni Karakter: {new_char})"


def inject_char_swapping(data):
    """Yan yana iki karakterin yerini değiştirir."""
    if len(data) < 2:
        return data, "Veri çok kısa. Yer değiştirme yapılamadı."
    
    
    index = random.randint(0, len(data) - 2) 
    
    corrupted_list = list(data)
    
    corrupted_list[index], corrupted_list[index+1] = corrupted_list[index+1], corrupted_list[index]
    corrupted_data = "".join(corrupted_list)
    
    return corrupted_data, f"Karakter Swapping uygulandı (Index: {index} ve {index+1} yer değiştirdi)"


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
        
        corrupted_binary[index] = '0' if corrupted_binary[index] == '1' else '1'
        flipped_indices.append(index)
    
    corrupted_data = binary_to_text("".join(corrupted_binary))
    return corrupted_data, f"Çoklu Bit Flip uygulandı ({num_flips} adet) (Indexler: {flipped_indices})"


def inject_burst_error(data):
    """Rastgele bir başlangıç noktasından itibaren 3 ila 8 karakteri bozar."""
    if len(data) < 8:
        return data, "Veri çok kısa. Burst Error uygulanamadı."
    
    burst_length = random.randint(3, 8)
    
    
    start_index = random.randint(0, len(data) - burst_length)
    
    
    corrupted_section = "".join(chr(random.randint(33, 126)) for _ in range(burst_length))
    
    corrupted_data = list(data)
    
    corrupted_data[start_index:start_index + burst_length] = list(corrupted_section)
    corrupted_data = "".join(corrupted_data)
    
    return corrupted_data, f"Burst Error uygulandı (Başlangıç: {start_index}, Uzunluk: {burst_length})"

def calculate_2d_parity(text, block_size=8):
    """Metin girdisi için 2D Parity (Matrix Parity) kodunu hesaplar."""
    
    binary_data = text_to_binary(text)
    
    
    blocks = [binary_data[i:i + block_size] for i in range(0, len(binary_data), block_size)]
    
    if not blocks:
        return "0" * (block_size + 1) 
    
    
    row_parities = ""
    for block in blocks:
        ones_count = block.count('1')
        row_parities += '1' if ones_count % 2 != 0 else '0' 
        
    
    column_parities = ""
    for j in range(len(blocks[0])): 
        col_ones_count = 0
        for block in blocks:
            
            if j < len(block) and block[j] == '1':
                col_ones_count += 1
        
        column_parities += '1' if col_ones_count % 2 != 0 else '0'
        
    
    parity_code = row_parities + column_parities
    return parity_code


def calculate_checksum(text, segment_size=16):
    """Metin girdisi için 16 bitlik Internet Checksum'ı hesaplar."""
    
    binary_data = text_to_binary(text)
    
    
    segments = [binary_data[i:i + segment_size] for i in range(0, len(binary_data), segment_size)]
    
    
    if len(segments[-1]) < segment_size:
        segments[-1] += '0' * (segment_size - len(segments[-1]))

    total_sum = 0
    
    
    for segment in segments:
        total_sum += int(segment, 2)

  
    max_16_bit = 2**segment_size - 1 
    while total_sum > max_16_bit:
        overflow = total_sum >> segment_size 
        total_sum = (total_sum & max_16_bit) + overflow 

    checksum = total_sum ^ max_16_bit
    
    
    hex_code = hex(checksum)[2:].upper().zfill(4)
    return hex_code


def calculate_hamming_control_bits(binary_data):
    """Hamming (7,4) veya (12,8) mantığına benzer şekilde kontrol bitlerini hesaplar."""
    
    if len(binary_data) < 4:
        
        return calculate_parity(binary_data)
        
  
    
    p1 = (int(binary_data[0]) + int(binary_data[1]) + int(binary_data[3])) % 2
    p2 = (int(binary_data[0]) + int(binary_data[2]) + int(binary_data[3])) % 2
    p3 = (int(binary_data[1]) + int(binary_data[2]) + int(binary_data[3])) % 2
    
   
    
    return f"{p1}{p2}{p3}" 

def calculate_hamming(text):
    """Tüm metin için Hamming Kontrol Kodunu döndürür."""
    binary_data = text_to_binary(text)
    
    
    control_code = ""
    for i in range(0, len(binary_data), 4):
        block = binary_data[i:i+4]
        if len(block) == 4:
            control_code += calculate_hamming_control_bits(block)
        elif len(block) > 0:
            
            control_code += calculate_parity(block)
            
    
    try:
        hex_code = hex(int(control_code, 2))[2:].upper()
    except ValueError:
        return "00" 
        
    return hex_code