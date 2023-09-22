import pandas as pd

# 读取表1和表2的数据
df1 = pd.read_excel('.//data//表1-患者列表及临床信息.xls')
df2 = pd.read_excel('.//data//表2-患者影像信息血肿及水肿的体积及位置.xls')

# 取前100名患者的数据
df1 = df1[df1['ID'].str.startswith('sub00')].reset_index(drop=True)
df2 = df2[df2['ID'].str.startswith('sub00')].reset_index(drop=True)

# 初始化结果数据框
result = pd.DataFrame(columns=['ID', '是否发生血肿扩张', '血肿扩张时间'])

# 遍历每名患者
for i in range(len(df1)):
    id = df1.loc[i, 'ID']

    # 获取首次影像检查流水号和发病到首次影像检查时间
    first_scan = df1.loc[i, '入院首次影像检查流水号']
    first_interval = df1.loc[i, '发病到首次影像检查时间间隔']

    # 获取该患者所有影像检查的数据
    data = df2[df2['ID'] == id]

    # 初始化变量
    is_expand = 0
    expand_time = None

    # 遍历每次影像检查
    for j in range(len(data)):
        scan = data.loc[j, '流水号']
        volume = data.loc[j, 'HM_volume']

        # 如果是首次检查,记录血肿体积
        if scan == first_scan:
            first_vol = volume

        # 如果不是首次检查
        else:
            # 计算时间间隔
            time = data.loc[j, '时间']
            interval = time - first_interval

            # 判断是否在48小时内
            if interval <= 48:
                # 计算体积变化
                change = volume - first_vol
                ratio = change / first_vol

                # 判断是否发生扩张
                if change >= 6 or ratio >= 0.33:
                    is_expand = 1
                    expand_time = interval
                    break

    # 将结果添加到结果数据框
    result.loc[i] = [id, is_expand, expand_time]

print(result)