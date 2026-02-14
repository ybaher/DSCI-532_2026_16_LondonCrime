from shiny import App, ui

app_ui = ui.page_fillable(
    ui.panel_title("Crime in London"),
    ui.layout_sidebar(
        ui.sidebar(
            # ui.input_select(
            #     "select",
            #     "Select Month",
            #     {
            #        "1" : "January",
            #        "2" : "February",
            #        "3": "March",
            #        "4": "April",
            #        "5": "May",
            #        "6": "June",
            #        "7": "July",
            #        "8": "August",
            #        "9": "September",
            #        "10": "October",
            #        "11": "November",
            #        "12": "December"
            #     }
            # ),
            ui.input_date_range(
                id="daterange",
                label="Date Range",
                start="2008-01-01",
                end="2016-12-01"
            ),
            ui.input_checkbox_group(
                id="checkbox_group",
                label="Crime Types",
                choices={
                    "Theft and Handling": "Theft and Handling",
                    "Violence Against the Person": "Violence Against the Person",
                    "Criminal Damage": "Criminal Damage",
                    "Robbery": "Robbery",
                    "Drugs": "Drugs",
                    "Other Notifiable Offences": "Other Notifiable Offences",
                },
                selected=[
                    "Theft and Handling",
                    "Violence Against the Person",
                    "Criminal Damage",
                    "Robbery",
                    "Drugs",
                    "Other Notifiable Offences"
                ],
            ),
            ui.input_selectize(  
                "selectize",  
                "Select Borough(s):",  
                {"Croydon": "Croydon", "Greenwich": "Greenwich", "Bromley": "Bromley"},  
                multiple=True,  
            ),  
            ui.input_action_button("action_button", "Reset filter"),
            open="desktop",
        ),
    ui.layout_columns(
        ui.value_box("Total Crimes", ui.p("count of total number of crimes"),),
        ui.value_box("Crime Rate", ui.p("crime rate (i.e. crimes per month?)")),
        ui.value_box("Most Common Crime", ui.p("most common type of crime")),
        ui.value_box("Lowest Crime Borough", ui.p("borough with the lowest number of crimes total")),
        fill=False,
    )
    ),
    ui.layout_columns(
        ui.card(
        ui.card_header("Amount of Crime - Borough Trend Comparison"),
        ui.p("line chart with months on the x axis and amount of crime on the y axis, with lines for each borough"),
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Amount of Crime by Type"),
        ui.p("bar chart with crime type on the x axis and amount of crime on the y axis, showing counts of each crime type"),
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Amount of Crime - Type Trend Comparison"),
        ui.p("line chart with months on the x axis and amount of the crime on the y axis, with lines for each crime type"),
        full_screen=True,
        ),
    ),
        ui.layout_columns(
        ui.card(
        ui.card_header("Crime Heatmap by Borough and Month"),
        ui.p("heatmap with  boroughs on the y axis and months on the x axis, showing amount of crime of by borough over for each month of the year"),        
        full_screen=True,
        ),
        ui.card(
        ui.card_header("Recent Incidents"),
        ui.p("list of most recent incidents"),
        full_screen=True,
        ),
    ),
)

def server(input, output, session):
    pass

app = App(app_ui, server)