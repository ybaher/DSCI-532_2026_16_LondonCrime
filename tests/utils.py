import pandas as pd

# used claude to help with some of the implementations
def filtered_data(data, year_range, major_categories, boroughs):
    """Filter crime data by year range, crime categories, and boroughs."""
    year = data.year.between(year_range[0], year_range[1], inclusive="both")
    major_category = data.major_category.isin(major_categories)
    borough = data.borough.isin(boroughs)
    return data[borough & major_category & year]

def filtered_data_year(data, year_range, major_categories):
    """Filter crime data by year range and crime categories only."""
    year = data.year.between(year_range[0], year_range[1], inclusive="both")
    major_category = data.major_category.isin(major_categories)
    return data[year & major_category]

def total_crimes(data, year_range, major_categories):
    """Return total number of crimes as a string, or 'No Data' if none found."""
    df = filtered_data_year(data, year_range, major_categories)
    if df.empty:
        return "No Data"
    return str(df.shape[0])