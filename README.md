# Radar-And-Weather

A Streamlit weather radar app using public NOAA/NWS radar and forecast data.

## What it does

This MVP shows Kansas City-area radar with:

- Animated NWS radar loop by station
- Static latest radar image by station
- Interactive radar map overlay using a public NEXRAD WMS layer
- Local National Weather Service forecast for the selected radar site

Default radar station: `KEAX`, Kansas City / Pleasant Hill, Missouri.

## Supported radar stations

- `KEAX` - Kansas City / Pleasant Hill, MO
- `KTWX` - Topeka, KS
- `KICT` - Wichita, KS
- `KOAX` - Omaha, NE
- `KSGF` - Springfield, MO

## Install

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Data sources

- National Weather Service radar images
- National Weather Service forecast API
- Iowa State University Mesonet NEXRAD WMS overlay

No paid API keys are required.

## Known limitations

- This first version does not decode raw Level II radar files.
- Radar animation uses the public NWS station loop image.
- Interactive map overlay is a live WMS layer, not a custom tiled radar product.
- Radar data can lag by several minutes.
- Some station images may occasionally be unavailable during maintenance or outages.

## Future enhancements

- Add raw NEXRAD Level II file discovery and download.
- Decode base reflectivity sweeps with Py-ART.
- Render transparent sweep frames.
- Add velocity, storm-relative velocity, and dual-pol products.
- Add warning polygons and storm-cell tracking.
- Deploy to Streamlit Community Cloud.
