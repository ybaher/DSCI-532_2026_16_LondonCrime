import pytest
import pandas as pd
from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from utils import filtered_data, total_crimes

# used claude to help with some of the implementations
@pytest.fixture
def sample_data():
    """Small representative subset of the London crime dataset for testing."""
    return pd.DataFrame({
        "year":           [2010, 2010, 2011, 2011, 2012, 2012, 2010],
        "month":          [1,    2,    1,    3,    1,    2,    1   ],
        "borough":        ["Camden", "Camden", "Croydon", "Croydon", "Camden", "Croydon", "Westminster"],
        "major_category": ["Robbery", "Drugs", "Burglary", "Robbery", "Drugs", "Burglary", "Robbery"],
    })

def test_filtered_data_correct_borough(sample_data):
    """Verifies filtered_data returns only the selected borough,
    if this breaks borough comparison plots will show wrong data."""
    result = filtered_data(sample_data, [2010, 2012], ["Robbery"], ["Camden"])
    assert set(result["borough"].unique()) == {"Camden"}

def test_total_crimes_returns_no_data_when_empty(sample_data):
    """Verifies total_crimes returns 'No Data' for unmatched filters,
    without this the value box would crash or misleadingly show 0."""
    result = total_crimes(sample_data, [2010, 2012], ["Sexual Offences"])
    assert result == "No Data"

def test_total_crimes_returns_string(sample_data):
    """Verifies total_crimes always returns a string,
    Shiny's render.text requires a string or the UI breaks."""
    result = total_crimes(sample_data, [2010, 2011], ["Robbery"])
    assert isinstance(result, str)

app = create_app_fixture("../src/app.py")

def test_borough_selectize_selection(page: Page, app: ShinyAppProc):
    """Verifies that selecting a borough updates the selectize input,
    if this breaks borough comparison plots will show incorrect or no data."""
    page.goto(app.url)
    borough = controller.InputSelectize(page, "borough_1")
    borough.set("Camden")
    borough.expect_selected(["Camden"])

def test_crime_type_filter(page: Page, app: ShinyAppProc):
    """Verifies that selecting a crime type filters the checkbox correctly,
    if this breaks deselected crime types would still appear in the charts."""
    page.goto(app.url)
    crime = controller.InputCheckboxGroup(page, "major_category")
    crime.set(["Robbery"])
    crime.expect_selected(["Robbery"])

def test_no_data_state(page: Page, app: ShinyAppProc):
    """Verifies that borough label updates when a borough is selected,
    if this breaks the UI would show stale or incorrect borough labels."""
    page.goto(app.url)
    borough = controller.InputSelectize(page, "borough_1")
    borough.set("Camden")
    label = controller.OutputText(page, "borough_label_1")
    label.expect_value("Camden")