# London Crime Data

An interactive dashboard to explore crime data in London. Filter by year and crime type, view key metrics, and explore trends and patterns across the city's boroughs.

---

## For Users

The *Crime in London* dashboard centralises publicly available crime data for London into one interactive tool. It is designed for:

- **Government and public safety staff** who need quick, high-level summaries of crime levels across boroughs and over time.
- **Prospective residents and relocators** deciding which boroughs to live in based on crime levels and trends.
- **Tourists and visitors** who want to understand which areas are safer for staying or going out at night.
- **Legal and policy professionals** who need evidence-based crime statistics to support or challenge claims in specific boroughs.

**What the dashboard helps you do**

- **Understand overall crime levels** via total crimes and crime rate per 1,000 people.
- **Compare boroughs** to see which are relatively safer or higher risk.
- **Explore patterns over time** (e.g., whether crime is rising or falling in a given area).
- **Drill into crime types** (e.g., theft, robbery, violence) to see which offences dominate where.

This enables better-informed decisions, such as choosing a neighbourhood to move to, selecting a hotel, or supporting arguments in reports and legal cases.

### Live dashboard

- **Stable Posit Cloud deployment** (recommended):  
  [Open the dashboard](https://019c8cf1-a288-5cee-f1a1-893bc0f9414c.share.connect.posit.cloud)
- **Preview / development deployment**:  
  [Preview dashboard](https://019c8cf5-07e1-aea6-bf22-33e39990085b.share.connect.posit.cloud)

### Demo (animated preview)

Below is a short animated demo of the dashboard in use (loading, filtering, and exploring key views):

![Animated demo of the Crime in London dashboard](img/demo.gif)

---

## For Contributors

Thank you for your interest in improving the *Crime in London* dashboard.

- **Contribution guidelines** (branching, coding style, issue workflow, and review process) are documented in  
  [`CONTRIBUTING.md`](CONTRIBUTING.md).
- The summary below focuses on how to **install dependencies** and **run the app locally**.

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) installed

### Getting the dashboard running locally

1. **Clone or download this repository**

   ```bash
   git clone https://github.com/ybaher/DSCI-532_2026_16_LondonCrime.git
   cd DSCI-532_2026_16_LondonCrime
   ```

2. **Create the conda environment**

   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment**

   ```bash
   conda activate LondonCrime
   ```

<!-- 4. **Install Shiny** (if not already in the environment)
   ```bash
   pip install shiny
   ``` -->

4. **Run the dashboard**

   ```bash
   shiny run src/app.py
   ```

5. **Open the app** in your browser at `http://127.0.0.1:8000` (or the URL shown in the terminal).

### AI Assistant

The **AI Assistant** tab lets you explore the London crime data with natural language (e.g., "Show only theft crimes in Westminster"). To enable it:

1. Copy `.env.example` to `.env` in the project root.
2. Add your `GITHUB_TOKEN`

