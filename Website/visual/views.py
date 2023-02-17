from operator import truediv
from django_echarts.entities import Jumbotron, LinkItem
from django_echarts.starter.sites import DJESite, SiteOpts
from django.urls import reverse_lazy
from pyecharts import options as opts
from django_echarts.geojson import use_geojson, geojson_url
from pyecharts.charts import Kline
from pyecharts.charts import Bar3D
from pyecharts.charts import Sankey, Map



from static.AnualEPS import listYearFirmEPS, TOP5_EQUITY_EPS
from static.histdatascrape import Techlist, Finlist
import pandas as pd


site_obj = DJESite(
    site_title='Mini Honours Project',
    
    opts=SiteOpts(
        list_layout='grid',
        nav_shown_pages=[],
        paginate_by=10,
        #detail_tags_position = 'bottom'
    )
)

site_obj.nav.add_menu(text='About', slug='about', url=reverse_lazy('dje_home'))

site_obj.add_widgets(
    jumbotron=Jumbotron('S&P 500 data visualistion', main_text='mini group project - University of Edinburgh', small_text='10/2022'),
)

site_obj.add_right_link(
    LinkItem(text='Project Repo', url='https://github.com/YongjiangChen/miniProject', new_page=True)
).add_left_link(LinkItem(text='Dashboard', url='/dashboard/'))
site_obj.add_left_link(LinkItem(text='Dashboard2', url='/dashboard2/'))

candleStickDescription = 'This Chart displays prices in real-time, you may click/scroll to move/zoom. The S&P 500® Information Technology comprises those companies included in the S&P 500 that are classified as members of the GICS information technology sector.'
candleStickDescription2 = 'This Chart displays prices in real-time, you may click/scroll to move/zoom. The S&P 500 Financials comprises those companies included in the S&P 500 that are classified as members of the GICS financials sector.'

#########################################################################################################
#make-up data, need to append real data from json dictionary to list of lists.
# [open, close, lowest, highest] 
prices = [[2320.26, 2320.26, 2287.3, 2362.94]]
columnAverage = [sum(priceList) / len(priceList) for priceList in zip(*prices)],
max_value = max(sublist[0] for sublist in prices)
###########################################################################################################



def findDay(theList, price):
    for ind in range(len(theList)):
        if price in theList[ind]:
            return ind

max_value_day = findDay(prices, max_value)
#print(max_value_day)

timeAxis = []
for i in range(9,17):
    if i == 9:
        for j in range(30,60,5):
            timeAxis.append(str(i)+":"+str(j))
    elif i>9 and i<16:
        for j in range(0,60,5):
            timeAxis.append(str(i)+":"+str(j))
    else:
        for j in range(0,35,5):
            timeAxis.append(str(i)+":"+str(j))


@site_obj.register_chart(title='Intraday prices for S&P 500 Information Technology Sector', description = candleStickDescription, catalog='Data Visualisation')
def mytechchart():
    candleStick = Kline().add_xaxis(
        [timeAxis[i] for i in range(len(Techlist))]
    ).add_yaxis(
        'Candlestick Prices', Techlist, itemstyle_opts=opts.ItemStyleOpts(color="#8fce00", color0="#ff3a3a", border_color="#8fce00", border_color0="#ff3a3a"),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="INDEXSP: SP500-45", subtitle="Time interval: 5-min"),
        datazoom_opts=opts.DataZoomOpts(is_show = True, type_ = "inside", orient = "horizontal", range_start=1, range_end=200)).set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_ = 'average', value_dim='close', name="Close Price Average",)
                #opts.MarkLineItem(y=columnAverage[0][1], name="Overall Close Price Average",)
            ],
            linestyle_opts=opts.LineStyleOpts( width = 2, type_ = "dashed", color="#5b5b5b")
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='max', value_dim='highest',  value=max_value, symbol_size=[80,50], name="Highest Price", itemstyle_opts=opts.ItemStyleOpts(color="#5b5b5b")),
                #opts.MarkPointItem(coord=(max_value_day,max_value), value=max_value, symbol_size=[80,50], name="Overall Highest Price"),
            ]
        ),
    )
    return candleStick

@site_obj.register_chart(title='Intraday prices for S&P 500 Financials Sector', description = candleStickDescription2, catalog='Data Visualisation')
def myfinchart():
    candleStick2 = Kline().add_xaxis(
        [timeAxis[i] for i in range(len(Techlist))]
    ).add_yaxis(
        'Candlestick Prices', Finlist, itemstyle_opts=opts.ItemStyleOpts(color="#8fce00", color0="#ff3a3a", border_color="#8fce00", border_color0="#ff3a3a"),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="INDEXSP: SP500-40", subtitle="Time interval: 5-min"),
        datazoom_opts=opts.DataZoomOpts(is_show = True, type_ = "inside", orient = "horizontal", range_start=1, range_end=200)).set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_ = 'average', value_dim='close', name="Close Price Average",)
                #opts.MarkLineItem(y=columnAverage[0][1], name="Overall Close Price Average",)
            ],
            linestyle_opts=opts.LineStyleOpts( width = 2, type_ = "dashed", color="#5b5b5b")
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='max', value_dim='highest',  value=max_value, symbol_size=[80,50], name="Highest Price", itemstyle_opts=opts.ItemStyleOpts(color="#5b5b5b")),
                #opts.MarkPointItem(coord=(max_value_day,max_value), value=max_value, symbol_size=[80,50], name="Overall Highest Price"),
            ]
        ),
    )
    return candleStick2

description3D = "This page illustrate the EPS change in the TOP 5 S&P 500 entities over past 10 years, together they make up 17.5% of the S&P 500"

#years = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]
equities = ["Apple", "Microsoft", "Alphabet", "Amazon", "Meta"]

@site_obj.register_chart(title='Earnings per share', description = description3D, catalog='Data Visualisation')
def Bar3Dchart():
    c=(
    Bar3D(init_opts=opts.InitOpts(width="900px", height="600px", bg_color="#f3f6f4",))
    .add(
        series_name="Earnings Per Share",
        #data=listYearFirmEPS,
        data = TOP5_EQUITY_EPS,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", name='Years',),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=equities, name='Top 5 Entities in S&P500', name_gap =40),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name='EPS'),
        grid3d_opts=opts.Grid3DOpts(is_rotate=True)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="3D Visualistion for change in Profitability", subtitle="Unit: USD"),
        visualmap_opts=opts.VisualMapOpts(
            max_=20,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )

)
    return c

def get_data(df):
    nodes =[]
    for i in range(2):
        vales=df.iloc[:,i].unique()
        for value in vales:
            dic={}
            dic['name']=value
            nodes.append(dic)
             
    nodes1 = []
    for id in nodes:
        if id not in nodes1:
            nodes1.append(id)
 
    links=[]
    for i in df.values:
        dic={}
        dic['source']=i[0]
        dic['target']=i[1]
        dic['value']=i[2]
        links.append(dic)
    print(links)
    return nodes1,links

nodes_list = [
 {'name': 'increase in NAHB Housing Market Index'},
 {'name': 'increase in 3-Month Bill Auction'},
 {'name': 'increase in 6-Month Bill Auction'},
 {'name': 'increase in Crude Oil Inventories'},
 {'name': 'rise in U.S. 20-Year Bond Auction'},
 {'name': 'increase in Initial Jobless Claims'},
 {'name': 'decrease in Natural Gas Storage'},
 {'name': 'US FOMC meeting'},
 {'name': 'Confidence for a  bull market'},
 {'name': 'Confidence for a  bear market'},
 {'name': 'Decrease in monthly PCE Price index'},
 {'name': 'Decrease in monthly New Home Sales'},
 {'name': 'Decrease in CB Consumer Confidence'},
 {'name': 'Decrease in monthly Gasoline production'},
 {'name': 'Decreas in US Producer Price Index'},
 {'name': 'Increase in US Consumer Price Index'},
 {'name': 'Bearish historical data input'},
 {'name': 'Bullish historical data input'},
 {'name': 'Drop in Gold Futures'},
 {'name': 'change in data input range'},
 {'name': 'Model A'},
 {'name': 'Model C'},
 {'name': 'Model D'},
 {'name': 'Model B'}
]

links_list = [
 {'source': 'Confidence for a  bull market', 'target': 'Model A', 'value': 80},
 {'source': 'Confidence for a  bull market', 'target': 'Model B', 'value': 95},
 {'source': 'Confidence for a  bull market', 'target': 'Model C', 'value': 91},
 {'source': 'Confidence for a  bull market', 'target': 'Model D', 'value': 92},
 {'source': 'Confidence for a  bear market', 'target': 'Model A', 'value': 20},
 {'source': 'Confidence for a  bear market', 'target': 'Model B', 'value': 5},
 {'source': 'Confidence for a  bear market', 'target': 'Model C', 'value': 9},
 {'source': 'Confidence for a  bear market', 'target': 'Model D', 'value': 8},
 {'source': 'Model A', 'target': 'increase in NAHB Housing Market Index', 'value': 10},
 {'source': 'Model A', 'target': 'increase in 3-Month Bill Auction', 'value': 5},
 {'source': 'Model A', 'target': 'increase in 6-Month Bill Auction', 'value': 3},
 {'source': 'Model A', 'target': 'rise in U.S. 20-Year Bond Auction', 'value': 25},
 {'source': 'Model A', 'target': 'Decrease in monthly Gasoline production', 'value': 30},
 {'source': 'Model A', 'target': 'increase in NAHB Housing Market Index', 'value': 13},
 {'source': 'Model A', 'target': 'Decrease in monthly PCE Price index', 'value': 7},
 {'source': 'Model B', 'target': 'Drop in Gold Futures', 'value': 27},
 {'source': 'Model B', 'target': 'Bullish historical data input', 'value': 13},
 {'source': 'Model B', 'target': 'rise in U.S. 20-Year Bond Auction', 'value': 26},
 {'source': 'Model B', 'target': 'increase in Crude Oil Inventories', 'value': 40},
 {'source': 'Model C', 'target': 'change in data input range', 'value': 14},
 {'source': 'Model C', 'target': 'Bearish historical data input', 'value': 16},
 {'source': 'Model C', 'target': 'Increase in US Consumer Price Index', 'value': 8},
 {'source': 'Model C', 'target': 'Decreas in US Producer Price Index', 'value': 2},
 {'source': 'Model D', 'target': 'Decrease in CB Consumer Confidence', 'value': 1},
 {'source': 'Model D', 'target': 'US FOMC meeting', 'value': 9},
 {'source': 'Model D', 'target': 'rise in U.S. 20-Year Bond Auction', 'value': 17},
 {'source': 'Model D', 'target': 'Increase in US Consumer Price Index', 'value': 25},
 {'source': 'Model D', 'target': 'decrease in Natural Gas Storage', 'value': 30},
 {'source': 'Model D', 'target': 'Decrease in monthly New Home Sales', 'value': 5}

]

@site_obj.register_chart(title='Sankey diagram for model comparison',  catalog='Data Visualisation')
def get_tu():
    sankey = (
        Sankey(init_opts=opts.InitOpts(width="1500px", height="600px"))
        .add(
            "",
            nodes_list,
            links_list,
            pos_top="10%",
            node_width = 30,  
            node_gap= 12, 
            is_draggable = True,
            is_selected = True,
            layout_iterations = 5,
            # focus_node_adjacency=True,
            itemstyle_opts=opts.ItemStyleOpts(border_width=2, border_color="#aaa"),
            linestyle_opt=opts.LineStyleOpts(opacity=0.8, curve=0.5, color='source'),
            label_opts=opts.LabelOpts(position='top', color="#fe6f5e"),

            
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Effects of economic events to the model predictions", 
                pos_bottom="0%",
                title_textstyle_opts=opts.TextStyleOpts(color="#fe6f5e")
                )
        )

    )
    return sankey

from pyecharts.charts import Bar, Grid, Line

bar = (
    Bar()
    .add_xaxis(["{}/2".format(i) for i in range(1, 13)])
    .add_yaxis(
        "price",
        [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
        yaxis_index=0,
        color="#d14a61",
    )
    .add_yaxis(
        "events",
        [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
        yaxis_index=1,
        color="#5793f3",
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="events",
            type_="value",
            min_=0,
            max_=250,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ABC"),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="",
            min_=0,
            max_=25,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} USD"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="events importance",
            min_=0,
            max_=250,
            position="right",
            offset=80,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} DEF"),
        ),
        title_opts=opts.TitleOpts(title="Grid-Overlap"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(pos_left="25%"),
    )
)

line = (
    Line()
    .add_xaxis(["{}/2".format(i) for i in range(1, 13)])
    .add_yaxis(
        "events sentiments",
        [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
        yaxis_index=2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
    )
)

overlap_1 = bar.overlap(line)

line1 = (
    Line()
    .add_xaxis(["{}/2".format(i) for i in range(1, 13)])
    .add_yaxis(
        " ",
        [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
        yaxis_index=2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
    )
)

@site_obj.register_chart(title='diagram overlay',  catalog='Data Visualisation')
def compo():
    grid = (
        Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
        .add(
            overlap_1, grid_opts=opts.GridOpts(pos_right="58%"), is_control_axis_index=True
        )
        .add(
            line1, grid_opts=opts.GridOpts(pos_left="58%"), is_control_axis_index=True
        )
    )
    return grid

    




