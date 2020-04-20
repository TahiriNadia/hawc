import base64
import io
import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table


from django_plotly_dash import DjangoDash

import pandas as pd


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = DjangoDash("BubblePlot", external_stylesheets=external_stylesheets)

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

app.layout = html.Div(
    [
        html.H5("Select y-axis"),
        dcc.Dropdown(id="y-dropdown", options=[]),
        html.H5("Select x-axis"),
        dcc.Dropdown(id="x-dropdown", options=[]),
        dcc.Graph(id="Mygraph"),
        dash_table.DataTable(
            id="datatable-upload-container",
            style_cell={
                "fontSize": 14,
                "font-family": "arial",
                "minWidth": "0px",
                "maxWidth": "350px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
            style_table={"overflowX": "scroll"},
            # fixed_rows={ 'headers': True, 'data': 0 }
        ),
        html.Div(id="none", children=[], style={"display": "none"}),
        html.Div(id="sessionstate", children=[]),
    ]
)


@app.expanded_callback(Output("sessionstate", "children"), [Input("none", "children")])
def update_session_state(*args, **kwargs):
    return str(kwargs["session_state"])


# update y-dropdown
@app.expanded_callback(Output("x-dropdown", "options"), [Input("none", "children")])
def update_y_dropdown(*args, **kwargs):
    return [{"label": k, "value": k} for k in kwargs["session_state"][0].keys()]


# update x-dropdown
@app.expanded_callback(Output("y-dropdown", "options"), [Input("none", "children")])
def update_x_dropdown(*args, **kwargs):
    return [{"label": k, "value": k} for k in kwargs["session_state"][0].keys()]


@app.expanded_callback(
    Output("Mygraph", "figure"), [Input("x-dropdown", "value"), Input("y-dropdown", "value"),],
)
def update_graph(xaxis, yaxis, **kwargs):
    fig = {"layout": go.Layout(plot_bgcolor=colors["graphBackground"], paper_bgcolor=colors["graphBackground"])}

    if not xaxis or not yaxis:
        return fig
    df = pd.DataFrame(kwargs["session_state"])
    df = df[pd.notnull(df[xaxis])]
    df = df[pd.notnull(df[yaxis])]
    df = df.groupby([xaxis, yaxis], sort=False).size().reset_index(name="freq")
    df["binned"] = pd.cut(np.array(df["freq"]), 5, precision=0)
    legend = pd.DataFrame(df["binned"].unique(), columns=["binned"])
    legend["binned"] = legend["binned"].astype("str")
    legend = legend["binned"].str.split(", ", n=1, expand=True)
    legend = legend[1].str.split("]", n=1, expand=True)
    legend = legend[0].str.split(".0", n=1, expand=True)
    legend[0] = legend[0].astype("str")
    legend[0] = legend[0].astype("float")
    yval = list(legend[0])
    legend = pd.DataFrame(yval, columns=["yaxis"])
    legend["xaxis"] = 1.5
    legend2 = pd.DataFrame({"yaxis": [df["freq"].min()], "xaxis": [1.5]})
    legend = legend.append(legend2)
    fig = make_subplots(
        rows=1,
        cols=10,
        specs=[[{"colspan": 8}, None, None, None, None, None, None, None, None, {}]],
        subplot_titles=("Bubble Plot", "Legend (Count)"),
    )
    # Bubble plot code
    fig.add_trace(
        go.Scatter(
            x=df[xaxis],
            y=df[yaxis],
            text=df["freq"],
            mode="markers",
            marker=dict(
                size=df["freq"],
                sizemode="area",
                sizeref=4.0 * max(df["freq"]) / (40.0 ** 2),
                sizemin=2,
                color=df["freq"],
                showscale=False,
            ),
            hovertemplate="%{xaxis.title.text} : %{x}" + "<br>%{yaxis.title.text} : %{y}<br>" + "Count: %{text}",
        ),
        row=1,
        col=1,
    )

    fig.update_xaxes(
        linecolor="lightgrey",
        gridcolor="lightgrey",
        # showticklabels = True,
        #   type = 'category',
        showgrid=True,
        zeroline=True,
        showline=True,
        mirror=True,
        automargin=True,
        title_standoff=25,
        dtick=1,
        title_text=xaxis,
        row=1,
        col=1,
    )

    fig.update_yaxes(
        linecolor="lightgrey",
        gridcolor="lightgrey",
        showgrid=True,
        zeroline=True,
        showline=True,
        automargin=True,
        mirror=True,
        dtick=1,
        title_text=yaxis,
        #  title_standoff = 70,
        tickangle=0,
        row=1,
        col=1,
    )

    # Legend figure code
    fig.add_trace(
        go.Scatter(
            x=legend["xaxis"],
            y=legend["yaxis"],
            mode="markers",
            marker=dict(
                size=legend["yaxis"],
                sizemode="area",
                sizeref=4.0 * max(legend["yaxis"]) / (40.0 ** 2),
                sizemin=2,
                color=legend["yaxis"],
                showscale=True,
            ),
            hoverinfo="none",
        ),
        row=1,
        col=10,
    )

    fig.update_xaxes(
        zeroline=True,
        showline=False,
        showticklabels=False,
        showgrid=False,
        tick0=1,
        range=[1, 2],
        rangemode="normal",
        row=1,
        col=10,
    )

    fig.update_yaxes(showgrid=False, zeroline=True, tickvals=legend["yaxis"], row=1, col=10)  # [0:6],

    fig.update_layout(
        plot_bgcolor="white",
        showlegend=False,
        #    height = 1300, width = 1300,
        font=dict(family="Courier New, monospace", size=18, color="black"),
    )
    return fig
