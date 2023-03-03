import pandas as pd
from pyecharts.charts import Kline, Line
from pyecharts import options as opts


def plot_kline(data, name, buy_sell):
    # buy_sell 是一个包含四个列表的列表
    # [['2022-07-07', '2022-07-13', '2022-08-04', '2022-08-15', '2022-08-26', '2022-11-01', '2022-12-07', '2022-12-19'],
    # [8.31, 8.74, 9.77, 9.01, 8.51, 8.02, 8.16, 7.95],
    # ['2022-07-12', '2022-07-14', '2022-08-05', '2022-08-19', '2022-10-20', '2022-12-06', '2022-12-08', '2023-01-06'],
    # [8.56, 9.1, 9.28, 9.6, 2, 8.37, 8.1, 8.14, 8.66]]
    # 分别是买入日期，买入时高价，卖出日期，卖出时高价，其中高价用来做买卖标记的纵坐标

    # name就是股票名

    # data是取tushare中的数据，并计算添加了画图需要的MA30，UP布林线，LOW布林线，MIDDLE布林线数据
    # 修改了data中trade_info各式
    # trade_info['trade_date'] = pd.to_datetime(trade_info['trade_date'], format='%Y%m%d').apply(lambda x: x.strftime('%Y-%m-%d'))
    # trade_info = trade_info.set_index('trade_date')
    buy_date = buy_sell[0]
    buy_high = buy_sell[1]
    sell_date = buy_sell[2]
    sell_high = buy_sell[3]
    add_date = buy_sell[4]
    add_high = buy_sell[5]
    minus_date = buy_sell[6]
    minus_high = buy_sell[7]
    stopwin_date = buy_sell[8]
    stopwin_high = buy_sell[9]
    stoploss_date = buy_sell[10]
    stoploss_high = buy_sell[11]
    kline = (
        Kline(init_opts=opts.InitOpts(width="1350px", height="500px"))  # 设置画布大小
        .add_xaxis(xaxis_data=list(data.index))  # 将原始数据的index转化为list作为横坐标
        .add_yaxis(series_name="k线", y_axis=data[["open", "close", "low", "high"]].values.tolist(),
                   # 纵坐标采用OPEN、CLOSE、LOW、HIGH，注意顺序
                   itemstyle_opts=opts.ItemStyleOpts(color="#c61328", color0="#223b24"), )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, pos_bottom=0, pos_left="center", orient='horizontal'),
                         datazoom_opts=[
                             opts.DataZoomOpts(
                                 is_show=False,
                                 type_="inside",
                                 xaxis_index=[0],
                                 range_start=50,
                                 range_end=100,
                             ),
                             opts.DataZoomOpts(
                                 is_show=False,
                                 xaxis_index=[0],
                                 type_="slider",
                                 pos_top="10%",
                                 range_start=50,
                                 range_end=100,
                             ),
                         ],
                         yaxis_opts=opts.AxisOpts(
                             is_scale=True,
                             splitarea_opts=opts.SplitAreaOpts(
                                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                             ),
                         ),
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="cross",
                             background_color="rgba(245, 245, 245, 0.8)",
                             border_width=1,
                             border_color="#ccc",
                             textstyle_opts=opts.TextStyleOpts(color="#000"),
                         ),
                         visualmap_opts=opts.VisualMapOpts(
                             is_show=False,
                             dimension=2,
                             series_index=5,
                             is_piecewise=True,
                             pieces=[
                                 {"value": 1, "color": "#00da3c"},
                                 {"value": -1, "color": "#ec0000"},
                             ],
                         ),
                         axispointer_opts=opts.AxisPointerOpts(
                             is_show=True,
                             link=[{"xAxisIndex": "all"}],
                             label=opts.LabelOpts(background_color="#777"),
                         ),
                         brush_opts=opts.BrushOpts(
                             x_axis_index="all",
                             brush_link="all",
                             out_of_brush={"colorAlpha": 0.1},
                             brush_type="lineX",
                         ),
                         title_opts=opts.TitleOpts(
                             title=name,
                             pos_left='center',
                             title_textstyle_opts=opts.TextStyleOpts(
                                 font_size=30
                             )),
                         )
    )

    line = (Line()
    .add_xaxis(xaxis_data=list(data.index))
    .add_yaxis(
        series_name="UP",
        y_axis=data["upper"].tolist(),
        # xaxis_index=1,
        # yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name="MID",
        y_axis=data["middle"].tolist(),
        # xaxis_index=1,
        # yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name="LOW",
        y_axis=data["lower"].tolist(),
        # xaxis_index=1,
        # yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(
        series_name="MA30",
        y_axis=data["ma30"].tolist(),
        # xaxis_index=1,
        # yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
    ))

    for i in range(0, len(buy_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[buy_date[i], buy_high[i]], name='test', value='买',
                                       itemstyle_opts={'color': '#f75d06'}),
                ]
            ), )
    for i in range(0, len(sell_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[sell_date[i], sell_high[i]], name='test', value='卖',
                                       itemstyle_opts={'color': '#08a2f9'}),
                ]
            ), )
    for i in range(0, len(stopwin_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[stopwin_date[i], stopwin_high[i]], name='test', value='赢',
                                       itemstyle_opts={'color': '#F53D3D'}),
                ]
            ), )
    for i in range(0, len(stoploss_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[stoploss_date[i], stoploss_high[i]], name='test', value='损',
                                       itemstyle_opts={'color': '#3FFF3F'}),
                ]
            ), )
    for i in range(0, len(add_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[add_date[i], add_high[i]], name='test', value='加',
                                       itemstyle_opts={'color': '#B53D3D'}),
                ]
            ), )
    for i in range(0, len(minus_date)):
        kline.add_yaxis(
            series_name="买卖",
            y_axis="",
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(coord=[minus_date[i], minus_high[i]], name='test', value='减',
                                       itemstyle_opts={'color': '#4AC2C2'}),
                ]
            ), )


    kline.overlap(line)
    # kline.render("kline.html")
    return kline
    #     #导出成html文件


# buysell = [
#     ['2022-07-07', '2022-07-13', '2022-08-04', '2022-08-15', '2022-08-26', '2022-11-01', '2022-12-07', '2022-12-19'],
#     [8.31, 8.74, 9.77, 9.01, 8.51, 8.02, 8.16, 7.95],
#     ['2022-07-12', '2022-07-14', '2022-08-05', '2022-08-19', '2022-10-20', '2022-12-06', '2022-12-08', '2023-01-06'],
#     [8.56, 9.1, 9.28, 9.6
#         , 2, 8.37, 8.1, 8.14, 8.66]]
# trade_info = pd.read_csv('windata' + str(False) + '\\' + '300933SZ' + '.csv')
# trade_info['trade_date'] = pd.to_datetime(trade_info['trade_date'], format='%Y%m%d').apply(
#     lambda x: x.strftime('%Y-%m-%d'))
# trade_info = trade_info.set_index('trade_date')
# plot_kline(trade_info, 'lll', buysell)
