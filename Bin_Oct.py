import re
from collections import defaultdict

# 十六進位轉513-bit後轉八進位
def hex512_to_base8_string(hex_str):
    if len(hex_str) < 128:
        raise ValueError("輸入的十六進位字串長度至少需為 128 hex 字元")
    bin_str = bin(int(hex_str[:128], 16))[2:].zfill(512)
    bin513 = '0' + bin_str  # 加一個前綴位元變成 513 bits
    
    int_val = int(bin513, 2)
    return oct(int_val)[2:].zfill(171)  # 去掉 '0o' 前綴

# 讀檔、分類、轉八進位字串
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
                    base8_str = hex512_to_base8_string(hex_str)
                    grouped_data[(current_set, current_way)].append(base8_str)
                except Exception as e:
                    print(f"[錯誤] Set: 0x{current_set}, Way: {current_way} → {e}")
    return grouped_data

# 寫入檔案，合併相同 set/way
def write_grouped_to_file(grouped_data, output_filename):
    with open(output_filename, 'w') as f:
        for (set_val, way_val), oct_list in grouped_data.items():
            f.write(f"Set: 0x{set_val}, Way: {way_val}\n")
            for oct_str in oct_list:
                f.write(oct_str + "\n")
            f.write("\n")  # 分組空一行

# 執行主程式
grouped = parse_and_group("grouped_cache_data.txt")
write_grouped_to_file(grouped, "octal.txt")
print("完成8進制轉換")
