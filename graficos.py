import plotly.express as px
import globals

def lineChart(dataframe, x, y, title, xaxis_title, yaxis_title, legendas = {}):
    fig = px.line(dataframe, x=x, y=y, title=title)

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title="Legenda",
    )

    if len(legendas) > 0:
        fig.for_each_trace(lambda t: t.update(name = legendas[t.name]))

    return fig

def barChart(dataframe, x, y, title, xaxis_title, yaxis_title):
    fig = px.bar(dataframe, x=x, y=y, title=title)

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title="Legenda",
    )

    return fig

def scatterChart(dataframe, x, y, title, xaxis_title, yaxis_title, color=None):
    fig = px.scatter(dataframe, x=x, y=y, title=title, color=color, trendline="ols", trendline_scope="overall", trendline_color_override="white")

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title="Legenda",
    )

    return fig
