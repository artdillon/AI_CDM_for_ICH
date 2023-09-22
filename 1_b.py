import pandas as pd
from sklearn.linear_model import LogisticRegression

# 读取数据
df1 = pd.read_csv('表1.csv')
df2 = pd.read_csv('表2.csv')
df3 = pd.read_csv('表3.csv')

# 提取前100例患者的数据
df1_train = df1.loc[df1['ID'].isin(range(1, 101)), :]
df2_train = df2.loc[df2['ID'].isin(range(1, 101)), :]
df3_train = df3.loc[df3['ID'].isin(range(1, 101)), :]

# 合并为训练集
train = pd.concat([df1_train, df2_train, df3_train], axis=1)

# 模型训练
X_train = train.loc[:, '年龄':'Kurtosis']  # 特征
y_train = train['是否发生血肿扩张'] # 目标变量

lr = LogisticRegression()
lr.fit(X_train, y_train)

# 所有患者数据
df1_all = df1
df2_all = df2
df3_all = df3

# 预测
X_all = df1_all.merge(df2_all, on='ID').merge(df3_all, on='ID')
X_all = X_all.loc[:, '年龄':'Kurtosis']

prob = lr.predict_proba(X_all)[:,1]

# 写入表4
df4 = pd.read_csv('表4.csv')
df4['血肿扩张预测概率'] = prob
df4.to_csv('表4.csv', index=False)