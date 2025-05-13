import re
from collections import defaultdict

# 儲存每組 (set, way) 對應的 data
grouped_data = defaultdict(list)

with open("trace_mcf.txt", "r") as f:
    lines = f.readlines()

current_data = None

for line in lines:
    # 偵測 data 行
    data_match = re.search(r'Data\s*=\s*([0-9a-fA-F]+)', line)
    if data_match:
        current_data = data_match.group(1)
        continue

    # 偵測 set 與 way 的行
    cache_match = re.search(r'set:\s*0x([0-9a-fA-F]+)\s+way:\s*(\d+)', line)
    if cache_match and current_data:
        set_val = cache_match.group(1).lower()
        way_val = cache_match.group(2)
        key = (set_val, way_val)
        grouped_data[key].append(current_data)
        current_data = None  # 清除 data，等待下一筆

# 將整理後的結果輸出
with open("grouped_cache_data.txt", "w") as out:
    for (set_val, way_val), data_list in sorted(grouped_data.items()):
        out.write(f"Set: 0x{set_val}, Way: {way_val}\n")
        for data in data_list:
            out.write(f"  Data: {data}\n")
        out.write("\n")

print("已完成整理，結果寫入 grouped_cache_data.txt")
