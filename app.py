from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from data_prep import load_data

app = Dash(__name__)
server = app.server
df = load_data()

COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#f97316",
    "text": "#f1f5f9",
    "subtext": "#94a3b8"
}

MONTH_NAMES = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
               7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
MONTH_SHORT = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
TEMPLATE = "plotly_dark"
DAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

app.layout = html.Div(style={"backgroundColor": COLORS["bg"],
                              "minHeight": "100vh", "padding": "40px"}, children=[

    # ── HEADER ───────────────────────────────────────────────────────────────
    html.Div(style={"textAlign": "center", "marginBottom": "48px",
                    "paddingTop": "48px", "paddingBottom": "28px",
                    "borderBottom": "1px solid rgba(249,115,22,0.15)"}, children=[

        html.P("CHICAGO · 2025", style={
            "color": COLORS["accent"],
            "fontSize": "13px",
            "letterSpacing": "6px",
            "fontWeight": "700",
            "marginBottom": "16px",
            "textTransform": "uppercase"
        }),

        html.H1([
            html.Span("Chicago Crime", style={
                "display": "block",
                "fontSize": "96px",
                "fontWeight": "800",
                "letterSpacing": "-3px",
                "lineHeight": "1",
                "color": COLORS["text"]
            }),
            html.Span("DASHBOARD", style={
                "display": "block",
                "fontSize": "96px",
                "fontWeight": "300",
                "letterSpacing": "16px",
                "lineHeight": "1.1",
                "color": COLORS["accent"],
                "textTransform": "uppercase"
            }),
        ], style={"margin": "0 0 24px 0"}),

        html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "16px",
            "marginBottom": "18px"
        }, children=[
            html.Div(style={"width": "60px", "height": "1px",
                            "backgroundColor": "rgba(249,115,22,0.4)"}),
            html.Span(f"{len(df):,} incidents", style={
                "color": COLORS["accent"],
                "fontSize": "14px",
                "fontWeight": "600",
                "letterSpacing": "2px",
                "border": "1px solid rgba(249,115,22,0.4)",
                "borderRadius": "20px",
                "padding": "6px 20px"
            }),
            html.Div(style={"width": "60px", "height": "1px",
                            "backgroundColor": "rgba(249,115,22,0.4)"}),
        ]),

        html.P(
            "Exploring crime patterns across Chicago's neighborhoods — "
            "powered by Chicago Police Department open data via the City of Chicago Open Data Portal.",
            className="intro-text"
        ),
    ]),

    html.Div(style={"marginBottom": "32px", "maxWidth": "600px"}, children=[
        html.P("Filter by Crime Type", className="filter-label"),
        dcc.Dropdown(
            id="crime-filter",
            options=[{"label": t, "value": t} for t in sorted(df["Primary Type"].unique())],
            multi=True,
            placeholder="All crime types...",
            style={"color": "#000", "fontSize": "15px"}
        )
    ]),

    # 地图
    html.Div(className="card", style={"backgroundColor": COLORS["card"],
                    "borderRadius": "14px", "padding": "24px",
                    "marginBottom": "28px"}, children=[
        html.H3("Crime Map", style={"color": COLORS["text"]}),
        dcc.Graph(id="map-chart", style={"height": "650px"}),
        html.P(id="map-narrative", className="narrative")
    ]),

    # Arrest Rate
    html.Div(className="card", style={"backgroundColor": COLORS["card"],
                    "borderRadius": "14px", "padding": "24px",
                    "marginBottom": "28px"}, children=[
        html.H3("Arrest Rate by Crime Type", style={"color": COLORS["text"]}),
        dcc.Graph(id="arrest-chart", style={"height": "550px"}),
        html.P(id="arrest-narrative", className="narrative")
    ]),

    # Monthly Trend
    html.Div(className="card", style={"backgroundColor": COLORS["card"],
                    "borderRadius": "14px", "padding": "24px",
                    "marginBottom": "28px"}, children=[
        html.H3("Monthly Crime Trend", style={"color": COLORS["text"]}),
        dcc.Graph(id="line-chart", style={"height": "450px"}),
        html.P(id="line-narrative", className="narrative")
    ]),

    # Heatmap
    html.Div(className="card", style={"backgroundColor": COLORS["card"],
                    "borderRadius": "14px", "padding": "24px",
                    "marginBottom": "28px"}, children=[
        html.H3("Crime by Hour and Day of Week", style={"color": COLORS["text"]}),
        dcc.Graph(id="heatmap-chart", style={"height": "500px"}),
        html.P(id="bubble-narrative", className="narrative")
    ]),
])

def filter_df(crime_types):
    if crime_types:
        return df[df["Primary Type"].isin(crime_types)]
    return df

@app.callback(
    Output("map-chart", "figure"),
    Output("arrest-chart", "figure"),
    Output("line-chart", "figure"),
    Output("heatmap-chart", "figure"),
    Output("map-narrative", "children"),
    Output("arrest-narrative", "children"),
    Output("line-narrative", "children"),
    Output("bubble-narrative", "children"),
    Input("crime-filter", "value")
)
def update_all(crime_types):
    d = filter_df(crime_types)
    total = len(d)
    label = ", ".join(crime_types) if crime_types else "all crime types"
    is_filtered = bool(crime_types)

    map_fig = px.scatter_map(
        d.sample(min(5000, len(d))),
        lat="Latitude", lon="Longitude",
        color="Primary Type",
        hover_data=["Primary Type", "Description", "Arrest"],
        zoom=10, height=650, template=TEMPLATE
    )
    map_fig.update_layout(
        map_style="carto-darkmatter",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    if is_filtered:
        map_text = (f"This map shows the geographic distribution of {total:,} reported incidents "
                    f"of {label} across Chicago in 2025. Each point represents one reported crime. "
                    f"The spatial pattern reveals which neighborhoods are most affected by "
                    f"this crime type specifically.")
    else:
        map_text = ("This map displays the geographic distribution of 236,900 crime incidents "
                    "across Chicago in 2025. Each point represents a reported crime. Dense clusters "
                    "are visible in the downtown area and on the South and West sides, indicating "
                    "that crime is heavily concentrated in specific neighborhoods rather than spread "
                    "evenly across the city. Use the filter above to isolate specific crime types "
                    "and observe how their geographic patterns differ.")

    arrest_df = (d.groupby("Primary Type")
                  .agg(total=("Arrest", "count"), arrested=("Arrest", "sum"))
                  .assign(rate=lambda x: x["arrested"] / x["total"] * 100)
                  .nlargest(15, "total")
                  .sort_values("rate"))
    arrest_fig = px.bar(
        arrest_df, x="rate", y=arrest_df.index,
        orientation="h", color="rate",
        color_continuous_scale="RdYlGn",
        labels={"rate": "Arrest Rate (%)", "y": ""},
        template=TEMPLATE
    )
    arrest_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, margin={"t": 10},
        font=dict(size=14)
    )

    highest = arrest_df.index[-1]
    highest_rate = arrest_df["rate"].iloc[-1]
    lowest = arrest_df.index[0]
    lowest_rate = arrest_df["rate"].iloc[0]
    if is_filtered and len(arrest_df) == 1:
        arrest_text = (f"Among the {total:,} reported incidents of {label} in 2025, "
                       f"the arrest rate is {highest_rate:.1f}%. "
                       f"This reflects how effectively law enforcement is able to "
                       f"identify and apprehend suspects for this type of crime.")
    else:
        arrest_text = (f"This chart shows the arrest rate for the "
                       f"{'selected' if is_filtered else '15 most frequently reported'} "
                       f"crime types. {highest} has the highest arrest rate at {highest_rate:.1f}%, "
                       f"likely because these incidents are typically caught in the act. "
                       f"In contrast, {lowest} has the lowest rate at {lowest_rate:.1f}%, "
                       f"reflecting the difficulty of identifying suspects after the fact.")

    monthly = d.groupby("Month").size().reset_index(name="Count")
    peak_row = monthly.loc[monthly["Count"].idxmax()]
    low_row = monthly.loc[monthly["Count"].idxmin()]
    peak_month_name = MONTH_NAMES[peak_row["Month"]]
    low_month_name = MONTH_NAMES[low_row["Month"]]
    diff = int(peak_row["Count"] - low_row["Count"])

    monthly["Month"] = monthly["Month"].map(MONTH_SHORT)
    line_fig = px.line(
        monthly, x="Month", y="Count",
        markers=True, template=TEMPLATE,
        color_discrete_sequence=[COLORS["accent"]]
    )
    line_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin={"t": 10},
        font=dict(size=14)
    )

    line_text = (f"{'For ' + label + ', crime' if is_filtered else 'Crime'} in Chicago peaks in "
                 f"{peak_month_name} with {int(peak_row['Count']):,} reported incidents, "
                 f"and drops to its lowest in {low_month_name} with {int(low_row['Count']):,} — "
                 f"a difference of {diff:,} cases. "
                 f"{'This pattern suggests seasonal factors influence when this type of crime occurs most.' if is_filtered else 'The warmer months from May through October consistently show higher activity, suggesting that weather and outdoor activity are significant factors in crime frequency.'}")

    heat_df = (d.groupby(["DayOfWeek", "Hour"]).size().reset_index(name="Count"))
    peak_bubble = heat_df.loc[heat_df["Count"].idxmax()]
    day_totals = d.groupby("DayOfWeek").size()
    busiest_day = day_totals.idxmax()
    quietest_day = day_totals.idxmin()

    heat_fig = px.scatter(
        heat_df, x="Hour", y="DayOfWeek",
        size="Count", color="Count",
        color_continuous_scale="YlOrRd",
        category_orders={"DayOfWeek": DAY_ORDER},
        hover_data={"Hour": True, "DayOfWeek": True, "Count": True},
        labels={"Hour": "Hour of Day", "DayOfWeek": "", "Count": "Crimes"},
        template=TEMPLATE, size_max=36,
    )
    heat_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(0, 24, 2)),
            ticktext=[f"{h}:00" for h in range(0, 24, 2)],
            tickfont=dict(color="white", size=13),
            title_font=dict(color="white", size=14),
            gridcolor="#1e293b"
        ),
        yaxis=dict(tickfont=dict(color="white", size=14), gridcolor="#1e293b"),
        coloraxis_colorbar=dict(title="Crimes", tickfont=dict(color="white"),
                                title_font=dict(color="white")),
        margin={"t": 10, "b": 40},
        font=dict(size=14)
    )

    bubble_text = (f"{'For ' + label + ', the' if is_filtered else 'The'} peak hour is "
                   f"{peak_bubble['DayOfWeek']} at {int(peak_bubble['Hour'])}:00 "
                   f"with {int(peak_bubble['Count']):,} incidents. "
                   f"{busiest_day} is the busiest day overall with {day_totals[busiest_day]:,} total crimes, "
                   f"while {quietest_day} records the fewest at {day_totals[quietest_day]:,}. "
                   f"Across all days, crime activity tends to be lowest in the early morning hours "
                   f"between 4:00 and 6:00 AM, then rises through the afternoon and evening.")

    return map_fig, arrest_fig, line_fig, heat_fig, map_text, arrest_text, line_text, bubble_text

if __name__ == "__main__":
    app.run(debug=True)