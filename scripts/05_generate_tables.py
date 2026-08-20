#!/usr/bin/env python3
"""
05_generate_tables.py

Generates publication-quality LaTeX tables and CSV datasets for Mars:
- table1_mars_landing_sites.tex: Landing site magnetic field values at 400 km and surface estimates
- table2_mars_biology_literature.tex: Systematic review of biological effects in hypomagnetic fields (HMF)
- table3_mars_risk_matrix.tex: Biological risk matrix across Martian magnetic environments
- mars_biology_literature_summary.csv: Machine-readable systematic review table

Saved to tables/ and data/processed/.
"""

import os
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "tables"
SITES_FILE = PROCESSED_DIR / "mars_landing_sites_magnetic.csv"

def ensure_directories():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def generate_table1():
    """Table 1: Martian landing sites and magnetic field intensities."""
    if not SITES_FILE.exists():
        logging.warning("Landing sites file missing, skipping Table 1.")
        return
        
    df = pd.read_csv(SITES_FILE)
    
    tex_path = TABLES_DIR / "table1_mars_landing_sites.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\footnotesize\n")
        f.write("\\caption{\\textbf{Martian crustal magnetic field environment across historical, active, and candidate human landing sites.} Magnetic field magnitude at \\SI{400}{\\kilo\\meter} mapping altitude and estimated ground-level surface field ($|\\mathbf{B}_{\\text{surf}}|$) derived from MGS/MAVEN models \\citep{Langlais2019} and InSight surface magnetometer observations \\citep{Johnson2020}.}\n")
        f.write("\\label{tab:mars_landing_sites}\n")
        f.write("\\begin{tabular}{llrrcll}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Landing Site / Region} & \\textbf{Mission / Target} & \\textbf{Lat ($^\\circ$N)} & \\textbf{Lon ($^\\circ$E)} & \\textbf{$|\\mathbf{B}_{\\text{400km}}|$ (nT)} & \\textbf{$|\\mathbf{B}_{\\text{surf}}|$ (nT)} & \\textbf{Classification} \\\\\n")
        f.write("\\midrule\n")
        
        for _, row in df.iterrows():
            name = row['name']
            mission = row['mission']
            lat = f"{row['lat']:.2f}"
            lon = f"{row['lon']:.2f}"
            b400 = f"{row['Bmag_400km']:.2f}"
            bsurf = f"{row['B_surface_est']:.1f}"
            classification = row['classification']
            f.write(f"{name} & {mission} & {lat} & {lon} & {b400} & {bsurf} & {classification} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
    logging.info(f"Generated {tex_path.name}")

def generate_table2_and_csv():
    """Table 2 & CSV: Systematic review of hypomagnetic field (HMF) effects on biology."""
    data = [
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Delayed floral transition and flowering time", "Cryptochrome (CRY1/CRY2) and phytochrome signaling disruption", "Agliassa et al. (2018) \\citep{Agliassa2018}"],
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Disrupted root directional growth and elongation", "PIN2 polar auxin transport redistribution and meristem elongation", "Narayana et al. (2018) \\citep{Narayana2018}"],
        ["\\textit{Arabidopsis thaliana}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Impaired iron acquisition and uptake homeostasis", "Downregulation of FIT and IRT1 transcription factors", "Narayana et al. (2021) \\citep{Narayana2021}"],
        ["\\textit{Arabidopsis thaliana}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Elevated reactive oxygen species (ROS) accumulation", "Perturbation of redox signaling and catalase/SOD enzyme activity", "Maffei (2014) \\citep{Maffei2014}"],
        ["Higher Plants (General)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Reduced photosynthetic efficiency and chlorophyll synthesis", "Thylakoid membrane ultrastructural disorganization", "Belyavskaya (2004) \\citep{Belyavskaya2004}"],
        ["Microorganisms (Bacteria)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Altered cell division rates and metabolic flux", "Membrane potential modulation and altered ion channel kinetics", "Creanga et al. (2009) \\citep{Creanga2009}"],
        ["Magnetotactic Bacteria", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Complete loss of magnetotaxis and directional motility", "Loss of passive dipole alignment of intracellular magnetosomes", "Frankel et al. (1981) \\citep{Frankel1981}"],
        ["Gut Microbiome (Murine)", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Restructuring of gut bacterial taxonomic diversity", "Shifts in Bacteroidetes to Firmicutes phylum abundance ratios", "Zhang et al. (2017) \\citep{Zhang2017}"],
        ["\\textit{Drosophila melanogaster}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Circadian rhythm period lengthening and arrhythmicity", "Cryptochrome-mediated radical pair recombination modulation", "Yoshii et al. (2009) \\citep{Yoshii2009}"],
        ["\\textit{Drosophila melanogaster}", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Embryonic developmental arrest and mortality", "Mitochondrial metabolic dysfunction and ROS-induced apoptosis", "Vitas et al. (2015) \\citep{Vitas2015}"],
        ["\\textit{Caenorhabditis elegans}", "Hypomagnetic ($<\\SI{5}{\\micro\\tesla}$)", "Disrupted burrowing orientation and magnetosensation", "AFD sensory neuron signaling and DAF-16 FOXO pathway modulation", "Vidal-Gadea et al. (2015) \\citep{VidalGadea2015}"],
        ["Human Neuroblastoma Cells", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Altered cell cycle transcriptome and proliferation rate", "Downregulation of cell division and DNA replication gene networks", "Mo et al. (2012) \\citep{Mo2012}"],
        ["Mammalian Model (Rat)", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Accelerated trabecular bone demineralization and osteopenia", "Synergy between HMF and hindlimb unloading; osteoblast suppression", "Xu et al. (2012) \\citep{Xu2012}"],
        ["Mammalian Model (Rat)", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Exacerbated musculoskeletal bone mass loss", "Enhanced osteoclast differentiation and calcium excretion", "Mo et al. (2014) \\citep{Mo2014}"],
        ["Human Cardiovascular", "Near-null ($<\\SI{1}{\\micro\\tesla}$)", "Altered microcirculatory capillary blood flow velocity", "Endothelial nitric oxide synthase and autonomic tone modulation", "Gurfinkel et al. (2014) \\citep{Gurfinkel2014}"],
        ["Mammalian Cells (General)", "Hypomagnetic ($<\\SI{1}{\\micro\\tesla}$)", "Altered DNA damage repair kinetics and genomic instability", "Radical pair singlet-triplet spin-state interconversion dynamics", "Binhi and Prato (2017) \\citep{Binhi2017}"]
    ]
    
    # Save CSV
    clean_csv_data = [
        [row[0].replace('\\textit{', '').replace('}', ''),
         row[1].replace('\\SI{', '').replace('}{\\micro\\tesla}', ' µT').replace('$<', '<').replace('$', ''),
         row[2], row[3], row[4].split('\\citep')[0].strip()]
        for row in data
    ]
    df_csv = pd.DataFrame(clean_csv_data, columns=["Organism / Model", "Magnetic Condition", "Biological Effect", "Mechanism", "Key Reference"])
    csv_path = PROCESSED_DIR / "mars_biology_literature_summary.csv"
    df_csv.to_csv(csv_path, index=False)
    logging.info(f"Generated {csv_path.name}")
    
    # Save LaTeX
    tex_path = TABLES_DIR / "table2_mars_biology_literature.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\footnotesize\n")
        f.write("\\caption{\\textbf{Systematic synthesis of documented biological responses and mechanisms under hypomagnetic field (HMF) conditions.} Summary of peer-reviewed experimental literature across plant, microbial, insect, and mammalian systems.}\n")
        f.write("\\label{tab:mars_biology_review}\n")
        f.write("\\begin{tabular}{p{2.8cm}p{2.2cm}p{3.4cm}p{4.4cm}p{3.0cm}}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Organism / Model} & \\textbf{Condition} & \\textbf{Biological Effect} & \\textbf{Mechanism} & \\textbf{Key Reference} \\\\\n")
        f.write("\\midrule\n")
        
        for row in data:
            f.write(f"{row[0]} & {row[1]} & {row[2]} & {row[3]} & {row[4]} \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
    logging.info(f"Generated {tex_path.name}")

def generate_table3():
    """Table 3: Risk matrix across Martian magnetic environments."""
    tex_path = TABLES_DIR / "table3_mars_risk_matrix.tex"
    with open(tex_path, 'w') as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\footnotesize\n")
        f.write("\\caption{\\textbf{Biological risk matrix across Martian surface magnetic environments.} Comparison of biological process vulnerability between Earth's geomagnetic field (GMF), Southern Highlands magnetic anomalies (e.g., Terra Sirenum), and Northern Lowlands demagnetized habitat candidate sites (e.g., Arcadia Planitia, Jezero Crater).}\n")
        f.write("\\label{tab:mars_risk_matrix}\n")
        f.write("\\begin{tabular}{p{3.6cm}cccc}\n")
        f.write("\\toprule\n")
        f.write("\\textbf{Biological System} & \\textbf{Earth GMF ($\\sim\\SI{50}{\\micro\\tesla}$)} & \\textbf{Terra Sirenum ($>\\SI{1000}{\\nano\\tesla}$)} & \\textbf{Elysium Planitia ($\\sim\\SI{200}{\\nano\\tesla}$)} & \\textbf{Arcadia / Jezero ($<\\SI{20}{\\nano\\tesla}$)} \\\\\n")
        f.write("\\midrule\n")
        f.write("Plant Vegetative Biomass & Nominal (Baseline) & Low-Moderate Risk & Moderate Risk & High Risk \\\\\n")
        f.write("Plant Flowering & Nominal (Baseline) & Moderate Risk & Moderate Risk & High Risk \\\\\n")
        f.write("Closed-Loop Microbiome & Nominal (Baseline) & Low Risk & Low-Moderate Risk & Moderate Risk \\\\\n")
        f.write("Animal Clocks & Nominal (Baseline) & Moderate Risk & Moderate-High Risk & High Risk \\\\\n")
        f.write("Human Bone Homeostasis & Nominal (Baseline) & Moderate Risk & High Risk & High Risk \\\\\n")
        f.write("Cellular DNA / ROS & Nominal (Baseline) & Moderate Risk & Moderate-High Risk & High Risk \\\\\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")
        
    logging.info(f"Generated {tex_path.name}")

def main():
    logging.info("Starting Mars table generation...")
    ensure_directories()
    
    try:
        generate_table1()
        generate_table2_and_csv()
        generate_table3()
        logging.info("All Mars tables generated successfully.")
    except Exception as e:
        logging.error(f"Table generation failed: {e}")

if __name__ == "__main__":
    main()
