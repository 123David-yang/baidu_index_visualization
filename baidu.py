import pandas as pd
from qdata.baidu_index import get_search_index
from qdata.baidu_index import PROVINCE_CODE, CITY_CODE
import time
import random
import os
import logging


current_path = os.path.dirname(os.path.abspath(__file__))
new_folder = "data_folder"
new_folder_path = os.path.join(current_path, new_folder)
if os.path.exists(new_folder_path):
    print("文件夹已经存在")
else:
    os.mkdir(new_folder_path)

keywords_list = [['财神'], ['财神方位'], ['财神爷图片']]

province = PROVINCE_CODE
print(province)


# 返回的是搜索指数，而不是资讯指数
start_date = '2011-01-01'
end_date = '2022-12-31'
cookie1 = 'your_cookie1'
cookie2 = 'your_cookie2'
cookies = [cookie1, cookie2]
data_all1 = pd.DataFrame()

# 按不同省请求数据
for key, value in province.items():
    data_all = pd.DataFrame()
    province_name = key
    print('正在爬取{}'.format(province_name))
    area = int(value)
    cookie = random.choice(cookies)
    if cookie == cookie1:
        cookie_name = 'cookie1'
        print('cookie1')
    else:
        cookie_name = 'cookie2'
        print('cookie2')
    try:
        baidu_list = list(get_search_index(keywords_list=keywords_list,
                                           start_date=start_date, end_date=end_date, cookies=cookie, area=area))
    except:
        logging.info("{}失效了".format(cookie_name))
        cookies.remove(cookie)

    data = pd.DataFrame(baidu_list)
    data['province'] = province_name
    data['keyword'] = data['keyword'].apply(lambda x: x[0])
    data['index'] = data['index'].astype('int')
    data['year'] = data.date.apply(lambda x: x.split('-')[0])
    data.to_csv(
        '{}\\{}.csv'.format(new_folder_path, province_name), index=False)
    data.drop(['date'], axis=1, inplace=True)
    data_all = data.groupby(['keyword', 'year', 'type'], as_index=False)['index'].agg(
        {'mean': 'mean', 'max': 'max', 'sum': 'sum'})
    data_all['province'] = province_name
    temp_column = data_all.pop('province')
    data_all.insert(0, 'province', temp_column)
    data_all1 = pd.concat([data_all1, data_all], ignore_index=True)
    time.sleep(random.randint(10, 30))
    # 更新数据
    data_all1.to_csv(
        '{}\\baidu.csv'.format(new_folder_path), index=False)
