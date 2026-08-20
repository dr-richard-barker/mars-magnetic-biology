#!/usr/bin/env python3
"""
04_generate_figures.py

Generates 7 publication-quality figures for the Mars magnetic biology project.
Adheres strictly to Nature Publishing Group (NPG) guidelines:
- 300 DPI vector PDF & web PNG
- Helvetica/Arial typography
- Single column (88mm) and double column (180mm) widths
- Colorblind-safe colormaps (viridis, plasma, RdBu_r, YlOrRd)

Figures saved to figures/ (PDF) and docs/assets/img/figures/ (PNG).
"""

import os
import logging
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

# Try to import Cartopy
try:
    import cartopy.crs as ccrs
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    logging.info("Cartopy not available. Using native matplotlib coordinate systems.")

# Try to import Seaborn
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GRID_FILE = PROCESSED_DIR / "mars_mag_field_grid.csv"
SITES_FILE = PROCESSED_DIR / "mars_landing_sites_magnetic.csv"
FIG_DIR = PROJECT_ROOT / "figures"
DOCS_FIG_DIR = PROJECT_ROOT / "docs" / "assets" / "img" / "figures"

# Matplotlib configuration for NPG standards
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7.5,
    'axes.labelsize': 8.5,
    'axes.titlesize': 9.0,
    'xtick.labelsize': 7.5,
    'ytick.labelsize': 7.5,
    'legend.fontsize': 7.5,
    'figure.titlesize': 10.0,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def save_fig(fig, name):
    """Save figure to both PDF and PNG in required directories."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_FIG_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_path = FIG_DIR / f"{name}.pdf"
    png_path = DOCS_FIG_DIR / f"{name}.png"
    
    fig.savefig(pdf_path, format='pdf', dpi=300)
    fig.savefig(png_path, format='png', dpi=300)
    logging.info(f"Saved {name}.pdf and .png")

def load_data():
    if not GRID_FILE.exists() or not SITES_FILE.exists():
        logging.error("Required processed CSV files missing. Run scripts 02 and 03 first.")
        raise FileNotFoundError("Processed files missing.")
    df_grid = pd.read_csv(GRID_FILE)
    df_sites = pd.read_csv(SITES_FILE)
    return df_grid, df_sites

def reshape_grid(df_grid, value_col):
    lats = np.sort(df_grid['lat'].unique())
    lons = np.sort(df_grid['lon'].unique())
    z = df_grid.pivot(index='lat', columns='lon', values=value_col).values
    lon_mesh, lat_mesh = np.meshgrid(lons, lats)
    return lon_mesh, lat_mesh, z

def plot_fig1(df_grid):
    """Fig 1: Global |B| crustal magnetic field map at 400 km altitude."""
    lon_mesh, lat_mesh, z_bmag = reshape_grid(df_grid, 'Bmag')
    
    fig = plt.figure(figsize=(7.08, 3.8))
    ax = plt.axes()
    
    # Logarithmic-like scaling for high dynamic range
    vmax = np.nanpercentile(z_bmag, 98.5)
    img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='inferno',
                        vmin=0, vmax=vmax, shading='auto')
    
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 90)
    
    # Annotate key provinces
    ax.text(190, -48, 'Terra Cimmeria / Sirenum\n(Intense Crustal Lineations)', 
            color='white', weight='bold', fontsize=7, ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.5, edgecolor='none'))
    ax.text(70, -42, 'Hellas Basin\n(Demagnetized)', color='cyan', fontsize=6.5, ha='center')
    ax.text(180, 50, 'Northern Lowlands\n(Near-Null Field)', color='yellow', fontsize=6.5, ha='center')
    ax.text(245, 10, 'Tharsis Rise', color='cyan', fontsize=6.5, ha='center')
    
    cbar = plt.colorbar(img, ax=ax, orientation='horizontal', fraction=0.046, pad=0.12)
    cbar.set_label('Total Crustal Magnetic Field Magnitude $|\\mathbf{B}|$ at 400 km Altitude (nT)')
    ax.set_title('Global Distribution of the Martian Crustal Magnetic Field (Langlais et al. 2019 MAVEN/MGS Model)')
    
    save_fig(fig, 'fig1_mars_global_mag_map')
    plt.close(fig)

def plot_fig2(df_grid):
    """Fig 2: Vector components triptych (Br, Btheta, Bphi)."""
    lon_mesh, lat_mesh, z_br = reshape_grid(df_grid, 'Br')
    _, _, z_btheta = reshape_grid(df_grid, 'Btheta')
    _, _, z_bphi = reshape_grid(df_grid, 'Bphi')
    
    vlim = np.nanpercentile(np.abs(z_br), 98)
    
    fig, axes = plt.subplots(3, 1, figsize=(7.08, 7.8), sharex=True)
    components = [
        ('Radial Component $B_r$ (Vertical)', z_br, axes[0]),
        ('Colatitudinal Component $B_\\theta$ (Southward)', z_btheta, axes[1]),
        ('Azimuthal Component $B_\\phi$ (Eastward)', z_bphi, axes[2])
    ]
    
    for title, z_data, ax in components:
        img = ax.pcolormesh(lon_mesh, lat_mesh, z_data, cmap='RdBu_r',
                            vmin=-vlim, vmax=vlim, shading='auto')
        ax.set_ylabel('Latitude (°N)')
        ax.set_title(title, fontsize=8.5, weight='bold')
        ax.set_ylim(-90, 90)
        cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.02, pad=0.02)
        cbar.set_label('nT')
        
    axes[2].set_xlabel('Longitude (°E)')
    axes[2].set_xlim(0, 360)
    plt.tight_layout()
    save_fig(fig, 'fig2_mars_vector_components')
    plt.close(fig)

def plot_fig3(df_grid, df_sites):
    """Fig 3: Landing site locations overlaid on crustal magnetic field map."""
    lon_mesh, lat_mesh, z_bmag = reshape_grid(df_grid, 'Bmag')
    
    fig, ax = plt.subplots(figsize=(7.08, 4.4))
    img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='inferno',
                        vmin=0, vmax=np.nanpercentile(z_bmag, 98), alpha=0.85, shading='auto')
    
    # Plot sites
    markers = {
        'NASA Mars 2020': '*', 'NASA MSL': 'o', 'NASA Discovery': 's',
        'NASA MER-B': 'D', 'NASA MER-A': 'D', 'NASA Scout': '^',
        'NASA Viking': 'v', 'CNSA Tianwen-1': 'p', 'ESA/Rosalind Franklin': 'h',
        'Human Exploration': 'X', 'Human Outpost': 'P'
    }
    colors = {
        'NASA Mars 2020': '#00e676', 'NASA MSL': '#00e5ff', 'NASA Discovery': '#ffea00',
        'NASA MER-B': '#ff9100', 'NASA MER-A': '#ff9100', 'NASA Scout': '#e040fb',
        'NASA Viking': '#ffffff', 'CNSA Tianwen-1': '#ff1744', 'ESA/Rosalind Franklin': '#651fff',
        'Human Exploration': '#76ff03', 'Human Outpost': '#ff3d00'
    }
    
    for mission in df_sites['mission'].unique():
        subset = df_sites[df_sites['mission'] == mission]
        ax.scatter(subset['lon'], subset['lat'], marker=markers.get(mission, 'o'),
                   color=colors.get(mission, 'white'), edgecolor='black', linewidth=0.6,
                   s=65, label=f"{mission} ({len(subset)})", zorder=5)
        
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.32), ncol=4, frameon=True, fontsize=6.5)
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_xlim(0, 360)
    ax.set_ylim(-90, 90)
    
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.03, pad=0.02)
    cbar.set_label('$|\\mathbf{B}|$ at 400 km (nT)')
    ax.set_title('Martian Landing Sites and Candidate Habitats Across Crustal Magnetic Regimes')
    
    plt.tight_layout()
    save_fig(fig, 'fig3_mars_landing_sites_overlay')
    plt.close(fig)

def plot_fig4(df_sites):
    """Fig 4: Bar plot comparing magnetic field magnitude across landing sites."""
    fig, ax = plt.subplots(figsize=(7.08, 4.4))
    
    df_sorted = df_sites.sort_values(by='B_surface_est', ascending=False).reset_index(drop=True)
    
    color_map = {'high-field': '#d32f2f', 'moderate': '#f57c00', 'low/null-field': '#1976d2'}
    bar_colors = [color_map.get(c, '#757575') for c in df_sorted['classification']]
    
    x_pos = np.arange(len(df_sorted))
    bars = ax.bar(x_pos, df_sorted['B_surface_est'], color=bar_colors, edgecolor='black', linewidth=0.5)
    
    # Threshold lines
    ax.axhline(1000.0, color='#d32f2f', linestyle='--', linewidth=0.8, label='High Field (>1000 nT surface)')
    ax.axhline(150.0, color='#f57c00', linestyle=':', linewidth=0.8, label='Moderate Field (150–1000 nT surface)')
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_sorted['name'], rotation=45, ha='right', fontsize=7.0)
    ax.set_ylabel('Estimated Surface Magnetic Field Magnitude $|\\mathbf{B}_{\\text{surf}}|$ (nT)')
    ax.set_title('Crustal Magnetic Field Intensities Across Historical, Active, and Candidate Mars Sites')
    ax.legend(loc='upper right', frameon=True, fontsize=7.0)
    ax.set_yscale('log')
    ax.set_ylim(1, 5000)
    
    # Add values on top of bars
    for bar, val in zip(bars, df_sorted['B_surface_est']):
        y = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, y * 1.15, f"{val:.0f} nT",
                ha='center', va='bottom', fontsize=5.8, rotation=90)
        
    plt.tight_layout()
    save_fig(fig, 'fig4_mars_sites_comparison')
    plt.close(fig)

def plot_fig5():
    """Fig 5: Biological evidence matrix heatmap for Martian hypomagnetic and radiation regimes."""
    organisms = [
        'Arabidopsis thaliana (Crop Plants)',
        'Cyanobacteria & Soil Microbes',
        'Drosophila melanogaster (Insects)',
        'Caenorhabditis elegans (Nematodes)',
        'Mammalian Bone Homeostasis (Osteoblasts)',
        'Human Cellular DNA Repair & ROS'
    ]
    stresses = [
        'Near-Null HMF (<20 nT)',
        'Mini-Magnetosphere (>500 nT)',
        'Synergistic Hypogravity (0.38 g)',
        'Chronic GCR / Radiation',
        'Radical Pair Recombination',
        'Circadian Entrainment (24.6h Sol)'
    ]
    
    # Evidence / Risk Impact score: 0=Negligible, 1=Low, 2=Moderate, 3=High/Documented
    impact_matrix = np.array([
        [3, 1, 3, 3, 3, 2], # Arabidopsis
        [2, 1, 2, 2, 2, 1], # Microbes
        [3, 1, 2, 2, 3, 3], # Drosophila
        [2, 1, 2, 2, 2, 2], # C. elegans
        [3, 2, 3, 3, 3, 1], # Mammalian Bone
        [3, 2, 2, 3, 3, 1], # Human DNA / ROS
    ])
    
    fig, ax = plt.subplots(figsize=(7.08, 4.2))
    im = ax.imshow(impact_matrix, cmap='YlOrRd', vmin=0, vmax=3, aspect='auto')
    
    ax.set_xticks(np.arange(len(stresses)))
    ax.set_yticks(np.arange(len(organisms)))
    ax.set_xticklabels(stresses, rotation=30, ha='right', fontsize=7.5)
    ax.set_yticklabels(organisms, fontsize=7.5)
    
    labels = ['None', 'Low', 'Moderate', 'High']
    for i in range(len(organisms)):
        for j in range(len(stresses)):
            score = impact_matrix[i, j]
            text_color = 'white' if score >= 2 else 'black'
            ax.text(j, i, labels[score], ha="center", va="center", color=text_color, fontsize=7, weight='bold')
            
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', fraction=0.03, pad=0.03, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(['0: None', '1: Low', '2: Moderate', '3: High'])
    cbar.set_label('Biological Vulnerability & Evidence Level')
    ax.set_title('Biological Vulnerability Matrix Under Martian Environmental and Magnetic Regimes')
    
    plt.tight_layout()
    save_fig(fig, 'fig5_mars_biology_matrix')
    plt.close(fig)

def plot_fig_s1(df_grid, df_sites):
    """Fig S1: High-resolution zoom of Terra Sirenum / Terra Cimmeria magnetic anomaly belt."""
    # Filter 120°E to 260°E, 10°S to 80°S
    df_sub = df_grid[(df_grid['lon'] >= 120) & (df_grid['lon'] <= 260) & (df_grid['lat'] >= -80) & (df_grid['lat'] <= -10)]
    lon_mesh, lat_mesh, z_bmag = reshape_grid(df_sub, 'Bmag')
    
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    img = ax.pcolormesh(lon_mesh, lat_mesh, z_bmag, cmap='inferno', vmin=0, vmax=np.nanpercentile(z_bmag, 98), shading='auto')
    
    # Plot any sites in this box
    sub_sites = df_sites[(df_sites['lon'] >= 120) & (df_sites['lon'] <= 260) & (df_sites['lat'] >= -80) & (df_sites['lat'] <= -10)]
    for _, site in sub_sites.iterrows():
        ax.scatter(site['lon'], site['lat'], marker='P', color='#00e5ff', edgecolor='black', s=100, zorder=6)
        ax.text(site['lon'] + 2, site['lat'] + 2, site['name'], color='white', weight='bold', fontsize=7.5,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7, edgecolor='none'))
        
    ax.set_xlabel('Longitude (°E)')
    ax.set_ylabel('Latitude (°N)')
    ax.set_title('Supplementary Figure S1: High-Resolution Terra Sirenum / Cimmeria Crustal Anomaly Belt')
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', fraction=0.03, pad=0.03)
    cbar.set_label('$|\\mathbf{B}|$ at 400 km (nT)')
    
    plt.tight_layout()
    save_fig(fig, 'fig_S1_terra_sirenum_detail')
    plt.close(fig)

def plot_fig_s2(df_grid, df_sites):
    """Fig S2: Global histogram of Martian crustal field with landing site markings."""
    fig, ax = plt.subplots(figsize=(7.08, 4.0))
    
    bmag_vals = df_grid['Bmag'].values
    ax.hist(bmag_vals, bins=100, log=True, color='#8d6e63', edgecolor='white', linewidth=0.4)
    
    mean_val = np.mean(bmag_vals)
    median_val = np.median(bmag_vals)
    
    ax.axvline(median_val, color='black', linestyle='--', linewidth=1.0, label=f'Global Median ({median_val:.2f} nT)')
    ax.axvline(mean_val, color='#d84315', linestyle='-', linewidth=1.0, label=f'Global Mean ({mean_val:.2f} nT)')
    
    # Mark specific sites
    jezero_b = df_sites[df_sites['name'].str.contains('Perseverance')]['Bmag_400km'].values[0]
    insight_b = df_sites[df_sites['name'].str.contains('InSight')]['Bmag_400km'].values[0]
    sirenum_b = df_sites[df_sites['name'].str.contains('Terra Sirenum')]['Bmag_400km'].values[0]
    
    ax.axvline(jezero_b, color='#00c853', linestyle='-.', linewidth=1.2, label=f'Perseverance Jezero ({jezero_b:.1f} nT)')
    ax.axvline(insight_b, color='#ffd600', linestyle='-.', linewidth=1.2, label=f'InSight Elysium ({insight_b:.1f} nT)')
    ax.axvline(sirenum_b, color='#d50000', linestyle=':', linewidth=1.4, label=f'Terra Sirenum Outpost ({sirenum_b:.1f} nT)')
    
    ax.set_xlabel('Total Crustal Magnetic Field Magnitude $|\\mathbf{B}|$ at 400 km Altitude (nT)')
    ax.set_ylabel('Number of Grid Points (Log Scale)')
    ax.set_title('Supplementary Figure S2: Global Distribution of Martian Crustal Magnetic Field Magnitude')
    ax.legend(loc='upper right', frameon=True, fontsize=7.0)
    
    plt.tight_layout()
    save_fig(fig, 'fig_S2_mars_field_histogram')
    plt.close(fig)

def main():
    logging.info("Starting figure generation pipeline for Mars...")
    df_grid, df_sites = load_data()
    
    plot_fig1(df_grid)
    plot_fig2(df_grid)
    plot_fig3(df_grid, df_sites)
    plot_fig4(df_sites)
    plot_fig5()
    plot_fig_s1(df_grid, df_sites)
    plot_fig_s2(df_grid, df_sites)
    
    logging.info("Mars figure generation pipeline completed successfully.")

if __name__ == "__main__":
    main()
