from pathlib import Path
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import querychat
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, output_widget

# Load environment variables for AI assistant (GITHUB_MODEL)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
github_model = os.getenv("GITHUB_MODEL", "gpt-4.1-mini")

data = pd.read_csv("data/raw/LondonCrimeData.csv")

def filtered_data(data, year_range, major_categories, boroughs):
    year = data.year.between(
        left=year_range[0],
        right=year_range[1],
        inclusive="both",
    )
    major_category = data.major_category.isin(major_categories)
    borough = data.borough.isin(boroughs)
    return data[borough & major_category & year]

def filtered_data_year(data, year_range, major_categories):
    year = data.year.between(
        left=year_range[0],
        right=year_range[1],
        inclusive="both",
    )
    major_category = data.major_category.isin(major_categories)
    return data[year & major_category]

def total_crimes(data, year_range, major_categories):
    df = filtered_data_year(data, year_range, major_categories)
    if df.empty:
        return "No Data"
    return str(df.shape[0])

# QueryChat setup for AI Assistant
qc = querychat.QueryChat(
    data,
    "london_crime",
    client=f"github/{github_model}",
    greeting=(
        "Try asking things like:\n"
        "- *Show only theft and violence crimes in Westminster*\n"
        "- *Filter to years 2012-2014 with burglary offences*\n"
        "- *Which boroughs have the highest crime counts?*\n"
        "- *Show crimes by type for Camden and Islington*"
    ),
)

BOROUGHS = sorted(['Barking and Dagenham', 'Waltham Forest', 'Tower Hamlets', 'Sutton', 'Southwark', 'Richmond upon Thames', 'Redbridge', 'Newham', 'Merton', 'Lewisham', 'Lambeth', 'Kingston upon Thames', 'Kensington and Chelsea', 'Islington', 'Hounslow', 'Wandsworth', 'Hillingdon', 'Harrow', 'Haringey', 'Hammersmith and Fulham', 'Hackney', 'Greenwich', 'Enfield', 'Ealing', 'Croydon', 'City of London', 'Camden', 'Bromley', 'Brent', 'Bexley', 'Barnet', 'Havering', 'Westminster'])

CRIME_TYPES = [
    "Theft and Handling",
    "Criminal Damage",
    "Robbery",
    "Drugs",
    "Violence Against the Person",
    "Other Notifiable Offences",
    "Sexual Offences",
    "Fraud or Forgery",
    "Burglary"
]

# Asked Claude to generate a color palette dictionary for the crime types
# and to create CSS code to ensure instances (plots, text boxes) use the same colorings.
CRIME_COLORS = {
    "Theft and Handling":          "#4E79A7",
    "Criminal Damage":             "#F28E2B",
    "Robbery":                     "#E15759",
    "Drugs":                       "#76B7B2",
    "Violence Against the Person": "#59A14F",
    "Other Notifiable Offences":   "#B07AA1",
    "Sexual Offences":             "#FF9DA7",
    "Fraud or Forgery":            "#9C755F",
    "Burglary":                    "#EDC948",
}

# CSS block that maps each crime type to its color for value box highlight
CRIME_CSS = "\n".join(
    f'.crime-color-{i} {{ color: {color} !important; font-weight: bold; }}'
    for i, color in enumerate(CRIME_COLORS.values())
)

# CSS block that colors the checkbox labels to match crime type colors.
# ui.input_checkbox_group renders as: #major_category .shiny-options-group > div:nth-child(n) label
CHECKBOX_CSS = "\n".join(
    f'#major_category .shiny-options-group > div:nth-child({i + 1}) label {{ color: {color}; font-weight: 600; }}\n'
    f'#major_category .shiny-options-group > div:nth-child({i + 1}) input[type="checkbox"] {{ accent-color: {color}; }}'
    for i, color in enumerate(CRIME_COLORS.values())
)

CRIME_COLOR_INDEX = {name: i for i, name in enumerate(CRIME_COLORS.keys())}


app_ui = ui.page_navbar(
    ui.nav_panel(
        "Dashboard",
        ui.tags.style(f"""
            #total_crimes {{ font-size: 2rem; font-weight: bold; }}
            #crime_rate {{ font-size: 2rem; font-weight: bold; }}
            #year_label_1, #year_label_2, #year_label_3, {{ font-size: 0.8rem; opacity: 0.7; }}
            .bslib-value-box {{ min-height: 120px !important; }}
            .bslib-value-box .value-box-grid {{ padding: 0.5rem !important; }}
            .bslib-card {{ min-height: 500px; }}
            .crime-value {{ font-size: 1rem; font-weight: bold; display: block; }}
            .crime-label {{ font-size: 0.7rem; opacity: 0.7; display: block; margin-top: 0.25rem; }}
            {CRIME_CSS}
            {CHECKBOX_CSS}
        """),
        ui.layout_sidebar(
            ui.sidebar(
                # Year Selector
                ui.input_slider(
                    "year_range",
                    "Year Range",
                    min=data.year.min(),
                    max=data.year.max(),
                    value=[data.year.min(), data.year.max()],
                    sep=""
                ),
                # Crime Type Checkbox with Custom Coloring (partner's cleaner approach)
                ui.input_checkbox_group(
                    "major_category",
                    "Crime Types",
                    choices=CRIME_TYPES,
                    selected=CRIME_TYPES,
                ),
                # Two borough selectors for side-by-side comparison (your change)
                ui.input_selectize(
                    "borough_1",
                    "Select Borough 1:",
                    choices=BOROUGHS,
                    multiple=False,
                    selected="Croydon"
                ),
                ui.input_selectize(
                    "borough_2",
                    "Select Borough 2:",
                    choices=BOROUGHS,
                    multiple=False,
                    selected="City of London"
                ),
                ui.input_action_button("reset_filter", "Restore Defaults"),
                open="desktop",
            ),
            # Summary Info Text Boxes — one column per borough
            ui.layout_columns(
                # Borough 1 value boxes
                ui.value_box(
                    ui.output_text("borough_label_1"),
                    ui.output_text("year_label_1"),
                    ui.tags.div(
                        ui.tags.span("Avg Monthly Crime Rate", class_="crime-label"),
                        ui.tags.div(ui.output_ui("crime_rate_1"), class_="crime-value"),
                        ui.tags.span("Most Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("most_common_crime_1"), class_="crime-value"),
                        ui.tags.span("Least Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("least_common_crime_1"), class_="crime-value"),
                    ),
                ),
                # Borough 2 value boxes
                ui.value_box(
                    ui.output_text("borough_label_2"),
                    ui.output_text("year_label_2"),
                    ui.tags.div(
                        ui.tags.span("Avg Monthly Crime Rate", class_="crime-label"),
                        ui.tags.div(ui.output_ui("crime_rate_2"), class_="crime-value"),
                        ui.tags.span("Most Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("most_common_crime_2"), class_="crime-value"),
                        ui.tags.span("Least Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("least_common_crime_2"), class_="crime-value"),
                    ),
                ),
                # London-wide summary
                ui.value_box(
                    "London (All Boroughs)",
                    ui.output_text("year_label_3"),
                    ui.tags.div(
                        ui.tags.span("Avg Monthly Crime Rate", class_="crime-label"),
                        ui.tags.div(ui.output_ui("crime_rate_london"), class_="crime-value"),
                        ui.tags.span("Most Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("most_common_crime_london"), class_="crime-value"),
                        ui.tags.span("Least Common Crime", class_="crime-label"),
                        ui.tags.div(ui.output_ui("least_common_crime_london"), class_="crime-value"),
                    ),
                ),
                fill=False,
            ),
            # Plots — borough comparison
            ui.navset_card_underline(
                ui.nav_panel(
                    "Total Crimes",
                    ui.card(output_widget("borough_trend"), full_screen=True),
                ),
                ui.nav_panel(
                    "Crime Type Breakdown",
                    ui.card(output_widget("crime_type_counts"), full_screen=True),
                ),
                ui.nav_panel(
                    "Crime Intensity By Month",
                    ui.card(output_widget("borough_month_heatmap"), full_screen=True),
                ),
                title="Crime Plots",
            ),
        ),
        # Footer
        ui.tags.footer(
            ui.tags.hr(style="margin: 0;"),
            ui.tags.div(
                ui.tags.div(
                    ui.tags.strong("London Crime Dashboard"),
                    ui.tags.span(" · ", style="opacity: 0.4;"),
                    ui.tags.span("An interactive exploration of crime trends across London boroughs from 2008–2016.", style="opacity: 0.7;"),
                    ui.tags.span(" · ", style="opacity: 0.4;"),
                    ui.tags.span("Authors: Molly Kessler, Yasaman Baher, Justin Mak", style="opacity: 0.7;"),
                    ui.tags.span(" · ", style="opacity: 0.4;"),
                    ui.tags.a("GitHub Repo", href="https://github.com/UBC-MDS/DSCI-532_2026_16_LondonCrime", target="_blank", style="opacity: 0.7;"),
                    ui.tags.span(" · ", style="opacity: 0.4;"),
                    ui.tags.span("Last updated: March 8, 2026", style="opacity: 0.7;"),
                ),
                style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; font-size: 0.8rem;",
            ),
        ),
    ),
    ui.nav_panel(
        "AI Assistant",
        ui.layout_sidebar(
            ui.sidebar(
                qc.ui(),
                ui.hr(),
                ui.p("Example prompts:"),
                ui.tags.ul(
                    ui.tags.li("Show only theft and violence crimes in Westminster"),
                    ui.tags.li("Filter to years 2012-2014 with burglary offences"),
                    ui.tags.li("Which boroughs have the highest crime counts?"),
                ),
                width=400,
            ),
            ui.card(
                ui.card_header("Filtered Data"),
                ui.output_data_frame("ai_data_table"),
            ),
            ui.card(
                ui.download_button("download_filtered", "Download filtered data"),
            ),
            ui.card(
                ui.card_header("AI query result state"),
                ui.output_text("ai_filter_state_text"),
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Crime by Borough and Type (AI Filtered)"),
                    output_widget("ai_borough_type_plot"),
                ),
                ui.card(
                    ui.card_header("Crime by Type Over Time (AI Filtered)"),
                    output_widget("ai_crime_type_trend"),
                ),
                col_widths=(6, 6),
            ),
            ui.card(
                ui.card_header("Crime Counts by Type (AI Filtered)"),
                output_widget("ai_crime_type_counts"),
            ),
        ),
    ),
    title="Crime in London",
)


def server(input, output, session):
    # Initialize QueryChat server for AI Assistant tab
    qc_vals = qc.server()

    # ── Filtered data reactives ──────────────────────────────────────────

    @reactive.calc
    def filtered_data_1():
        """Data filtered to borough_1 selection, selected crime types, and year range."""
        year = data.year.between(input.year_range()[0], input.year_range()[1], inclusive="both")
        # major_category = data.major_category.isin(input.major_category())
        borough = data.borough == input.borough_1()
        return data[borough & year]

    @reactive.calc
    def filtered_data_2():
        """Data filtered to borough_2 selection, selected crime types, and year range."""
        year = data.year.between(input.year_range()[0], input.year_range()[1], inclusive="both")
        # major_category = data.major_category.isin(input.major_category())
        borough = data.borough == input.borough_2()
        return data[borough & year]

    @reactive.calc
    def filtered_data_london():
        """London-wide data filtered to selected crime types and year range (for summary boxes)."""
        year = data.year.between(input.year_range()[0], input.year_range()[1], inclusive="both")
        # major_category = data.major_category.isin(input.major_category())
        return data[year]

    @reactive.calc
    def filtered_data_both():
        """Data for both selected boroughs combined — used for comparison plots."""
        year = data.year.between(input.year_range()[0], input.year_range()[1], inclusive="both")
        major_category = data.major_category.isin(input.major_category())
        borough = data.borough.isin([input.borough_1(), input.borough_2()])
        return data[borough & major_category & year]

    # ── Helper functions ─────────────────────────────────────────────────

    def most_common_crime(df):
        crime = str(df.major_category.value_counts().idxmax())
        idx = CRIME_COLOR_INDEX.get(crime, 0)
        return ui.tags.span(crime, class_=f"crime-color-{idx}")

    def least_common_crime(df):
        crime = str(df.major_category.value_counts().idxmin())
        idx = CRIME_COLOR_INDEX.get(crime, 0)
        return ui.tags.span(crime, class_=f"crime-color-{idx}")

    def calc_crime_rate(df):
        monthly_crimes = df.groupby(["year", "month"]).size()
        return str(round(monthly_crimes.mean()))

    def year_label():
        start, end = input.year_range()
        return str(start) if start == end else f"{start} - {end}"

    # ── Year / borough labels ────────────────────────────────────────────

    @render.text
    def year_label_1():
        return year_label()

    @render.text
    def year_label_2():
        return year_label()

    @render.text
    def year_label_3():
        return year_label()

    @render.text
    def borough_label_1():
        return input.borough_1()

    @render.text
    def borough_label_2():
        return input.borough_2()

    # ── London-wide summary stats ────────────────────────────────────────

    @render.ui
    def crime_rate_london():
        df = filtered_data_london()
        return ui.tags.span("No Data") if df.empty else ui.tags.span(calc_crime_rate(df))

    @render.ui
    def most_common_crime_london():
        df = filtered_data_london()
        return ui.tags.span("No Data") if df.empty else most_common_crime(df)

    @render.ui
    def least_common_crime_london():
        df = filtered_data_london()
        return ui.tags.span("No Data") if df.empty else least_common_crime(df)

    # ── Per-borough stats ────────────────────────────────────────────────

    @render.ui
    def most_common_crime_1():
        df = filtered_data_1()
        return ui.tags.span("No Data") if df.empty else most_common_crime(df)

    @render.ui
    def most_common_crime_2():
        df = filtered_data_2()
        return ui.tags.span("No Data") if df.empty else most_common_crime(df)

    @render.ui
    def least_common_crime_1():
        df = filtered_data_1()
        return ui.tags.span("No Data") if df.empty else least_common_crime(df)

    @render.ui
    def least_common_crime_2():
        df = filtered_data_2()
        return ui.tags.span("No Data") if df.empty else least_common_crime(df)

    @render.ui
    def crime_rate_1():
        df = filtered_data_1()
        return ui.tags.span("No Data") if df.empty else ui.tags.span(calc_crime_rate(df))

    @render.ui
    def crime_rate_2():
        df = filtered_data_2()
        return ui.tags.span("No Data") if df.empty else ui.tags.span(calc_crime_rate(df))

    # ── Plots ────────────────────────────────────────────────────────────

    @render_plotly
    def borough_trend():
        df = filtered_data_both()
        if df.empty:
            return px.bar(title="No data — select boroughs")
        df_grouped = df.groupby(["borough", "major_category"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values("count", ascending=False)
        fig = px.bar(
            df_grouped,
            x="borough",
            y="count",
            color="major_category",
            barmode="stack",
            title="Amount of Crime by Borough",
            labels={"borough": "Borough", "count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig

    @render_plotly
    def crime_type_counts():
        df = filtered_data_both()
        if df.empty:
            return px.bar(title="No data — select boroughs")
        df_grouped = df.groupby(["major_category", "borough"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values("count", ascending=True)
        fig = px.bar(
            df_grouped,
            x="major_category",
            y="count",
            color="major_category",
            facet_col="borough",
            title="Amount of Crime by Type",
            labels={"count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        fig.update_layout(margin=dict(t=80))
        return fig

    @render_plotly
    def borough_month_heatmap():
        df = filtered_data_both()
        if df.empty:
            return px.imshow([[]], title="No data — select boroughs")
        df_grouped = df.groupby(["borough", "month"]).size().reset_index(name="count")
        df_pivot = df_grouped.pivot(index="borough", columns="month", values="count")
        df_pivot = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100
        fig = px.imshow(
            df_pivot,
            title="Monthly Crime Breakdown by Borough (% of Total Yearly Commited In Given Month)",
            labels={"x": "Month", "y": "Borough", "color": "% of Yearly Crime"},
            color_continuous_scale="Viridis",
            aspect="auto",
        )
        return fig

    # ── Reset Filters ────────────────────────────────────────────────────

    @reactive.effect
    @reactive.event(input.reset_filter)
    def reset_filters():
        ui.update_slider("year_range", value=[int(data.year.min()), int(data.year.max())])
        ui.update_checkbox_group("major_category", selected=CRIME_TYPES)
        ui.update_selectize("borough_1", selected="Croydon")
        ui.update_selectize("borough_2", selected="City of London")

    # ── AI Assistant tab outputs ─────────────────────────────────────────

    @render.data_frame
    def ai_data_table():
        df = qc_vals.df()
        return df.to_pandas() if hasattr(df, "to_pandas") else df

    @render.download(filename="filtered_london_crime.csv")
    def download_filtered():
        df = qc_vals.df()
        pdf = df.to_pandas() if hasattr(df, "to_pandas") else df
        yield pdf.to_csv(index=False)

    @render.text
    def ai_filter_state_text():
        df = qc_vals.df()
        pdf = df.to_pandas() if hasattr(df, "to_pandas") else df
        return f"Rows: {len(pdf):,} | Columns: {len(pdf.columns):,}"

    @render_plotly
    def ai_borough_type_plot():
        df = qc_vals.df()
        pdf = df.to_pandas() if hasattr(df, "to_pandas") else df
        if pdf.empty:
            return px.line(title="No data for current query")
        if "borough" not in pdf.columns or "major_category" not in pdf.columns:
            return px.line(title="Required columns not in query result")
        df_grouped = pdf.groupby(["borough", "major_category"]).size().reset_index(name="count")
        df_grouped = df_grouped.sort_values("count", ascending=False)
        fig = px.bar(
            df_grouped,
            x="borough",
            y="count",
            color="major_category",
            barmode="stack",
            title="Crime by Borough and Type",
            labels={"borough": "Borough", "count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig

    @render_plotly
    def ai_crime_type_trend():
        df = qc_vals.df()
        pdf = df.to_pandas() if hasattr(df, "to_pandas") else df
        if pdf.empty:
            return px.line(title="No data for current query")
        if "year" not in pdf.columns or "month" not in pdf.columns or "major_category" not in pdf.columns:
            return px.line(title="Required columns not in query result")
        df_grouped = pdf.groupby(["year", "month", "major_category"]).size().reset_index(name="count")
        df_grouped["date"] = pd.to_datetime(df_grouped[["year", "month"]].assign(day=1))
        fig = px.line(
            df_grouped,
            x="date",
            y="count",
            color="major_category",
            title="Crime by Type Over Time",
            labels={"date": "Date", "count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig

    @render_plotly
    def ai_crime_type_counts():
        df = qc_vals.df()
        pdf = df.to_pandas() if hasattr(df, "to_pandas") else df
        if pdf.empty:
            return px.bar(title="No data for current query")
        if "major_category" not in pdf.columns:
            return px.bar(title="Required columns not in query result")
        df_grouped = pdf.groupby("major_category").size().reset_index(name="count")
        df_grouped = df_grouped.sort_values("count", ascending=True)
        fig = px.bar(
            df_grouped,
            x="major_category",
            y="count",
            color="major_category",
            title="Crime Counts by Type",
            labels={"count": "Number of Crimes", "major_category": "Crime Type"},
            color_discrete_map=CRIME_COLORS,
        )
        return fig


app = App(app_ui, server)