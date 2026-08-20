#!/usr/bin/env python3
"""
03_identify_landing_sites.py

Maps historical, contemporary, and candidate human landing sites on Mars to
local crustal magnetic field values (orbital at 400 km and surface estimates)
via bilinear interpolation.

Classifies each site from an astrobiology, space physiology, and habitat perspective:
- High-Field: |B| > 80 nT (at 400 km) or surface > 800 nT (partial plasma shielding)
- Moderate: 20 nT <= |B| <= 80 nT
- Low/Null-Field: |B| < 20 nT (severe hypomagnetic environment relative to Earth's 50,000 nT)

Output: data/processed/mars_landing_sites_magnetic.csv
"""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.interpolate import RegularGridInterpolator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GRID_FILE = PROCESSED_DIR / "mars_mag_field_grid.csv"
OUTPUT_FILE = PROCESSED_DIR / "mars_landing_sites_magnetic.csv"

# Comprehensive Mars Landing Sites Database with High-Precision Surface Telemetry
MARS_LANDING_SITES = [
    # Contemporary NASA Surface Assets
    {"name": "Perseverance (Jezero Crater)", "lat": 18.445, "lon": 77.451, "mission": "NASA Mars 2020",
     "surface_measured_nt": None, "geological_setting": "Octavia E. Butler Landing / Delta Fan"},
    {"name": "Curiosity (Gale Crater)", "lat": -4.589, "lon": 137.442, "mission": "NASA MSL",
     "surface_measured_nt": None, "geological_setting": "Bradbury Landing / Crater Interior"},
    {"name": "InSight (Elysium Planitia)", "lat": 4.502, "lon": 135.623, "mission": "NASA Discovery",
     "surface_measured_nt": 2013.0, "geological_setting": "Smooth Volcanic Plain (IFG Ground Truth)"},
    
    # Historical NASA Rovers & Landers
    {"name": "Opportunity (Meridiani Planum)", "lat": -1.946, "lon": 354.473, "mission": "NASA MER-B",
     "surface_measured_nt": None, "geological_setting": "Challenger Memorial Station / Hematite Plain"},
    {"name": "Spirit (Gusev Crater)", "lat": -14.568, "lon": 175.473, "mission": "NASA MER-A",
     "surface_measured_nt": None, "geological_setting": "Columbia Memorial Station / Anomaly Margin"},
    {"name": "Phoenix (Vastitas Borealis)", "lat": 68.219, "lon": 234.251, "mission": "NASA Scout",
     "surface_measured_nt": None, "geological_setting": "Green Valley / Polar Subsurface Ice Sheet"},
    {"name": "Viking 1 (Chryse Planitia)", "lat": 22.480, "lon": 312.050, "mission": "NASA Viking",
     "surface_measured_nt": None, "geological_setting": "Thomas Mutch Memorial Station / Outflow Plain"},
    {"name": "Viking 2 (Utopia Planitia)", "lat": 47.967, "lon": 134.280, "mission": "NASA Viking",
     "surface_measured_nt": None, "geological_setting": "Demagnetized Impact Lowland Plain"},
     
    # International Surface Missions
    {"name": "Zhurong (Utopia Planitia)", "lat": 25.066, "lon": 109.925, "mission": "CNSA Tianwen-1",
     "surface_measured_nt": None, "geological_setting": "Southern Utopia Sedimentary Basin"},
    {"name": "ExoMars (Oxia Planum)", "lat": 18.275, "lon": 335.368, "mission": "ESA/Rosalind Franklin",
     "surface_measured_nt": None, "geological_setting": "Clay-Rich Lowland Lacustrine Plain"},
     
    # Candidate Human Exploration & Scientific Outpost Sites
    {"name": "Arcadia Planitia (Candidate)", "lat": 39.300, "lon": 189.700, "mission": "Human Exploration",
     "surface_measured_nt": None, "geological_setting": "Shallow Subsurface Glacial Ice Candidate"},
    {"name": "Deuteronilus Mensae (Candidate)", "lat": 39.100, "lon": 23.200, "mission": "Human Exploration",
     "surface_measured_nt": None, "geological_setting": "Lobate Debris Aprons / Glacial Slopes"},
    {"name": "Terra Sirenum Anomaly (Science)", "lat": -30.000, "lon": 195.000, "mission": "Human Outpost",
     "surface_measured_nt": None, "geological_setting": "Intense Crustal Magnetic Lineation / Mini-Magnetosphere"}
]

def classify_martian_field(bmag_400km, bmag_surface):
    """Classify magnetic field intensity for biological risk assessment."""
    if bmag_400km > 80.0 or bmag_surface > 800.0:
        return "high-field"
    elif bmag_400km >= 20.0 or bmag_surface >= 150.0:
        return "moderate"
    else:
        return "low/null-field"

def main():
    logging.info("Starting Mars landing site identification and classification...")
    
    if not GRID_FILE.exists():
        logging.error(f"Grid file missing: {GRID_FILE}")
        raise FileNotFoundError("Run 02_process_magnetic_data.py first.")
        
    df_grid = pd.read_csv(GRID_FILE)
    
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    
    grid_bmag = df_grid.pivot(index='lat', columns='lon', values='Bmag').values
    grid_br = df_grid.pivot(index='lat', columns='lon', values='Br').values
    grid_btheta = df_grid.pivot(index='lat', columns='lon', values='Btheta').values
    grid_bphi = df_grid.pivot(index='lat', columns='lon', values='Bphi').values
    grid_surface = df_grid.pivot(index='lat', columns='lon', values='Bmag_surface').values
    
    interp_bmag = RegularGridInterpolator((lats, lons), grid_bmag, bounds_error=False, fill_value=None)
    interp_br = RegularGridInterpolator((lats, lons), grid_br, bounds_error=False, fill_value=None)
    interp_btheta = RegularGridInterpolator((lats, lons), grid_btheta, bounds_error=False, fill_value=None)
    interp_bphi = RegularGridInterpolator((lats, lons), grid_bphi, bounds_error=False, fill_value=None)
    interp_surface = RegularGridInterpolator((lats, lons), grid_surface, bounds_error=False, fill_value=None)
    
    results = []
    
    for site in MARS_LANDING_SITES:
        name = site["name"]
        lat = site["lat"]
        lon = site["lon"] % 360.0
        mission = site["mission"]
        setting = site["geological_setting"]
        measured_surface = site.get("surface_measured_nt")
        
        point = np.array([[lat, lon]])
        bmag = float(interp_bmag(point)[0])
        br = float(interp_br(point)[0])
        btheta = float(interp_btheta(point)[0])
        bphi = float(interp_bphi(point)[0])
        b_surface_model = float(interp_surface(point)[0])
        
        # If ground truth exists (e.g. InSight IFG magnetometer = 2013 nT), record ground truth
        b_surface_effective = measured_surface if measured_surface is not None else b_surface_model
        
        classification = classify_martian_field(bmag, b_surface_effective)
        
        results.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "mission": mission,
            "Bmag_400km": round(bmag, 2),
            "Br": round(br, 2),
            "Btheta": round(btheta, 2),
            "Bphi": round(bphi, 2),
            "B_surface_est": round(b_surface_effective, 1),
            "classification": classification,
            "geological_setting": setting,
            "source": "Langlais et al. (2019) MAVEN/MGS Model"
        })
        
    df_results = pd.DataFrame(results)
    
    logging.info(f"Saving {len(df_results)} classified landing sites to {OUTPUT_FILE}...")
    df_results.to_csv(OUTPUT_FILE, index=False)
    
    counts = df_results['classification'].value_counts()
    logging.info(f"Landing site classification breakdown:\n{counts}")

if __name__ == "__main__":
    main()
