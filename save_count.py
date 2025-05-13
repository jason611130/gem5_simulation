def read_result_st_ht(filename):
    """
    讀取 result_st_ht.txt 檔案，並解析出 TSTZ33, TSTZ, zeroTT 的數字資料
    """
    result_data = {}
    with open(filename, 'r') as file:
        current_section = None
        for line in file:
            line = line.strip()
            if line in ['TSTZ33', 'TSTZ', 'zeroTT']:
                current_section = line
                result_data[current_section] = {'ST': 0, 'HT': 0, 'Transitions': 0}
            elif 'Total ST' in line:
                result_data[current_section]['ST'] = int(line.split('=')[1].strip())
            elif 'Total HT' in line:
                result_data[current_section]['HT'] = int(line.split('=')[1].strip())
            elif 'Total Transitions' in line:
                result_data[current_section]['Transitions'] = int(line.split('=')[1].strip())
    return result_data


def read_data_from_file(filename):
    """
    讀取資料檔案 (zeroTT.txt, TSTZ.txt, TSTZ33.txt)，並返回對應的資料字典
    """
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            if "Total" in line:
                key, value = line.split('=')
                data[key.strip()] = int(value.strip())
    return data


def update_result_data(result_data, zeroTT_data, TSTZ_data, TSTZ33_data):
    """
    根據檔案資料，將 zeroTT, TSTZ, TSTZ33 的數字加到 result_st_ht.txt 的相對應欄位
    """
    result_data['zeroTT']['ST'] += zeroTT_data['Total ST']
    result_data['zeroTT']['HT'] += zeroTT_data['Total HT']
    result_data['zeroTT']['Transitions'] += zeroTT_data['Total Transitions']

    result_data['TSTZ']['ST'] += TSTZ_data['Total ST']
    result_data['TSTZ']['HT'] += TSTZ_data['Total HT']
    result_data['TSTZ']['Transitions'] += TSTZ_data['Total Transitions']

    result_data['TSTZ33']['ST'] += TSTZ33_data['Total ST']
    result_data['TSTZ33']['HT'] += TSTZ33_data['Total HT']
    result_data['TSTZ33']['Transitions'] += TSTZ33_data['Total Transitions']

    return result_data


def save_updated_data(filename, result_data):
    """
    儲存更新後的資料到 result_st_ht.txt
    """
    with open(filename, 'w') as file:
        for section in ['TSTZ33', 'TSTZ', 'zeroTT']:
            file.write(f"{section}\n")
            file.write(f"Total ST = {result_data[section]['ST']}\n")
            file.write(f"Total HT = {result_data[section]['HT']}\n")
            file.write(f"Total Transitions = {result_data[section]['Transitions']}\n\n")


def main():
    result_filename = 'result_st_ht.txt'
    zeroTT_filename = 'zeroTT.txt'
    TSTZ_filename = 'TSTZ.txt'
    TSTZ33_filename = 'TSTZ33.txt'

    # 讀取檔案資料
    result_data = read_result_st_ht(result_filename)
    zeroTT_data = read_data_from_file(zeroTT_filename)
    TSTZ_data = read_data_from_file(TSTZ_filename)
    TSTZ33_data = read_data_from_file(TSTZ33_filename)

    # 更新資料
    updated_result_data = update_result_data(result_data, zeroTT_data, TSTZ_data, TSTZ33_data)

    # 儲存更新結果
    save_updated_data(result_filename, updated_result_data)

    print("資料已成功更新並儲存至 result_st_ht.txt")


if __name__ == "__main__":
    main()

