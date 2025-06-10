# REW Group Delay Extractor

This Python script fetches Group Delay data from Room EQ Wizard (REW) via its API, processes the data, interpolates it for a finer frequency range (40–250 Hz), and generates visualizations and text outputs. The script retrieves measurement UUIDs, decodes Group Delay data, saves the results to text files, and creates plots showing both raw and interpolated Group Delay values with the maximum value highlighted.

## Features
- Fetches all measurement UUIDs from the REW API.
- Retrieves Group Delay data for each measurement.
- Decodes Big-Endian float32 data from base64-encoded strings.
- Filters data to the 40–250 Hz frequency range.
- Interpolates Group Delay data for smoother visualization.
- Identifies the maximum Group Delay value and its corresponding frequency.
- Saves raw Group Delay data and maximum values to text files.
- Generates and saves plots of Group Delay with interpolated data and max value markers.

## Requirements
- Python 3.x
- Required Python packages:
  - `requests`
  - `numpy`
  - `matplotlib`
  - `scipy`
- A running REW instance with its API enabled (default: `http://localhost:4735`).

Install the required packages using:
```bash
pip install requests numpy matplotlib scipy
