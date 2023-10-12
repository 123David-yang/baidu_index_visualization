import pandas as pd

index = pd.read_csv("baidu.csv", encoding='gbk')
population = pd.read_csv('population.csv', encoding='utf-8')

population.rename(columns={'地区': 'province'}, inplace=True)
df = pd.DataFrame()
for year in range(2003, 2023):
    df_tmp = pd.DataFrame()
    year_ = '{}年'.format(year)
    df_tmp = population.loc[:, ['province', year_]]
    df_tmp.rename(columns={'{}年'.format(year): 'population'}, inplace=True)
    df_tmp['year'] = int(year)
    df = pd.concat([df, df_tmp])
index_columns = index.province.unique().tolist()
index['province'] = index.province.apply(lambda x:str(x)[:2])
data_all = index.merge(df,how='left',on=['province','year'])
def adjust_province(x,index_columns):
    for place in index_columns:
        if place.startswith(x):
            return place
data_all['province'] = data_all.province.apply(lambda x:adjust_province(x,index_columns))
data_all['mean'] = data_all['mean']/data_all['population']
data_all.to_csv('data_all.csv', index=False)
