# London Crime Data

An interactive dashboard to explore crime data in London. Filter by year and crime type, view key metrics, and explore trends and patterns across the city's boroughs.

---

## Getting the Dashboard Running Locally

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) installed

### Steps

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

5. **Run the dashboard**
   ```bash
   shiny run src/app.py
   ```

6. **Open the app** in your browser at `http://127.0.0.1:8000` (or the URL shown in the terminal).
