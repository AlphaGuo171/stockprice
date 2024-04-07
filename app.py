from flask import Flask, render_template, request
import pandas as pd
import akshare as ak
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.io as pio
pio.templates.default = "plotly"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_code = request.form.get('stock_code')
        try:
            data = ak.stock_cyq_em(symbol=stock_code, adjust="")
            price = ak.stock_zh_a_spot_em()
            cost_price = price.loc[price['代码']==stock_code]['最新价'].item()
            
            df = pd.DataFrame(data)
            df['日期'] = pd.to_datetime(df['日期'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['日期'], y=df['平均成本'], mode='lines', name='平均成本'))
            fig.add_trace(go.Scatter(x=df['日期'], y=df['90成本-低'], mode='lines', name='90成本-低'))
            fig.add_trace(go.Scatter(x=df['日期'], y=df['90成本-高'], mode='lines', name='90成本-高'))
            fig.add_trace(go.Scatter(x=df['日期'], y=df['70成本-低'], mode='lines', name='70成本-低'))
            fig.add_trace(go.Scatter(x=df['日期'], y=df['70成本-高'], mode='lines', name='70成本-高'))

            cost_line = go.Scatter(x=df['日期'], y=[cost_price] * len(df['日期']), mode='lines', line=dict(color='red', dash='dash'), name='现价')
            fig.add_trace(cost_line)

            fig.update_layout(
                xaxis_title='日期',
                yaxis_title='成本',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                ),
                margin=dict(t=40, l=20, r=20, b=20),  # 调整边距以适应小屏幕
                hovermode='closest',  # 改善移动设备上的悬停体验
                autosize=True  # 图表将自动调整大小以适应容器
            )

            # 调整字体大小以适应移动设备
            fig.update_layout(
                font=dict(
                    size=10
                )
            )

            # 输出图表
            plot_div = plot(fig, output_type='div', include_plotlyjs=True)
            return render_template('index.html', plot_div=plot_div, stock_code=stock_code)
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
