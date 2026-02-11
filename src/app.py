from shiny import App, ui

app_ui = ui.page_fillable(
    ui.panel_title("Crime in London"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                id="slider",
                label="Years",
                min=1990,
                max=2026,
                value=[1990, 2026],
            ),
            ui.input_checkbox_group(
                id="checkbox_group",
                label="Crime Types",
                choices={
                    "Theft": "Theft",
                    "Burglary": "Burglary",
                },
                selected=[
                    "Theft",
                    "Burglary",
                ],
            ),
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
    ui.layout_columns(
        ui.value_box("Total Crimes", ui.output_text("total_crimes")),
        ui.value_box("Crime Rate", ui.output_text("crime_rate")),
        ui.value_box("Most Common Crime", ui.output_text("most_common_crime")),
        ui.value_box("Average Response Time", ui.output_text("avg_response_time")),
        fill=False,
    )
    ),
    ui.layout_columns(
        ui.card(
        ui.card_header("Crime Trends"),
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Crimes By Type"),
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Crime Type Trends"),
        full_screen=True,
        ),
    ),
        ui.layout_columns(
        ui.card(
        ui.card_header("Crime Heatmap by Borough and Time"),
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Recent Incidents"),
        full_screen=True,
        ),
    ),
)

def server(input, output, session):
    pass

app = App(app_ui, server)