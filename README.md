# MQTmine
An algorithm for mine Frequent Pattern from uncertain data stream.

### V2 版本说明 

12/21 修复了BUG，适配IBM提供的TID数据集。但仍有难以发现的小问题，不影响运行。
    
### 代码文件说明

MQTmine.py —— MQT-min 算法主程序。

BSUFmineV2.py —— BSUF-mine 算法主程序。

LoadData.py —— 读取数据的方法。

Combine.py —— 生成组合数的方法。

connect-4.data、connect.dat —— connect 数据集

T10I4D100k.txt、T10I4D1000.txt —— IBM提供的数据集

temp.py —— 一些临时代码。
