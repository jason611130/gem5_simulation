#!/bin/bash

# 初次模擬
build/X86/gem5.opt --debug-flag=Cache configs/learning_gem5/part1/2cache.py > trace_mcf.txt

# 執行 100 次迴圈
for i in {1..100}
do
    echo "========== 執行第 $i次 =========="

    # 執行分析與統計程式
    python3 group.py
    python3 Bin_Ter.py
    python3 Bin_Oct.py
    python3 countzeroTT.py
    python3 countTSTZ.py
    python3 countTSTZ33.py
    python3 save_count.py

    # 推送 Git 版本
    git add .
    git commit -m "auto update $i"
    git push -u origin main

    # 繼續模擬
    build/X86/gem5.opt --debug-flag=Cache configs/learning_gem5/part1/2cache.py --resume > trace_mcf.txt
done
