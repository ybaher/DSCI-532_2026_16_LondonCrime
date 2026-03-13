# Changelog

## [0.3.0]

### Added

- Added an AI chatbot tab that filters the data based on user input and implements a selection of plots using the filtered data. The AI chatbot is not set up specifically for borough comparisons, as it is based off of the version 0.2.0 dashboard.

### Changed

- Made the plots into their own tabs inside the main dashboard so that they are easier to view in large format. Chose the stacked bar plot as the default view plot, since it provides a good summary of the two comparison boroughs and their relative amount of crime and crime type breakdown.
- Changed dashboard format to an exactly two borough comparison
- Updated side selector to select exactly two boroughs, with the lowest and highest crime boroughs as the defaults
- Redesigned plots to showcase borough comparisons
- Removed trend line plot and crime type vs month heat map plot, as they did not facilitate easy borough comparison
- Combined summary cards such that each summary card has average crime rate, lowest, and highest crime type. Created three summary cards: one for each comparison borough and one for the city of london at large to use as a baseline.

### Fixed

- Summary cards and plots now handle empty filtered data gracefully, displaying "No Data" instead of errors when filters return no results.
- Fix cards being too small for readability.

### Known Issues

- AI chatbot can take a very long time to load, even on the first message.

### Reflection

The two borough comparison makes the summary cards much more useful, and makes it easier to compare to a baseline (all boroughs). The graphs contain some repeated information, and additional graph design to make each graph its own unit of important information would be a good next step. That the dashboard and the AI chatbot aren't completely aligned (the dashboard is hyperfocused on two borough comparison, while the AI chatbot allows for broader inquiries) may be confusing to some users.

## [0.2.0]

### Added

- Sidebar controls for date range selection, crime type filters, borough multi-select, and a reset button.
- Value boxes for key summary metrics (total crimes, crime rate, most common crime, and lowest crime borough).
- Card layout with placeholder panels for borough trend comparison, crime type distribution, crime-type trend comparison, a borough–month heatmap, and a recent incidents view.

### Changed

- Structured the dashboard layout so that key headline metrics appear above the main visualizations.
- Aligned the planned views more closely with the Milestone 1 proposal.

### Fixed

- Populated the placeholder panels with the data from the dataset.

### Known Issues

- Performance and usability have not yet been tested on the full raw dataset.

### Reflection

Building out the UI skeleton helped clarify how users will move between filters, headline metrics, and detailed views, and surfaced several design decisions (such as placing key numbers above the plots and grouping related charts together). This milestone is a good starting point for the implementation of the dashboard.