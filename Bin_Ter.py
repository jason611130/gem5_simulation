import re
from collections import defaultdict

# 十進位轉三進位
def decimal_to_base3(n):
    if n == 0:
        return "0"
    trits = ""
    while n > 0:
        trits = str(n % 3) + trits
        n //= 3
    return trits

# 將 128 hex → 324 個 base-3 字串
def hex512_to_concat_base3_string(hex_str):
    if len(hex_str) < 128:
        raise ValueError("輸入的十六進位字串長度至少需為 128 hex 字元")
    bin_str = bin(int(hex_str[:128], 16))[2:].zfill(512)
    bin513 = '0' + bin_str
    if len(bin513) != 513 or len(bin513) % 19 != 0:
        raise ValueError("513 bits 無法被 19 整除")
    groups = [bin513[i:i+19] for i in range(0, 513, 19)]
    return ''.join(decimal_to_base3(int(bits, 2)).zfill(12) for bits in groups)

# 讀檔、分類、轉 base-3 字串
def parse_and_group(filename):
    grouped_data = defaultdict(list)
    current_set, current_way = None, None

    with open(filename, 'r') as f:
        for line in f:
            # 匹配 Set 和 Way
            set_way_match = re.match(r'Set:\s*0x([0-9a-fA-F]+),\s*Way:\s*(\d+)', line)
            if set_way_match:
                current_set = set_way_match.group(1).lower()
                current_way = set_way_match.group(2)
                continue

            # 匹配 Data 行
            data_match = re.match(r'\s*Data:\s*([0-9a-fA-F]+)', line)
            if data_match and current_set is not None and current_way is not None:
                hex_str = data_match.group(1)
                try:
                    base3_str = hex512_to_concat_base3_string(hex_str)
                    grouped_data[(current_set, current_way)].append(base3_str)
                except Exception as e:
                    print(f"[錯誤] Set: 0x{current_set}, Way: {current_way} → {e}")
    return grouped_data

# 寫入檔案，合併相同 set/way
def write_grouped_to_file(grouped_data, output_filename):
    with open(output_filename, 'w') as f:
        for (set_val, way_val), trit_list in grouped_data.items():
            f.write(f"Set: 0x{set_val}, Way: {way_val}\n")
            for trit in trit_list:
                f.write(trit + "\n")
            f.write("\n")  # 分組空一行

# 執行主程式
grouped = parse_and_group("grouped_cache_data.txt")
write_grouped_to_file(grouped, "ternary.txt")
print("完成3進制轉換")




