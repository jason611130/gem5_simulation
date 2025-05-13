import re
from collections import defaultdict
def read_grouped_base8(filename):
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

# 轉換對照表（略，這裡省略內容以節省篇幅，請用你原本的 transition_table 變數）
transition_table = {
    '0': {
        '0': {
            '0': {'0': ''},
            '1': {'0': 'st+1'},
            '2': {'1': 'st+1 ht+1'},
            '3': {'0': 'ht+1'},
            '4': {'0': 'st+1'},
            '5': {'0': 'st+2'},
            '6': {'1': 'ht+1'},
            '7': {'0': 'st+1 ht+1'}
        },
        '1': {
            '0': {'1': ''},
            '1': {'1': 'st+1'},
            '2': {'0': 'ht+1'},
            '3': {'0': 'st+1 ht+1'},
            '4': {'1': 'st+1'},
            '5': {'1': 'st+2'},
            '6': {'1': 'st+1 ht+1'},
            '7': {'1': 'ht+1'}
        }
    },
    '1': {
        '0': {
            '0': {'0': 'st+1'},
            '1': {'0': ''},
            '2': {'1': 'ht+1'},
            '3': {'0': 'ht+1'},
            '4': {'0': 'st+2'},
            '5': {'0': 'st+1'},
            '6': {'1': 'st+1 ht+1'},
            '7': {'0': 'st+1 ht+1'}
        },
        '1': {
            '0': {'1': 'st+1'},
            '1': {'1': ''},
            '2': {'0': 'ht+1'},
            '3': {'0': 'st+1 ht+1'},
            '4': {'1': 'st+2'},
            '5': {'1': 'st+1'},
            '6': {'1': 'ht+1'},
            '7': {'0': 'st+1 ht+1'}
        }
    },
    '2': {
        '0': {
            '0': {'0': 'ht+1'},
            '1': {'1': 'ht+1'},
            '2': {'0': ''},
            '3': {'0': 'st+1'},
            '4': {'0': 'st+1 ht+1'},
            '5': {'1': 'st+1 ht+1'},
            '6': {'0': 'st+1'},
            '7': {'0': 'st+2'}
        },
        '1': {
            '0': {'0': 'st+1 ht+1'},
            '1': {'0': 'ht+1'},
            '2': {'1': ''},
            '3': {'1': 'st+1'},
            '4': {'1': 'st+1 ht+1'},
            '5': {'1': 'ht+1'},
            '6': {'1': 'st+1'},
            '7': {'1': 'st+2'}
        }
    },
    '3': {
        '0': {
            '0': {'0': 'ht+1'},
            '1': {'1': 'st+1 ht+1'},
            '2': {'0': 'st+1'},
            '3': {'0': ''},
            '4': {'0': 'st+1 ht+1'},
            '5': {'1': 'ht+1'},
            '6': {'0': 'st+2'},
            '7': {'0': 'st+1'}
        },
        '1': {
            '0': {'0': 'st+1 ht+1'},
            '1': {'0': 'ht+1'},
            '2': {'1': 'st+1'},
            '3': {'1': ''},
            '4': {'1': 'ht+1'},
            '5': {'1': 'st+1 ht+1'},
            '6': {'1': 'st+2'},
            '7': {'1': 'st+1'}
        }
    },
    '4': {
        '0': {
            '0': {'0': 'st+1'},
            '1': {'0': 'st+2'},
            '2': {'1': 'st+1 ht+1'},
            '3': {'0': 'st+1 ht+1'},
            '4': {'0': ''},
            '5': {'0': 'st+1'},
            '6': {'1': 'ht+1'},
            '7': {'0': 'ht+1'}
        },
        '1': {
            '0': {'1': 'st+1'},
            '1': {'1': 'st+1'},
            '2': {'1': 'st+2'},
            '3': {'0': 'ht+1'},
            '4': {'1': ''},
            '5': {'1': 'st+1'},
            '6': {'1': 'st+1 ht+1'},
            '7': {'1': 'ht+1'}
        }
    },
    '5': {
        '0': {
            '0': {'0': 'st+1'},
            '1': {'0': 'st+2'},
            '2': {'0': 'st+1'},
            '3': {'1': 'ht+1'},
            '4': {'0': 'st+1'},
            '5': {'0': ''},
            '6': {'1': 'st+1 ht+1'},
            '7': {'0': 'ht+1'}
        },
        '1': {
            '0': {'1': 'st+2'},
            '1': {'1': 'st+1'},
            '2': {'0': 'st+1 ht+1'},
            '3': {'0': 'ht+1'},
            '4': {'1': 'st+1'},
            '5': {'1': ''},
            '6': {'1': 'ht+1'},
            '7': {'1': 'st+1 ht+1'}
        }
    },
    '6': {
        '0': {
            '0': {'0': 'st+1 ht+1'},
            '1': {'1': 'ht+1'},
            '2': {'0': 'st+1'},
            '3': {'0': 'st+2'},
            '4': {'0': 'ht+1'},
            '5': {'1': 'st+1 ht+1'},
            '6': {'0': ''},
            '7': {'0': 'st+1'}
        },
        '1': {
            '0': {'0': 'ht+1'},
            '1': {'0': 'st+1 ht+1'},
            '2': {'1': 'st+1'},
            '3': {'1': 'st+2'},
            '4': {'1': 'st+1 ht+1'},
            '5': {'1': 'ht+1'},
            '6': {'1': ''},
            '7': {'1': 'st+1'}
        }
    },
    '7': {
        '0': {
            '0': {'0': 'st+1 ht+1'},
            '1': {'1': 'st+1 ht+1'},
            '2': {'0': 'st+2'},
            '3': {'0': 'st+1'},
            '4': {'0': 'ht+1'},
            '5': {'1': 'ht+1'},
            '6': {'0': 'st+1'},
            '7': {'0': ''}
        },
        '1': {
            '0': {'0': 'ht+1'},
            '1': {'0': 'st+1 ht+1'},
            '2': {'1': 'st+2'},
            '3': {'1': 'st+1'},
            '4': {'1': 'ht+1'},
            '5': {'1': 'st+1 ht+1'},
            '6': {'1': 'st+1'},
            '7': {'1': ''}
        }
    }
}
# transition_table = { ... (照你原本的內容貼上) ... }

# 比對八進位字串，建立轉換紀錄與統計 st/ht
def compare_octal_transitions(src, src_label, dst):
    label = ''
    st_total = 0
    ht_total = 0
    transition_log = []

    for i in range(len(src)):
        now = src[i]
        lab = src_label[i]
        fut = dst[i]

        try:
            transition_entry = transition_table[now][lab][fut]
            key = list(transition_entry.keys())[0]
            action = transition_entry[key]
        except KeyError:
            # 無法對應 → 略過或記錄錯誤
            transition_log.append(f"{i:03d}: {now}[{lab}] → {fut}[?] : [Invalid]")
            label += '0'  # 或其他預設值
            continue

        # 統計 st / ht
        st_count = len(re.findall(r'st\+1', action)) + 2 * len(re.findall(r'st\+2', action))
        ht_count = len(re.findall(r'ht\+1', action))

        st_total += st_count
        ht_total += ht_count

        # 紀錄
        transition_log.append(f"{i:03d}: {now}[{lab}] → {fut}[{key}] : {action}")
        label += key

    #print("\n".join(transition_log))
    #print(f"\nTotal st: {st_total}, Total ht: {ht_total}\n")
    return label, st_total, ht_total

# 初始標記
# 比對第一筆 → 第二筆

def process_grouped_base8(input_file, output_file):
    grouped_data = read_grouped_base8(input_file)
    total_st = 0
    total_ht = 0

    with open(output_file, 'w') as f:
        for (set_val, way_val), data_list in grouped_data.items():
            st_count = 0
            ht_count = 0
            octal_label = ['0' * 171]  # 初始化第一個 label

            #f.write(f"Set: 0x{set_val}, Way: {way_val}\n")
            for i in range(len(data_list) - 1):
                label, st_step, ht_step = compare_octal_transitions(
                    data_list[i], octal_label[i], data_list[i + 1]
                )
                octal_label.append(label)
                st_count += st_step
                ht_count += ht_step

            total = st_count + ht_count
            #f.write(f"ST = {st_count}, HT = {ht_count}, Total = {total}\n\n")
            total_st += st_count
            total_ht += ht_count

        total_transitions = total_st + total_ht
        f.write(f"Total ST = {total_st}\nTotal HT = {total_ht}\nTotal Transitions = {total_transitions}\n")

    print("分析完成，結果已寫入", output_file)
    
process_grouped_base8("octal.txt", "zeroTT.txt")

