import json
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import threading
import dash
import threading
import plotly.graph_objs as go
import pandas as pd


latest_data = {
    'latitude': 35.38848046107848,
    'longitude': 139.4269932869966,
    'smile_degree': 0,
}
def compute_text_color(value):
    r = int(value * 255 / 100)
    b = 255 - r
    return f'rgb({r},0,{b})'

def get_smile_emoji(smile_value):
    if smile_value < 20:
        return "😐"
    elif smile_value < 40:
        return "🙂"
    elif smile_value < 60:
        return "😀"
    elif smile_value < 80:
        return "😃"
    else:
        return "😄"
    
# def get_smile_emoji(smile_value):
#     if smile_value < 20:
#         return u"\u1F610"  # 😐
#     elif smile_value < 40:
#         return u"\u1F642"  # 🙂
#     elif smile_value < 60:
#         return u"\u1F600"  # 😀
#     elif smile_value < 80:
#         return u"\u1F603"  # 😃
#     else:
#         return u"\u1F604"  # 😄







# #Set up Map
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-map'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000,  # 1秒毎に更新
            n_intervals=0
    )
])

@app.callback(
    Output('live-map', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_live_map(n):
    # if not latest_data['latitude']:  # データがまだ設定されていない場合の処理
    #     return dash.no_update
    data = pd.DataFrame({
        '緯度': [35.38848046107848, 35.388062, 35.387716,35.388383,35.388718,35.388488,35.388237,35.387775,35.389070,35.388274,35.388821,35.387115,35.389131,35.387231,35.387607,35.387476,35.388788,35.388079],
        '経度': [139.4269932869966, 139.426193, 139.426117,139.426367,139.426391,139.427976,139.425490,139.427772,139.425664,139.427187,139.427477,139.425986,139.426669,139.427029,139.427356,139.428268,139.428080,139.428118
],
        '笑顔度😄': [100,23,0,100,50,80,30,40,60,70,90,10,80,100,11,50,30,78],
        'label':["諭吉像前","ε館","κ館","℩館","ο館","A館","Δ館","Ω館","τ館","図書館","Θ館","Σ館","Γ館","鴨池前","サブウェイ","バス停前","駐車場","大学出入口"]
    })

    fig = go.Figure()

    # for idx, row in data.iterrows():
    #     color = compute_text_color(row["笑顔度😄"])
    #     fig.add_trace(go.Scattermapbox(
    #         lat=[row["緯度"]],
    #         lon=[row["経度"]],
    #         mode='markers+text',

    #         text=row["label"],
    #         textposition="top right",
    #         textfont=dict(color=color)
    #     ))


    colors = data["笑顔度😄"].apply(compute_text_color).tolist()
    smile_emojis = data["笑顔度😄"].apply(get_smile_emoji).tolist()
    print(smile_emojis)
    print(colors)

    # マーカーを表示
    marker_sizes = [10 + (x / 3) for x in data["笑顔度😄"]]  # 笑顔度が高いほどマーカーサイズを大きくする

    max_size = 25
    min_size = 10
    sizes = [min_size + (x/100)*(max_size - min_size) for x in data["笑顔度😄"]]
    frames = [go.Frame(data=[go.Scattermapbox(marker=dict(size=[s + (1 if (i%2)==0 else -1)*5 for s in sizes]))]) for i in range(10)]



    emoji_url = "./assets/images/flowers/roseA001.png"

    fig.add_trace(go.Scattermapbox(
        lat=data["緯度"],
        lon=data["経度"],
        mode='markers+text',
        #textfont=dict(family="Arial, sans-serif"),  # このフォントが絵文字をサポートしているかどうかを確認
        #textfont=dict(family="Apple Color Emoji"),  # MacOSでの絵文字サポートフォント
        textfont=dict(),
        text=[f"笑顔度😄: {smile_degree}" for smile_degree in data["笑顔度😄"]],

        marker=go.scattermapbox.Marker(
            size=marker_sizes,  # 笑顔度に応じてサイズを変更
            color=colors,
            colorscale=[(0, 'blue'), (1, 'red')],
            cmin=0,
            cmax=100,
            colorbar=dict(title="笑顔度😄"),
        ),

        #text=[f"{label}<br>笑顔度😄: {smile_degree} {emoji}" for label, smile_degree, emoji in zip(data["label"], data["笑顔度😄"], smile_emojis)],
        # textfont=dict(
        #     family="Arial, sans-serif",  # フォントファミリー
        #     size=14,  # フォントサイズ
        #     color="black"  # テキストカラー
        # ),
        #hoverinfo='none',
        hovertemplate="<b></b><br>笑顔度😄: %<extra></extra>",
        textposition="top right",

    ))
    fig.update_layout(
        title="笑顔度😄の分布マップ",
        mapbox_style="carto-positron",
        height=900, 
        width=1500
    )
    fig.frames = frames
    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)])])])


    fig.update_layout(mapbox_style="carto-positron", height=900, width=1500)
    fig.update_layout(mapbox_zoom=16.9, mapbox_center={"lat": latest_data['latitude'], "lon": latest_data['longitude']})

    return fig


def run_dash_app():
    app.run_server(debug=True)

run_dash_app()

