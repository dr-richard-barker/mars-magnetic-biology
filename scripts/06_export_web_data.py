#!/usr/bin/env python3
"""
06_export_web_data.py

Exports data for the interactive 3D Three.js Mars WebGL globe and data explorer:
- docs/assets/js/mag_field_data.json: JSON dataset of landing sites and global statistics
- docs/assets/img/mars_mag_texture.png: 2048x1024 equirectangular magnetic field heatmap texture
"""

import os
import json
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
GRID_FILE = PROCESSED_DIR / "mars_mag_field_grid.csv"
SITES_FILE = PROCESSED_DIR / "mars_landing_sites_magnetic.csv"

def ensure_directories():
    (ASSETS_DIR / "js").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "data").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "img").mkdir(parents=True, exist_ok=True)

def export_json():
    logging.info("Exporting Mars magnetic data to JSON...")
    df_sites = pd.read_csv(SITES_FILE)
    df_grid = pd.read_csv(GRID_FILE)
    
    # Calculate global statistics
    stats = {
        "global_mean_400km": round(float(df_grid['Bmag'].mean()), 2),
        "global_median_400km": round(float(df_grid['Bmag'].median()), 2),
        "global_max_400km": round(float(df_grid['Bmag'].max()), 2),
        "northern_lowlands_mean": round(float(df_grid[df_grid['lat'] > 0]['Bmag'].mean()), 2),
        "southern_highlands_mean": round(float(df_grid[df_grid['lat'] < 0]['Bmag'].mean()), 2),
        "total_sites": int(len(df_sites)),
        "high_field_sites": int(len(df_sites[df_sites['classification'] == 'high-field'])),
        "moderate_field_sites": int(len(df_sites[df_sites['classification'] == 'moderate'])),
        "low_field_sites": int(len(df_sites[df_sites['classification'] == 'low/null-field'])),
        "reference_earth_gmf": 50000.0
    }
    
    sites_list = []
    for _, row in df_sites.iterrows():
        sites_list.append({
            "name": str(row['name']),
            "mission": str(row['mission']),
            "lat": float(row['lat']),
            "lon": float(row['lon']),
            "Bmag_400km": float(row['Bmag_400km']),
            "Br": float(row['Br']),
            "Btheta": float(row['Btheta']),
            "Bphi": float(row['Bphi']),
            "B_surface_est": float(row['B_surface_est']),
            "classification": str(row['classification']),
            "geological_setting": str(row['geological_setting']),
            "source": str(row['source'])
        })
        
    web_payload = {
        "metadata": {
            "title": "Martian Crustal Magnetic Field Heterogeneity & Biological Landing Site Assessment",
            "model": "Langlais et al. (2019) MAVEN/MGS Model",
            "doi": "10.1029/2019JE005979",
            "authors": [
                "Richard Barker", "Adriana Kaley Sanchez", "Manisha Dagar",
                "Katrina Boland", "Cauê Sciascia Borlina", "D. Marshall Porterfield"
            ],
            "affiliation": "Purdue University",
            "version": "1.0.0"
        },
        "statistics": stats,
        "landing_sites": sites_list
    }
    
    js_json_path = ASSETS_DIR / "js" / "mag_field_data.json"
    data_json_path = ASSETS_DIR / "data" / "mag_field_data.json"
    
    with open(js_json_path, 'w') as f:
        json.dump(web_payload, f, indent=2)
    with open(data_json_path, 'w') as f:
        json.dump(web_payload, f, indent=2)
        
    logging.info(f"Saved web JSON to {js_json_path} and {data_json_path}")

def export_texture():
    logging.info("Generating equirectangular magnetic field texture (2048x1024)...")
    df_grid = pd.read_csv(GRID_FILE)
    
    lats = np.linspace(90, -90, 1024)
    lons = np.linspace(0, 360, 2048)
    
    grid_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    old_lats = np.sort(df_grid['lat'].unique())
    old_lons = np.sort(df_grid['lon'].unique())
    
    from scipy.interpolate import RegularGridInterpolator
    interp = RegularGridInterpolator((old_lats, old_lons), grid_bmag, bounds_error=False, fill_value=None)
    
    lon_mesh, lat_mesh = np.meshgrid(lons, lats)
    points = np.stack([lat_mesh.flatten(), lon_mesh.flatten()], axis=1)
    bmag_highres = interp(points).reshape(1024, 2048)
    
    # Normalize with perceptual curve
    vmax = np.percentile(bmag_highres, 98.5)
    normalized = np.clip(bmag_highres / vmax, 0, 1)
    
    # Apply colormap
    cmap = plt.get_cmap('inferno')
    rgba = cmap(normalized)
    
    # Set subtle transparency for near-null field regions (< 5 nT) to blend smoothly with Mars surface
    alpha_mask = np.clip(bmag_highres / 25.0, 0.25, 0.95)
    rgba[:, :, 3] = alpha_mask
    
    img_array = (rgba * 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
    texture_path = ASSETS_DIR / "img" / "mars_mag_texture.png"
    img.save(texture_path, format="PNG")
    logging.info(f"Saved 2048x1024 Mars magnetic texture to {texture_path}")

def main():
    logging.info("Starting web data export for Mars...")
    ensure_directories()
    export_json()
    export_texture()
    logging.info("Mars web data export complete.")

if __name__ == "__main__":
    main()
