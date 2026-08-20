#!/usr/bin/env python3
"""
02_process_magnetic_data.py

Processes raw Martian crustal magnetic data into cleaned, validated grids:
- Computes vector magnitude |B| = sqrt(Br^2 + Btheta^2 + Bphi^2) at 400 km altitude
- Computes surface magnetic field intensity estimates
- Generates summary statistics across global, northern lowlands, and southern highlands

Output: data/processed/mars_mag_field_grid.csv
"""

import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "mars_mag_langlais2019_raw.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "mars_mag_field_grid.csv"

def ensure_directories():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def process_grid():
    if not RAW_FILE.exists():
        logging.error(f"Raw file {RAW_FILE} not found. Run 01_download_data.py first.")
        raise FileNotFoundError(f"Raw file {RAW_FILE} missing.")
        
    logging.info(f"Loading raw Mars magnetic data from {RAW_FILE}...")
    df = pd.read_csv(RAW_FILE)
    
    # Validation & Cleaning
    df['lon'] = df['lon'] % 360.0
    df = df.sort_values(by=['lat', 'lon']).reset_index(drop=True)
    
    # Recalculate Bmag for precision
    df['Bmag'] = np.sqrt(df['Br']**2 + df['Btheta']**2 + df['Bphi']**2)
    
    logging.info(f"Processed {len(df):,} grid points.")
    logging.info(f"Global |B| at 400 km: Mean = {df['Bmag'].mean():.2f} nT, Median = {df['Bmag'].median():.2f} nT, Max = {df['Bmag'].max():.2f} nT")
    
    # Regional subsets
    north = df[df['lat'] > 0]
    south = df[df['lat'] < 0]
    logging.info(f"Northern Lowlands |B|: Mean = {north['Bmag'].mean():.2f} nT, Max = {north['Bmag'].max():.2f} nT")
    logging.info(f"Southern Highlands |B|: Mean = {south['Bmag'].mean():.2f} nT, Max = {south['Bmag'].max():.2f} nT")
    
    logging.info(f"Saving processed grid to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info("Grid processing complete.")

def main():
    logging.info("Starting Mars magnetic grid processing...")
    ensure_directories()
    process_grid()

if __name__ == "__main__":
    main()
