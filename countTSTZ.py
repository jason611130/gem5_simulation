import re
from collections import defaultdict

# 讀取並分組 base-3 資料 by (Set, Way)
def read_grouped_base3(filename):
    grouped_data = defaultdict(list)
    current_key = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            set_way_match = re.match(r'Set:\s*0x([0-9a-fA-F]+),\s*Way:\s*(\d+)', line)
            if set_way_match:
                set_val = set_way_match.group(1).lower()
                way_val = set_way_match.group(2)
                current_key = (set_val, way_val)
            elif current_key:
                grouped_data[current_key].append(line)
    return grouped_data

# 判斷 ST / HT 類型
def compare_trits(a, b):
    if (a == '0' and b == '1') or (a == '1' and b == '0') or (a == '1' and b == '2') or (a == '2' and b == '1'):
        return 'st'
    elif (a == '0' and b == '2') or (a == '2' and b == '0'):
        return 'ht'
    else:
        return None

# 比較兩筆 base-3 字串
def compare_pair(str1, str2):
    st_count = 0
    ht_count = 0
    length = min(len(str1), len(str2))
    for i in range(length):
        result = compare_trits(str1[i], str2[i])
        if result == 'st':
            st_count += 1
        elif result == 'ht':
            ht_count += 1
    return st_count, ht_count

# 主程式：處理所有 set/way 分組並統計 ST/HT
def process_grouped_base3(input_file, output_file):
    grouped_data = read_grouped_base3(input_file)
    total_st = 0
    total_ht = 0

    with open(output_file, 'w') as f:
        for (set_val, way_val), data_list in grouped_data.items():
            st_sum = 0
            ht_sum = 0
            #f.write(f"Set: 0x{set_val}, Way: {way_val}\n")
            for i in range(len(data_list) - 1):
                st, ht = compare_pair(data_list[i], data_list[i + 1])
                st_sum += st
                ht_sum += ht
            total = st_sum + ht_sum
            #f.write(f"ST = {st_sum}, HT = {ht_sum}, Total = {total}\n\n")
            total_st += st_sum
            total_ht += ht_sum

        total_transitions = total_st + total_ht
        f.write(f"Total ST = {total_st}\nTotal HT = {total_ht}\nTotal Transitions = {total_transitions}\n")

    print("分析完成，結果已寫入 TSTZ.txt")

# 執行主程式
process_grouped_base3("ternary.txt", "TSTZ.txt")

