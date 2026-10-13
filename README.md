# Soccer Charts

A Python project for generating soccer-related charts and visualizations from match and statistical data.

The project provides reusable components for data processing and chart generation, alongside individual applications designed to analyze different aspects of soccer performance.

Each application maintains its own configuration and documentation while sharing common processing and graphing functionality.

## Project Structure

```text
Soccer_Charts/
├── Dictionaries/
│   └── Colors/
│       ├── Seasons_ATLUTD.json
│       └── Seasons_ATLUTD2.json
├── Graphing/
│   └── Chart_Lines.py
├── Processing/
│   ├── Data_Processing.py
│   └── Soccer_Processing.py
├── Points_Per_Season/
│   ├── Config.toml.example
│   ├── Points_Per_Season.py
│   └── README.md
├── Output/
├── tests/
├── requirements.txt
└── README.md
```

## Applications

### Points Per Season

Generates cumulative points charts comparing a team's performance across multiple seasons.

Features include:

- Full-season and limited-season comparisons.
- Support for seasons with different numbers of matches.
- Standard and shootout-based points calculations.
- Configurable match inclusion and exclusion filters.
- Manually selected season highlights.
- Muted historical seasons and emphasized current seasons.
- Multiple team configurations.
- WebP chart output.

**[Points Per Season — Documentation](Points_Per_Season/README.md)**

## Shared Modules

### Graphing

Reusable chart-generation components intended to support multiple applications.

**`Graphing/Chart_Lines.py`**

Provides a configurable line-chart generator supporting:

- Multiple data series with different lengths.
- Custom series colors and line styling.
- Highlighted and muted series.
- Endpoint annotations.
- Configurable titles, axes, fonts, and backgrounds.
- Full and limited charts.
- Image export, including WebP.

### Data Processing

**`Processing/Data_Processing.py`**

General-purpose data-processing operations, including:

- CSV loading.
- Record filtering.
- Duplicate removal.
- Grouped cumulative calculations.

These functions are designed to remain independent of soccer-specific rules.

### Soccer Processing

**`Processing/Soccer_Processing.py`**

Soccer-specific calculations used by applications, including match points for standard and shootout-based competitions.

Keeping soccer rules separate from generic data-processing functionality allows the shared modules to be reused for additional chart types.


**Requirements**

```bash
python -m pip install -r requirements.txt
```

## Getting Started

1. Clone or download the repository.
2. Install the required Python packages.
3. Navigate to the application you want to run.
4. Copy its example configuration file to the working configuration filename.
5. Update the configuration to reference your local data.
6. Run the application using the instructions in its README.

For the currently implemented application, see [Points Per Season](Points_Per_Season/README.md).

## Configuration

Each application is responsible