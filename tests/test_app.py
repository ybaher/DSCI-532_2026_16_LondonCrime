import sys
import os
import pandas as pd
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from utils import filtered_data, filtered_data_year, total_crimes

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

# filtered_data tests
def test_filtered_data_correct_borough(sample_data):
    """Verifies that filtered_data returns only rows matching the selected borough,
    incorrect borough filtering would show wrong borough data in the comparison plots."""
    result = filtered_data(sample_data, [2010, 2012], ["Robbery", "Drugs", "Burglary"], ["Camden"])
    assert set(result["borough"].unique()) == {"Camden"}


def test_filtered_data_correct_year_range(sample_data):
    """Verifies that filtered_data excludes rows outside the selected year range,
    if year filtering breaks, the dashboard would show data from unselected years."""
    result = filtered_data(sample_data, [2010, 2011], ["Robbery", "Drugs", "Burglary"], ["Camden"])
    assert result["year"].max() <= 2011
    assert result["year"].min() >= 2010


def test_filtered_data_correct_crime_type(sample_data):
    """Verifies that filtered_data excludes unselected crime types,
    if crime type filtering breaks, deselected crimes would still appear in plots."""
    result = filtered_data(sample_data, [2010, 2012], ["Robbery"], ["Camden", "Croydon"])
    assert set(result["major_category"].unique()) == {"Robbery"}


def test_filtered_data_multiple_boroughs(sample_data):
    """Verifies that filtered_data includes all selected boroughs when multiple are chosen,
    this underpins the side-by-side borough comparison feature."""
    result = filtered_data(sample_data, [2010, 2012], ["Robbery", "Drugs", "Burglary"], ["Camden", "Croydon"])
    assert "Camden" in result["borough"].values
    assert "Croydon" in result["borough"].values


def test_filtered_data_empty_when_no_borough_match(sample_data):
    """Verifies that filtered_data returns an empty DataFrame when the borough doesn't exist,
    the dashboard should gracefully show 'No Data' rather than crash."""
    result = filtered_data(sample_data, [2010, 2012], ["Robbery"], ["Nonexistent Borough"])
    assert result.empty


def test_filtered_data_single_year(sample_data):
    """Verifies that a single-year range (start == end) returns only that year's data,
    boundary conditions on the year slider must filter inclusively."""
    result = filtered_data(sample_data, [2011, 2011], ["Robbery", "Burglary"], ["Croydon"])
    assert list(result["year"].unique()) == [2011]


# filtered_data_year tests
def test_filtered_data_year_ignores_borough(sample_data):
    """Verifies that filtered_data_year includes all boroughs (no borough filter applied),
    this function powers the London-wide summary stats which should not be borough-restricted."""
    result = filtered_data_year(sample_data, [2010, 2012], ["Robbery", "Drugs", "Burglary"])
    assert "Westminster" in result["borough"].values
    assert "Camden" in result["borough"].values
    assert "Croydon" in result["borough"].values


def test_filtered_data_year_filters_crime_type(sample_data):
    """Verifies that filtered_data_year still respects the crime type filter,
    London-wide stats must reflect the user's selected crime categories."""
    result = filtered_data_year(sample_data, [2010, 2012], ["Burglary"])
    assert set(result["major_category"].unique()) == {"Burglary"}


# total_crimes tests
def test_total_crimes_correct_count(sample_data):
    """Verifies that total_crimes returns the exact row count as a string,
    an off-by-one error here would display a wrong number in the summary value box."""
    result = total_crimes(sample_data, [2010, 2012], ["Robbery", "Drugs", "Burglary"])
    assert result == str(len(sample_data))  # all rows match


def test_total_crimes_returns_no_data_when_empty(sample_data):
    """Verifies that total_crimes returns 'No Data' when the filtered result is empty,
    without this guard the value box would crash or display '0' misleadingly."""
    result = total_crimes(sample_data, [2010, 2012], ["Sexual Offences"])
    assert result == "No Data"


def test_total_crimes_returns_string(sample_data):
    """Verifies that total_crimes always returns a string type,
    Shiny's @render.text requires a string — returning an int would break the UI."""
    result = total_crimes(sample_data, [2010, 2011], ["Robbery"])
    assert isinstance(result, str)