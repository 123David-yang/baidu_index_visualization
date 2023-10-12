from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
from pyecharts.faker import Faker
import pandas as pd
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import numpy as np


# df = pd.read_csv("baidu.csv", encoding='gbk')
df = pd.read_csv('data_all.csv', encoding='utf-8')
df = df.loc[(df.keyword == '财神') & (df['type'] == 'all'),
            ['province', 'keyword', 'year', 'mean']]
print(df.head())


provinces = ['山东省', '贵州省', '江西省', '重庆市', '内蒙古自治区', '湖北省', '辽宁省', '湖南省', '福建省', '上海市', '北京市', '广西壮族自治区', '广东省', '四川省', '云南省', '江苏省',
             '浙江省', '青海省', '宁夏回族自治区', '河北省', '黑龙江省', '吉林省', '天津市', '陕西省', '甘肃省', '新疆维吾尔自治区', '河南省', '安徽省', '山西省', '海南省', '台湾省', '西藏自治区', '香港特别行政区']


def change_province_name(x):
    for i in provinces:
        if i.startswith(x):
            return i


df['province'] = df['province'].apply(lambda x: change_province_name(x))


def timeline_map(df, descri='mean', step=0.2, keyword='财神'):
    df = df.loc[(df['keyword'] == keyword)]
    visualmap_data = []
    for i in np.arange(0, 1 + step, step):
        visualmap_data.append(df[descri].quantile(i))
    print(visualmap_data)
    print(df['mean'].max())
    # 切分多期数据
    data_list = []
    for year in range(df.year.min(), df.year.max() + 1):
        data_list.append(df.loc[df.year == year, ['province', 'year', descri]])
    tl = Timeline(init_opts=opts.InitOpts(page_title='',
                                          theme=ThemeType.CHALK,
                                          width='1000px', height='620px'))

    for data in data_list:
        year = data.year.unique()[0]
        data.drop(['year'], axis=1, inplace=True)
        f_map = (
            Map(init_opts=opts.InitOpts(width='900px',
                                        height='500px',
                                        page_title='',
                                        bg_color=None))
            .add(series_name=keyword,
                 data_pair=data[['province', descri]].values.tolist(),
                 maptype='china',
                 is_map_symbol_show=False)
            .set_global_opts(
                title_opts=opts.TitleOpts(title='全国各省级行政区{}百度指数'.format(keyword),
                                          pos_left='center',),
                legend_opts=opts.LegendOpts(
                    is_show=True, pos_top="40px", pos_right="30px"),
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True, range_text=['高', '低'], pieces=[
                        {"min": visualmap_data[4],
                            "max": visualmap_data[5], "color": "#751d0d"},
                        {"min": visualmap_data[3],
                            "max": visualmap_data[4], "color": "#ae2a23"},
                        {"min": visualmap_data[2],
                            "max": visualmap_data[3], "color": "#d6564c"},
                        {"min": visualmap_data[1],
                            "max": visualmap_data[2], "color": "#f19178"},
                        {"min": visualmap_data[0], "max": visualmap_data[1], "color": "#f7d3a6"}]),
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                             markpoint_opts=opts.MarkPointOpts(
                symbol_size=[90, 90], symbol='circle'),
                effect_opts=opts.EffectOpts(is_show='True',)
            )
        )
        tl.add(f_map, "{}年".format(year))
        tl.add_schema(is_timeline_show=True,
                      play_interval=1000,
                      symbol=None,
                      is_loop_play=True)
    return tl


timeline_map(df).render("map_caishen.html")

# # c = (
# #     Map()
# #     .add("商家A", [list(z) for z in zip(Faker.provinces, Faker.values())], "china")
#     .set_global_opts(title_opts=opts.TitleOpts(title="Map-基本示例"))
#     .render("map_base.html")
# )

# d = (
#     Map()
#     .add("2019年财神信仰各省虔诚度", df_2021.values.tolist(), "china")
#     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#     .set_global_opts(
#         visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="Geo-基本示例")
#     )
#     .render("map_caishen.html")

# )
# # print([list(z) for z in zip(Faker.provinces, Faker.values())])
# # print(df.province.unique().tolist())


# https: // www.maigoo.com / news / 480576.html
