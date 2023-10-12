import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd


url2 = 'https://www.maigoo.com/news/480576.html'  # 2021-2003
url3 = 'https://www.maigoo.com/top/431525.html'  # 2022-2022


def adjust_porvince(x):
    return x[0:2]


"""
url2
"""
df_list = pd.read_html(url2, encoding='utf-8', header=0)
df1 = df_list[0]
df2 = df_list[1]


df2.loc[len(df2)] = df2.sum()
df2.iloc[-1, 0] = '总人'

df1['地区'] = df1['地区'].apply(lambda x: adjust_porvince(x))
df2['地区'] = df2['地区'].apply(lambda x: adjust_porvince(x))
df2021_2003 = pd.merge(df1, df2, how='left', on='地区')


"""
url3
"""
df_list1 = pd.read_html(url3, encoding='utf-8', header=0)
df3 = df_list1[0]
df3.rename(columns={'省级行政区': '地区'}, inplace=True)
df3['地区'] = df3['地区'].apply(lambda x: adjust_porvince(x))
df3.loc[len(df3)] = df3.loc[0]
df2022 = df3[1:]


df_population = df2022[['地区', '2022年']].merge(df2021_2003, how='left', on='地区')
row_fillna = df_population.loc[(df_population['2022年'].notnull()) & (
    df_population['2021年'].isnull()), '2022年']
# 使用2022年的数据为缺失值插补
for year in range(2003, 2022):
    df_population.loc[df_population['{}年'.format(
        year)].isnull(), '{}年'.format(year)] = row_fillna
print(df_population)
df_population.to_csv('population.csv', index=False)
