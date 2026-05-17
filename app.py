from __future__ import annotations

import streamlit as st
from streamlit_folium import st_folium

from radar.maps import build_radar_map
from radar.nws import get_forecast_by_latlon, nws_radar_loop_url, nws_radar_static_url
from radar.stations import RADAR_STATIONS

st.set_page_config(
    page_title="Radar & Weather",
    page_icon="🌦️",
    layout="wide",
)

st.title("Radar & Weather")
st.caption("Public NOAA/NWS radar and forecast viewer. MVP focused on Kansas City-area radar.")

with st.sidebar:
    st.header("Controls")
    station_code = st.selectbox(
        "Radar station",
        options=list(RADAR_STATIONS.keys()),
        format_func=lambda code: f"{code} - {RADAR_STATIONS[code]['name']}",
        index=0,
    )

    display_mode = st.radio(
        "Radar display",
        options=["Animated NWS loop", "Static NWS image", "Interactive map overlay"],
        index=0,
    )

    st.divider()
    st.write("First version uses public NWS radar images and a public NEXRAD WMS overlay.")
    st.write("Future version can add raw Level II sweep decoding.")

station = RADAR_STATIONS[station_code]
lat = station["lat"]
lon = station["lon"]

left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader(f"{station_code} Radar: {station['name']}")

    if display_mode == "Animated NWS loop":
        st.image(nws_radar_loop_url(station_code), caption="Animated NWS radar loop")
    elif display_mode == "Static NWS image":
        st.image(nws_radar_static_url(station_code), caption="Latest NWS radar image")
    else:
        radar_map = build_radar_map(lat=lat, lon=lon, zoom=station["zoom"])
        st_folium(radar_map, height=650, width=None)

with right:
    st.subheader("Local forecast")
    try:
        forecast = get_forecast_by_latlon(lat, lon)
        st.caption(f"NWS grid: {forecast.office} {forecast.grid_x},{forecast.grid_y} | {forecast.location_name}")

        for period in forecast.periods[:6]:
            with st.container(border=True):
                st.markdown(f"**{period.get('name', 'Forecast')}**")
                temp = period.get("temperature")
                unit = period.get("temperatureUnit", "F")
                wind = period.get("windSpeed", "")
                direction = period.get("windDirection", "")
                short = period.get("shortForecast", "")
                detail = period.get("detailedForecast", "")

                st.write(f"{temp}°{unit} | {short}")
                if wind:
                    st.write(f"Wind: {wind} {direction}".strip())
                st.caption(detail)
    except Exception as exc:
        st.error("Forecast data could not be loaded from the National Weather Service API.")
        st.caption(str(exc))

st.divider()
st.markdown(
    """
### Roadmap
- Add raw NEXRAD Level II ingest from public cloud storage.
- Decode lowest elevation reflectivity sweeps.
- Render transparent PNG frames.
- Add velocity, storm-relative velocity, and dual-pol products.
- Add storm-cell tracking and warning polygons.
"""
)