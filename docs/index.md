---
layout: default
title: Home
---

<div class="hero">
    <h1>Martian Crustal Magnetic Field Heterogeneity & Biological Implications</h1>
    <p>A FAIR-compliant planetary geophysics and space biology investigation evaluating hypomagnetic field (HMF) environments across active, historical, and candidate human landing sites on Mars.</p>
    <div class="hero-buttons">
        <a href="{{ site.baseurl }}/globe/" class="btn btn-primary"><i class="fas fa-globe"></i> Explore 3D Mars Globe</a>
        <a href="{{ site.baseurl }}/data/" class="btn btn-secondary"><i class="fas fa-table"></i> Landing Site Explorer</a>
        <a href="{{ site.baseurl }}/publications/" class="btn btn-secondary"><i class="fas fa-file-pdf"></i> Download npj Manuscript</a>
    </div>
</div>

<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">&gt;1500 nT</div>
        <div class="stat-label">Southern Highlands Max Surface Field</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">&lt;20 nT</div>
        <div class="stat-label">Northern Lowlands Surface Field</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">&gt;2,500×</div>
        <div class="stat-label">Field Reduction vs Earth GMF (50 µT)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">13 Sites</div>
        <div class="stat-label">Classified Missions & Habitats</div>
    </div>
</div>

<div class="card">
    <h2>Research Overview</h2>
    <p>Unlike Earth, which maintains an active global dipole dynamo generating a continuous ~50 µT geomagnetic field (GMF), Mars underwent core dynamo extinction approximately 4.1 to 3.9 billion years ago. However, Mars preserves intense localized remnant crustal magnetic fields within its ancient southern cratered crust, creating a profound hemispheric dichotomy:</p>
    <ul>
        <li><strong>Southern Highlands (Terra Sirenum & Terra Cimmeria):</strong> Harbor intense crustal magnetic lineations (>200 nT at 400 km orbital altitude; >1500 nT at ground level) that form mini-magnetospheres capable of deflecting solar wind ions.</li>
        <li><strong>Northern Lowlands & Human Exploration Candidates (Arcadia Planitia, Deuteronilus Mensae, Jezero Crater):</strong> Display extensive impact, thermal, and volcanic demagnetization, exposing surface payloads and habitats to near-null hypomagnetic field (HMF) conditions (<20 nT).</li>
    </ul>
    
    <div class="figure-container">
        <img src="{{ site.baseurl }}/assets/img/figures/fig1_mars_global_mag_map.png" alt="Mars Crustal Magnetic Field Map">
        <div class="figure-caption"><strong>Figure 1 | Global distribution of the Martian crustal magnetic field magnitude.</strong> Total field intensity |B| at 400 km altitude derived from the Langlais et al. (2019) model based on MAVEN and Mars Global Surveyor (MGS) observations.</div>
    </div>
</div>

<div class="card">
    <h2>Biological Risks of Martian Hypomagnetic Environments</h2>
    <p>Terrestrial organisms evolved within Earth's geomagnetic field. Our systematic review reveals that prolonged exposure to hypomagnetic field conditions (<5 µT) induces notable physiological stress:</p>
    
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Target System</th>
                    <th>Observed Phenotypic & Molecular Effect</th>
                    <th>Biological Mechanism</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Crop Plants (<em>Arabidopsis</em>)</strong></td>
                    <td>Delayed floral transition; aberrant root gravitropism; reduced iron uptake</td>
                    <td>Cryptochrome (CRY1/2) signaling; PIN2 polar auxin redistribution; FIT/IRT1 downregulation</td>
                </tr>
                <tr>
                    <td><strong>Microbiome & Biofilms</strong></td>
                    <td>Altered cell division rates; shifts in gut taxonomic community ratios</td>
                    <td>Membrane potential changes; loss of magnetotactic directional motility</td>
                </tr>
                <tr>
                    <td><strong>Mammalian Musculoskeletal</strong></td>
                    <td>Accelerated trabecular bone loss and osteopenia</td>
                    <td>Synergistic suppression of osteoblasts and elevation of osteoclastic bone resorption</td>
                </tr>
                <tr>
                    <td><strong>Cellular DNA & Redox</strong></td>
                    <td>Elevated ROS generation; altered cell cycle transcriptomes</td>
                    <td>Radical pair singlet-triplet spin-state interconversion dynamics</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="figure-container">
        <img src="{{ site.baseurl }}/assets/img/figures/fig5_mars_biology_matrix.png" alt="Biological Risk Matrix">
        <div class="figure-caption"><strong>Figure 5 | Biological vulnerability matrix across Martian environmental stressors.</strong></div>
    </div>
</div>
