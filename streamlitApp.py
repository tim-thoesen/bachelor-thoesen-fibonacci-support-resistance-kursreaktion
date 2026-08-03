import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Vergleich von Fibonacci-Retracements und horizontalen Support-/Resistance-Niveaus zur Analyse von Kursreaktionen",
    layout="wide"
)

st.title("Vergleich von Fibonacci-Retracements und horizontalen Support-/Resistance-Niveaus zur Analyse von Kursreaktionen")

RESULTS_PATH = "ergebnisse/ergebnisseAnalyseGLOBAL.csv"
PRICE_DATA_FOLDER = "datenCLEAN"

def readInCsv(filename, folderName):
    return pd.read_csv(
        f"{folderName}/{filename}",
        parse_dates=["Date"],
        index_col="Date"
    )

def createYearSeperation(folderName):
    ALLAssetsYearSeperated = {}
    cleanData = os.listdir(folderName)

    for filename in cleanData:

        assetYearSeperated = {}
        assetName = filename.split("_")[0]

        df = readInCsv(filename, folderName)
        df = df.sort_index()

        years = df.index.year.unique()

        for year in years:
            yearDF = df[df.index.year == year]
            assetYearSeperated[year] = yearDF

        ALLAssetsYearSeperated[assetName] = assetYearSeperated

    return ALLAssetsYearSeperated

@st.cache_data
def loadResults():
    df = pd.read_csv(RESULTS_PATH)
    df["eventDate"] = pd.to_datetime(df["eventDate"])
    return df


@st.cache_data
def loadPriceData():
    return createYearSeperation(PRICE_DATA_FOLDER)


results = loadResults()
dictionaryAssetYearData = loadPriceData()

st.sidebar.header("Auswahl")

asset = st.sidebar.selectbox(
    "Finanzinstrument",
    sorted(results["asset"].unique())
)

available_years = sorted(
    results.loc[
        results["asset"] == asset,
        "year"
    ].unique()
)

year = st.sidebar.selectbox(
    "Jahr",
    available_years
)

available_methods = sorted(
    results.loc[
        (results["asset"] == asset) &
        (results["year"] == year),
        "methodGroup"
    ].unique()
)

method = st.sidebar.selectbox(
    "Methode",
    available_methods
)

events = results[
    (results["asset"] == asset) &
    (results["year"] == year) &
    (results["methodGroup"] == method)
].copy()
events = events.sort_values("eventDate")

marketphaseRaw = events["marketphase"].iloc[0]
marketphaseLabels = {"trend": "Trendphase", "sideways": "Seitwärtsphase"}
marketphase = marketphaseLabels.get(marketphaseRaw)

try:
    price_df = dictionaryAssetYearData[asset][year].copy()
except KeyError:
    st.error(f"Keine Kursdaten gefunden für {asset} {year}.")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Finanzinstrument", asset)
col2.metric("Jahr", year)
col3.metric("Methode", method)
col4.metric("Marktphase", marketphase)
col5.metric("Events", len(events))

def getLevelColor(methodGroup, levelSubtype):
    if methodGroup == "support_resistance":

        if levelSubtype == "support":
            return "#2E7D32"

        if levelSubtype == "resistance":
            return "#D84315"

        return "#616161"

    if methodGroup == "fibonacci":
        return "#6A1B9A"

    return "#616161"

def getLevelLabel(methodGroup, levelSubtype, levelLabel):
    if methodGroup == "support_resistance":

        if levelSubtype == "support":
            return str(levelLabel)

        if levelSubtype == "resistance":
            return str(levelLabel)

    if methodGroup == "fibonacci":
        return str(levelLabel)

    return str(levelLabel)

st.subheader("Kursverlauf mit technischen Preisniveaus und Events")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=price_df.index,
        open=price_df["Open"],
        high=price_df["High"],
        low=price_df["Low"],
        close=price_df["Close"],
        whiskerwidth=0.8,
        name="OHLC",
        increasing=dict(
            line=dict(
                color="#2E7D32",
                width=1
            ),
            fillcolor="#A5D6A7"
        ),
        decreasing=dict(
            line=dict(
                color="#C62828",
                width=1
            ),
            fillcolor="#EF9A9A"
        )
    )
)

unique_levels = events[["methodGroup", "levelSubtype", "levelLabel", "levelValue"]].drop_duplicates()

for _, row in unique_levels.iterrows():

    level_color = getLevelColor(
        row["methodGroup"],
        row["levelSubtype"]
    )

    level_annotation = getLevelLabel(
        row["methodGroup"],
        row["levelSubtype"],
        row["levelLabel"]
    )

    fig.add_hline(
        y=row["levelValue"],
        line_dash="dot",
        line_color=level_color,
        line_width=1.4,
        opacity=0.7,
        annotation_text=level_annotation,
        annotation_position="top right",
        annotation_font=dict(
            size=10,
            color=level_color
        )
    )

reaction_events = events[
    events["reaction"] == 1
]

no_reaction_events = events[
    events["reaction"] == 0
]

fig.add_trace(
    go.Scatter(
        x=no_reaction_events["eventDate"],
        y=no_reaction_events["levelValue"],
        mode="markers",
        name="Event ohne Kursreaktion",
        marker=dict(
            color="#FF0000",
            size=12,
            symbol="diamond",
            line=dict(
                color="white",
                width=1.2
            )
        ),
        hovertemplate=(
            "Datum: %{x|%Y-%m-%d}<br>"
            "Preisniveau: %{y:.4f}<br>"
            "Keine Kursreaktion"
            "<extra></extra>"
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=reaction_events["eventDate"],
        y=reaction_events["levelValue"],
        mode="markers",
        name="Event mit Kursreaktion",
        marker=dict(
            color="#1DF500",
            size=12,
            symbol="diamond",
            line=dict(
                color="white",
                width=1.2
            )
        ),
        hovertemplate=(
            "Datum: %{x|%Y-%m-%d}<br>"
            "Preisniveau: %{y:.4f}<br>"
            "Kursreaktion"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=dict(
        text=f"{asset} ({year}) — {method}",
        x=0.01,
        font=dict(
            size=21,
            family="Arial",
            color="#222222"
        )
    ),
    template="plotly_white",
    height=720,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        family="Arial",
        size=13,
        color="#222222"
    ),
    xaxis_title="Datum",
    yaxis_title="Preis",
    xaxis_rangeslider_visible=False,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.98)",
        bordercolor="rgba(0,0,0,0.10)",
        borderwidth=1,
        font=dict(
        size=12,
        color="#222222"
        ),
        itemsizing="constant"
    ),
    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    )
)

fig.update_xaxes(
    range=[
        price_df.index.min(),
        price_df.index.max()
    ],
    showgrid=True,
    gridcolor="rgba(0,0,0,0.06)",
    zeroline=False,
    showline=True,
    linecolor="rgba(0,0,0,0.20)",
    linewidth=1,
    ticks="outside",
    showticklabels=True,
    automargin=True,
    tickmode="auto",
    nticks=12,
    tickformat="%d.%m.%Y",
    tickangle=-45,
    tickfont=dict(
        color="black",
        size=11
    ),
    rangebreaks=[
        dict(bounds=["sat", "mon"])
    ]
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="rgba(0,0,0,0.06)",
    zeroline=False,
    showline=True,
    linecolor="rgba(0,0,0,0.20)",
    linewidth=1,
    ticks="outside",
    tickfont=dict(
        color="black"
    )
)

st.plotly_chart(
    fig,
    width="stretch"
)