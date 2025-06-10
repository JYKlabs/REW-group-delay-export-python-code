# REW Group Delay Extractor

This Python script extracts Group Delay data from Room EQ Wizard (REW) via its API, processes it within the 40–250 Hz frequency range, applies cubic interpolation for smoother visualization, and generates text files and plots. It retrieves measurement UUIDs, decodes base64-encoded Group Delay data, and outputs raw data, maximum values, and visualizations.

## Features
- Fetches all measurement UUIDs from the REW API.
- Retrieves Group Delay data for each measurement, decoded from base64-encoded Big-Endian float32 format.
- Processes data within the 40–250 Hz frequency range, respecting the API-provided frequency step (`freqStep`).
- Applies cubic interpolation to generate a smooth Group Delay curve with 210,000 points.
- Identifies the maximum absolute Group Delay value and its corresponding frequency.
- Saves:
  - Raw Group Delay data as text files (`<title> group delay values.txt`).
  - Maximum Group Delay value and frequency (`<title> group delay max value.txt`).
  - Plots showing raw and interpolated Group Delay with the maximum value marked (`<title> group delay graph.png`).
- Ensures unique filenames to prevent overwriting existing files.

## Requirements
- Python 3.x
- Required Python packages:
  - `requests` (for API calls)
  - `numpy` (for numerical processing)
  - `matplotlib` (for plotting)
  - `scipy` (for cubic interpolation)
- A running REW instance with its API enabled (default: `http://localhost:4735`).

Install the required packages using:
```bash
pip install requests numpy matplotlib scipy
