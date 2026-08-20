# Martian Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

**Authors**: Richard Barker\*, Adriana Kaley Sanchez, Manisha Dagar, Katrina Boland, Cauê Sciascia Borlina, D. Marshall Porterfield  
**Affiliation**: Purdue University, West Lafayette, IN, USA  
**Target Journal**: Nature Publishing Group (*npj Microgravity*)

---

## Overview

This repository contains the complete FAIR-compliant analysis pipeline, publication-quality figures, LaTeX manuscript, and interactive 3D WebGL visualization for a study of Martian crustal magnetic field heterogeneity and its biological implications for landing site selection and surface habitats.

**Key Outputs:**
- 🔴 **Interactive 3D Mars Globe** — [Explore Online](https://dr-richard-barker.github.io/mars-magnetic-biology/globe/)
- 📄 **Manuscript PDF (*npj Microgravity* style)** — [Download PDF](https://dr-richard-barker.github.io/mars-magnetic-biology/assets/pdf/manuscript_npj_microgravity.pdf)
- 📑 **Supplementary Information PDF** — [Download PDF](https://dr-richard-barker.github.io/mars-magnetic-biology/assets/pdf/supplementary_information.pdf)
- 📊 **Publication Figures** — Vector PDFs in `figures/` and PNGs in `docs/assets/img/figures/`
- 📋 **Data Tables** — LaTeX tables in `tables/` and CSVs in `data/processed/`

---

## Scientific Context

Unlike Earth, which maintains an active global dipole generating a continuous $\sim 50\text{ }\mu\text{T}$ geomagnetic field (GMF), Mars experienced core dynamo extinction approximately 4.1 to 3.9 billion years ago. However, Mars preserves intense localized remnant crustal magnetic fields within its ancient southern cratered crust, creating a pronounced planetary dichotomy:

- **Southern Highlands (Terra Sirenum & Terra Cimmeria)**: Harbor intense crustal magnetic lineations ($>200\text{ nT}$ at 400 km altitude; $>1500\text{ nT}$ at ground level) that form mini-magnetospheres capable of deflecting solar wind ions.
- **Northern Lowlands & Human Exploration Candidates (Arcadia Planitia, Deuteronilus Mensae, Jezero Crater)**: Display extensive impact, thermal, and volcanic demagnetization, exposing surface payloads and habitats to near-null hypomagnetic field (HMF) conditions ($<20\text{ nT}$, $>2,500\times$ to $>50,000\times$ weaker than Earth's GMF).

On Earth, the geomagnetic field entrains fundamental biological processes:
- **Plant Morphogenesis & Flowering**: Cryptochrome and phytochrome photoperiodic signaling; PIN2 polar auxin transport; FIT/IRT1 iron uptake transcription
- **Microbial Ecology**: Bacterial cell division rates; gut microbiome taxonomic diversity
- **Mammalian Health**: Trabecular bone homeostasis (accelerated osteopenia under HMF); radical pair spin-state recombination kinetics; ROS regulation

This project maps the crustal magnetic environment across 13 Mars landing sites and synthesizes the literature to establish an actionable biological risk assessment matrix.

---

## Data Sources

| Dataset | Coverage | Source | DOI |
|---------|----------|--------|-----|
| Martian Crustal Magnetic Field Model | Global ($90^\circ\text{S}$–$90^\circ\text{N}$, $0^\circ$–$360^\circ\text{E}$), 400 km alt | MGS MAG/ER \& MAVEN / Langlais et al. 2019 | [10.1029/2019JE005979](https://doi.org/10.1029/2019JE005979) |
| InSight Surface Magnetometer Ground Truth | Elysium Planitia ($4.50^\circ\text{N}$, $135.62^\circ\text{E}$) | NASA InSight / Johnson et al. 2020 | [10.1038/s41561-020-0536-x](https://doi.org/10.1038/s41561-020-0536-x) |

---

## Quickstart

### Prerequisites
- Python 3.11+
- Tectonic or standard TeX Live / MacTeX distribution

### Installation

```bash
git clone https://github.com/dr-richard-barker/mars-magnetic-biology.git
cd mars-magnetic-biology

# Using pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Complete Pipeline

```bash
make all        # Runs download -> analysis -> figures -> tables -> web -> manuscript
make validate   # Validates FAIR compliance (.zenodo.json, CITATION.cff, YAML)
```

---

## Repository Structure

```
├── data/raw/              # Raw spherical harmonic grid datasets
├── data/processed/        # Cleaned, processed CSV grids and site catalogs
├── scripts/               # Pipeline modules (01–06)
├── figures/               # Publication-quality vector PDF figures (NPG format)
├── tables/                # LaTeX-ready data tables
├── manuscript/            # Complete LaTeX manuscript (npj Microgravity style)
├── docs/                  # GitHub Pages site with interactive 3D WebGL globe
├── CITATION.cff           # Machine-readable citation metadata
├── .zenodo.json           # Zenodo deposit metadata
├── environment.yml        # Conda environment
├── Makefile               # Pipeline orchestration
└── LICENSE                # MIT & CC-BY-4.0 licenses
```

---

## How to Cite

```bibtex
@article{barker2026mars,
  title={Martian Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites},
  author={Barker, Richard and Sanchez, Adriana Kaley and Dagar, Manisha and Boland, Katrina and Borlina, Cau{\^e} Sciascia and Porterfield, D. Marshall},
  journal={npj Microgravity},
  year={2026},
  volume={12},
  pages={46},
  doi={10.1038/s41526-026-00452-y},
  url={https://github.com/dr-richard-barker/mars-magnetic-biology}
}
```

---

## License

Code and data analysis pipelines are licensed under [MIT](LICENSE). Documentation, manuscript text, and figures are licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). NASA MGS, MAVEN, and InSight data are in the US public domain.
