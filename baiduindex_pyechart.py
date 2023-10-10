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
cookie1 = 'BIDUPSID=21722FDB14083C86AB3497C8DEE6839F; PSTM=1594036410; Hm_up_d101ea4d2a5c67dab98251f0b5de24dc={"uid_":{"value":"3896297528","scope":1}}; BAIDUID=5DB611835F65DA3C3937CAC575E4B3F7:FG=1; MCITY=-131:; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1681041118; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BAIDUID_BFESS=5DB611835F65DA3C3937CAC575E4B3F7:FG=1; BA_HECTOR=0l0h8hak258g2l0k2g2ga4191i3c4gp1n; ZFY=ANvevV6joWY8bfVfhLhx1:ATIHqvOV6:Bk6hFeCPYvW:B4:C; PSINO=6; H_PS_PSSID=36543_38470_38354_38368_38468_38289_38485_37923_37710_38356_26350_38282; delPer=1; BDUSS=FnUVNYM0R6dmZma2piczBXSTNuWFViZ2lwOXN5YlpLclBScjg1NzJMc0twVjFrSUFBQUFBJCQAAAAAAQAAAAEAAAAxHuhkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoYNmQKGDZkN2; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04312791488Et7Ly6j5ckW7dgc6qR9aVhdl0dMFH3F0e4rPIHFnmriCgW86oRPyCGD03N0PBU40RUh/YN1FnL/omWZbl3YmwFBNUHqP3sh654Ej79VA/MJdLBL43ToJ7fFRdFyR9BIHOHe265OJSOV5tvvVkodceO3Vhemh4/CB0rNz6c6ScfKdPwWfBg/KiINaAGFmmiwfi1XNv0mEEw6nyQwQwSEZ8VFMNAv7NJta3QkTG/tWdX8WPFrLS9MWbbxaPLlTwmCUUQlW8DHGH+DrKDAL471Qx8X46LiZJ2LbXjEf0QcKGlE=18158170442104174686535652886828; __cas__rn__=431279148; __cas__st__212=7e7deac5be69293911caf25ea41746a28c99263b9727d0a15c86ac4829bd72b3f78d008e71e9f0cb7e1ece62; __cas__id__212=47300827; CPID_212=47300827; CPTK_212=304591576; bdindexid=ss4db0bfvjha1q4udbthofhld4; RT="z=1&dm=baidu.com&si=e2bb11eb-2cea-492b-b1f7-2a8d85b2e574&ss=lgd1o5bs&sl=u&tt=1289&bcn=https://fclog.baidu.com/log/weirwood?type=perf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1681266713'
cookie2 = 'PSTM=1659942912; BIDUPSID=1426A0E8C41A9C3C632D1060D906A7E7; BAIDUID=C7DF70CBD0CFD117B1BD39F5F5493CC6:FG=1; BAIDUID_BFESS=C7DF70CBD0CFD117B1BD39F5F5493CC6:FG=1; delPer=0; PSINO=7; ZFY=nEW39pfO7kPx:BPBhaEOo:BSgkxaClSOlfiz1mPpOn9Qg:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=2k8gah2k000h840581a5ak0c1ii71no1o; BDUSS=F0Q01HZXpyN3hPNEd6U2lIR3RnS1NYOG9CdE9yaGN4QVQzcXhScjFEbzRGRXRsSVFBQUFBJCQAAAAAAAAAAAEAAAAkN87OQ2tzd3poAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADiHI2U4hyNlSl; H_PS_PSSID=39330_39396_39348_39407_39415_39438_39481_39477_39233_39406_26350_39425; bdindexid=4dt9jdc8073t2mkco5kg02n432; BCLID=11051545500894961340; BCLID_BFESS=11051545500894961340; BDSFRCVID=Lp0OJexroG0i0JJqKkT9rgHIJcpWxY5TDYrEOwXPsp3LGJLVFqB6EG0Pts1-dEu-S2EwogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=Lp0OJexroG0i0JJqKkT9rgHIJcpWxY5TDYrEOwXPsp3LGJLVFqB6EG0Pts1-dEu-S2EwogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRAOoC8-fIvDqTrP-trf5DCShUFs3bTtB2Q-XPoO3KJEhhc_KfRO35DXbP7ABtJjQ5bk_xbgy4op8P3y0bb2DUA1y4vp0JoGJeTxoUJ2-KDVeh5Gqq-KQJ-ebPRiJ-b9Qg-JbpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD89Dj-Ke5PVKgTa54cbb4o2WbCQJnTm8pcN2b5oQT8tD-6ZbxnWQN7H0hnYWJO2SPnXjqOUWJDkXpJvQnJjt2JxaqRC3tjIMl5jDh3MKToDb-oteltH36vy0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDH-OJ6tHfn3aQ5rtKRTffjrnhPF3QbjDXP6-hnjy3bR0opcF-lvOSb64bU7zy4tQ3p7ktl3Ry6r42-39LPO2hpRjyxv4QR_Yj4oxJpOJ-bCL0p5aHx8Kst3vbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC8ytC8KbKvYh4Oq2KCV-frb-C62aKDs5lnxBhcqJ-ovQT3EDMIpKtRWLUbH52bAaJOMQ-nZMfbeWJ5pXh8EMfQ02x3pb4jpKtjPJq5nhMJmKTLVbML0qJ-H0Rby523iob3vQpPMVhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjJbDH-HqTna--oa3RTeb6rjDnCrXb02XUI82h5y05O0tgQZQlvoQITKepnVy4b23nk4jJORXRj4B5vvbPOMthRnOlRKQRQIjxL1Db3Jb5_L5gTtsx8-343oepvoDPJc3Mv30-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SCD-tDKb3j; H_BDCLCKID_SF_BFESS=tRAOoC8-fIvDqTrP-trf5DCShUFs3bTtB2Q-XPoO3KJEhhc_KfRO35DXbP7ABtJjQ5bk_xbgy4op8P3y0bb2DUA1y4vp0JoGJeTxoUJ2-KDVeh5Gqq-KQJ-ebPRiJ-b9Qg-JbpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD89Dj-Ke5PVKgTa54cbb4o2WbCQJnTm8pcN2b5oQT8tD-6ZbxnWQN7H0hnYWJO2SPnXjqOUWJDkXpJvQnJjt2JxaqRC3tjIMl5jDh3MKToDb-oteltH36vy0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDH-OJ6tHfn3aQ5rtKRTffjrnhPF3QbjDXP6-hnjy3bR0opcF-lvOSb64bU7zy4tQ3p7ktl3Ry6r42-39LPO2hpRjyxv4QR_Yj4oxJpOJ-bCL0p5aHx8Kst3vbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC8ytC8KbKvYh4Oq2KCV-frb-C62aKDs5lnxBhcqJ-ovQT3EDMIpKtRWLUbH52bAaJOMQ-nZMfbeWJ5pXh8EMfQ02x3pb4jpKtjPJq5nhMJmKTLVbML0qJ-H0Rby523iob3vQpPMVhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0DjJbDH-HqTna--oa3RTeb6rjDnCrXb02XUI82h5y05O0tgQZQlvoQITKepnVy4b23nk4jJORXRj4B5vvbPOMthRnOlRKQRQIjxL1Db3Jb5_L5gTtsx8-343oepvoDPJc3Mv30-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SCD-tDKb3j; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1696827244; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04468397000RbAadSv2OSEq4hG6DPJeI2gkgpEvWXLF0kNKIAMWmxKF5ne56yDF6KOujj9LO6dqwoqH3hnw%2BLpWEvtF47OId526kqgJ2kCQWv6lqlpWpp%2FfW%2FqX6AnSemE0ACer%2BdHExb%2Fdt6O0P%2F4BVvzNZHieuY95ww%2BELa%2F5YpAPYh%2FaiB4JXrlZ%2B60dPTeCv4VQW22eJ6i%2FP2%2B%2Fp4wkGNrFro%2BCqs5JhR7EK1dSEvMbbRpMKd47QmHlAX4SUUtxU%2F%2FsIYlQobAeRPDHYz7BmG3Yvj9RSw%3D%3D19016925675818399240709192162529; __cas__rn__=446839700; __cas__st__212=bfae1c2c5c0e94294a4081ef9820d73e35fbf619154d7913546801e155ae1c339c4a931e6da59533fc96a9f2; __cas__id__212=46086365; CPTK_212=782396859; CPID_212=46086365; RT="z=1&dm=baidu.com&si=6f1ea65a-ce5e-4b5e-9c17-18df24c3b654&ss=lnif4e5q&sl=2&tt=1o5&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1696827274; ab_sr=1.0.1_YjY2MDk5MWFkNmRjYjhjYWQ2MmFjMmQ4M2Q3NzZjM2Y3ZGRkNzNjY2Y5YmZlNDNhZmE3ZjZkMWI2NDVhMWEzM2VjYTA2YzQ3NmE4NTNkZDQ3ZTU2Y2MwNzU2MDZiZTBlYzhiMjFiZmFkZDg5NWZiM2I4MmYxNDRlYzY3YjE4ZGVlN2NhMDU2YWYxYWViZGNjYzY0NWM5YWRkNjcyYzNjMQ==; BDUSS_BFESS=F0Q01HZXpyN3hPNEd6U2lIR3RnS1NYOG9CdE9yaGN4QVQzcXhScjFEbzRGRXRsSVFBQUFBJCQAAAAAAAAAAAEAAAAkN87OQ2tzd3poAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADiHI2U4hyNlSl'
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
        '{}\\baidu_index.csv'.format(new_folder_path), index=False)
    break
