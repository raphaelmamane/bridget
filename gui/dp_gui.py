import typing as t
import pandas as pd

import datapane as dp

import datapane_components as dc
from datapane_components import chatgpt

TEXT_GRADIENT_STYLING="background: -webkit-linear-gradient(#B372F7, #7038A1); -webkit-background-clip: text; -webkit-text-fill-color: transparent"


def load_dataset(dataset: str) -> pd.DataFrame:
    if dataset == "Marketing":
        d = "data/test_dataset.csv"
    else:
        print("Error")
        return None

    return pd.read_csv(d)

def ask_question(dataset: str, query: str, query_type: str) -> t.List:
    df = load_dataset(dataset)
    if df is None:
        return None

    # Trim whitespace as it confuses chatgpt
    df.columns = df.columns.str.strip()

    # Replace spaces with _
    df.columns = df.columns.str.replace(" ", "_")

    if query_type == "Dataset":
        res = chatgpt.ask_data_question(df, query)
    else:  # Visualization
        res = chatgpt.ask_viz_question(df, query)

    return [
        dc.divider(),
        f"<h4 style='color: lightslategrey;'>Q: {query}</h4>",
        f"<h4 style='{TEXT_GRADIENT_STYLING}'>Bridget: Here's your {query_type.lower()}</h4>",
        res,
    ]


about_view = dp.Group(
    dp.Group(
        dp.Media(file="images/bridget.png"),
        f"<h1 style='{TEXT_GRADIENT_STYLING}'>Ask Bridget</h1>",
        columns=2,
        valign="center"
    ),
    dp.Text("Hi I'm Bridget!"),
    dp.Text("I'm your Nexar AI-nalyst, here to bridge the gap between data and people."),
    dp.Text("**Upload** a pdf, a text file or **choose** a dataset, **ask** a question"),
    dp.Text("Get an analysis in **real-time!**"),
)

ask_view = dp.Group(
    dp.Text("## Ask a new question"),
    dp.Form(
        ask_question,
        target="results",
        controls=dict(
            dataset=dp.Choice(label="Select dataset", options=["Marketing", "Sales", "Road Data", "Incidents"], initial="Marketing"),
            query=dp.TextBox(label=f"What do you want to know regarding?"),
            query_type=dp.Choice(label="What type of result?", options=["Dataset", "Visualization"]),
        ),
        submit_label="Ask Bridget"
    ),
    columns=1,
    valign="center"
)

bridget_view = [
    dp.Group(
        about_view,
        ask_view,
        columns=2,
        widths=[30, 70]
    ),

    dp.Group(name="results"),
]

dp.enable_logging()

dp.serve_app(bridget_view)