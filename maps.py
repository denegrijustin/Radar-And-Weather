"""Folium map builder with a public radar WMS overlay."""

from __future__ import annotations

import folium


def build_radar_map(lat: float, lon: float, zoom: int = 7) -> folium.Map:
    """Build a map with an Iowa State Mesonet NEXRAD WMS overlay.

    This gives the app a live map-style radar layer without requiring heavy radar
    decoding libraries in the first version.
    """
    m = folium.Map(location=[lat, lon], zoom_start=zoom, control_scale=True)

    folium.TileLayer("OpenStreetMap", name="Street Map", control=True).add_to(m)

    folium.raster_layers.WmsTileLayer(
        url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0q.cgi",
        name="NEXRAD Reflectivity Overlay",
        layers="nexrad-n0q-900913",
        fmt="image/png",
        transparent=True,
        version="1.1.1",
        attr="Iowa State University Mesonet / NOAA NEXRAD",
        overlay=True,
        control=True,
        show=True,
    ).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup="Selected radar site",
        tooltip="Radar site",
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m
