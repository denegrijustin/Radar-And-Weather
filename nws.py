"""Small helpers for public National Weather Service endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

NWS_HEADERS = {
    "User-Agent": "Radar-And-Weather streamlit app; contact: local-user",
    "Accept": "application/geo+json, application/json",
}


@dataclass(frozen=True)
class ForecastSummary:
    location_name: str
    office: str
    grid_x: int
    grid_y: int
    periods: list[dict[str, Any]]


def get_forecast_by_latlon(lat: float, lon: float, timeout: int = 12) -> ForecastSummary:
    """Return a compact NWS forecast for a latitude and longitude.

    The NWS API first resolves a lat/lon to a forecast grid, then returns forecast
    periods from that grid. This requires no API key.
    """
    point_url = f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}"
    point_resp = requests.get(point_url, headers=NWS_HEADERS, timeout=timeout)
    point_resp.raise_for_status()
    point_data = point_resp.json()
    props = point_data["properties"]

    forecast_url = props["forecast"]
    forecast_resp = requests.get(forecast_url, headers=NWS_HEADERS, timeout=timeout)
    forecast_resp.raise_for_status()
    forecast_data = forecast_resp.json()

    relative_location = props.get("relativeLocation", {}).get("properties", {})
    city = relative_location.get("city", "Selected Location")
    state = relative_location.get("state", "")
    location_name = f"{city}, {state}".strip().strip(",")

    return ForecastSummary(
        location_name=location_name,
        office=props.get("gridId", ""),
        grid_x=int(props.get("gridX", 0)),
        grid_y=int(props.get("gridY", 0)),
        periods=forecast_data.get("properties", {}).get("periods", []),
    )


def nws_radar_loop_url(site: str) -> str:
    """Return the public NWS standard radar loop GIF for a station."""
    return f"https://radar.weather.gov/ridge/standard/{site.upper()}_loop.gif"


def nws_radar_static_url(site: str) -> str:
    """Return the public NWS standard static radar image for a station."""
    return f"https://radar.weather.gov/ridge/standard/{site.upper()}_0.gif"
