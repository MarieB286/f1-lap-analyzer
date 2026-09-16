# F1 Lap Analyzer

Interactive telemetry analysis tool for Formula 1 lap comparisons, built with [FastF1](https://docs.fastf1.dev/) and [Dash](https://dash.plotly.com/).

Compare any two drivers' fastest laps across sessions, visualize speed profiles and cumulative delta over the lap, see where each driver gains or loses time on the track, and get a corner-by-corner breakdown with slow/medium/fast classification.

## Features

- Dynamic selection of year, Grand Prix, session, and qualifying phase (Q1/Q2/Q3)
- Interactive speed and cumulative delta plot with corner annotations
- Track map colored by local time gain, showing where each driver is faster
- Corner-by-corner comparison table with minimum speeds and classification (slow / medium / fast)
- Automatic detection of qualifying phases using temporal gap analysis, so comparisons in Q3 actually compare Q3 laps and not each driver's best of the whole session

## Getting started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/MarieB286/f1-lap-analyzer.git
cd f1-lap-analyzer
pip install -r requirements.txt
```

### Run the app

```bash
python test_dash.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

The first session load takes 30-60 seconds while FastF1 downloads the data. Subsequent loads are cached and near-instant.

## Roadmap

- [x] Week 1 — Refactor Monaco notebook into modular library
- [x] Week 2 — Dash app with dynamic selectors and interactive Plotly graphs
- [x] Week 3 — Corner classification (slow / medium / fast) and comparison table
- [ ] Week 4 — Gap analyzer: identify corners where the delta really builds up
- [ ] Week 5 — Automatic narrative generator (template-based)
- [ ] Week 6 — PDF report export
- [ ] Week 7 — Visual polish (team colors, dark theme, responsive layout)

## Limitations

— FastF1 depends on F1 Live Timing data, which can take a few hours to be complete
- Corner classification uses a fixed 60m/30m window around each corner, which may miss the true Vmin on very short or overlapping corners

## Built with

- [FastF1](https://docs.fastf1.dev/) — Python package for accessing F1 telemetry data
- [Dash](https://dash.plotly.com/) — Web framework for analytical apps
- [Plotly](https://plotly.com/python/) — Interactive graphing library
- [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), [scipy](https://scipy.org/) — Data manipulation

## License

MIT — see [LICENSE](LICENSE) for details.

## Author

Marie Bouteyre — [GitHub](https://github.com/MarieB286)