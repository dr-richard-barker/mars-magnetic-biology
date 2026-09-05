---
layout: default
title: Publications
permalink: /publications/
---

<div class="card">
    <h2>Publications and Research Outputs</h2>
    
    <h3>Preprint & Manuscript Draft</h3>
    <p><strong>Title:</strong> Martian Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites<br>
    <strong>Authors:</strong> Richard Barker*, Adriana Kaley Sanchez, Manisha Dagar, Katrina Boland, Cauê Sciascia Borlina, D. Marshall Porterfield<br>
    <strong>Affiliation:</strong> Purdue University, West Lafayette, IN, USA<br>
    <strong>Target Journal:</strong> Nature Publishing Group (<em>npj Microgravity</em>, in preparation)</p>

    <div class="pub-actions">
        <a href="{{ site.baseurl }}/assets/pdf/manuscript_npj_microgravity.pdf" class="btn btn-primary"><i class="fas fa-file-pdf"></i> Download Manuscript PDF (npj Microgravity Style)</a>
        <a href="{{ site.baseurl }}/assets/pdf/supplementary_information.pdf" class="btn btn-secondary"><i class="fas fa-file-alt"></i> Download Supplementary Info (PDF)</a>
        <a href="https://github.com/dr-richard-barker/mars-magnetic-biology" class="btn btn-secondary"><i class="fab fa-github"></i> GitHub Source</a>
        <a href="https://doi.org/10.5281/zenodo.XXXXXXX" class="btn btn-secondary"><i class="fas fa-database"></i> Zenodo Archive</a>
        <button onclick="copyBibtex()" class="btn btn-secondary"><i class="fas fa-copy"></i> Copy BibTeX</button>
    </div>

    <div style="margin-top: 2rem;">
        <h3>Abstract</h3>
        <p>Mars presents a highly anomalous magnetic environment characterized by the extinction of its ancient core dynamo and the survival of intense, localized crustal magnetic remanence predominantly in its southern ancient cratered highlands. As international space agencies and commercial ventures plan crewed missions and long-term surface habitats on Mars, understanding this complex magnetic landscape is vital for designing bioregenerative life support systems (BLSS), agricultural growth chambers, and astronaut health protocols. In this study, we quantitatively map the Martian crustal magnetic field across 13 contemporary, historical, and candidate human landing sites using calibrated spherical harmonic models derived from Mars Global Surveyor (MGS) and MAVEN orbital magnetometer observations, integrated with InSight surface ground truth. We demonstrate that prospective human habitat sites situated in the ice-rich northern plains (e.g., Arcadia Planitia and Deuteronilus Mensae) and rover landing sites (e.g., Jezero Crater and Oxia Planum) reside in near-null hypomagnetic field (HMF) environments (|B| &lt; 20 nT at surface level, &gt;2,500× weaker than Earth's ~50 µT geomagnetic field). Conversely, southern highland anomaly belts (e.g., Terra Sirenum and Terra Cimmeria) exhibit ground-level field intensities exceeding 1500 nT, generating localized mini-magnetospheres with distinct plasma deflection capabilities. We synthesize the experimental magnetobiology literature across plant growth, root directional auxin transport, cryptochrome signaling, microbial community stability, and mammalian bone demineralization, formulating a biological risk matrix and operational siting framework for Martian surface exploration.</p>
    </div>

    <div style="margin-top: 2rem;">
        <h3>Citation</h3>
        <pre id="bibtex-code">@unpublished{barker2026mars,
  title={Martian Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites},
  author={Barker, Richard and Sanchez, Adriana Kaley and Dagar, Manisha and Boland, Katrina and Borlina, Cau{\^e} Sciascia and Porterfield, D. Marshall},
  year={2026},
  url={https://github.com/dr-richard-barker/mars-magnetic-biology},
  note={Manuscript in preparation; target journal: npj Microgravity. Not yet published --- no DOI, volume or page numbers have been assigned.}
}</pre>
    </div>
</div>

<script>
function copyBibtex() {
    const text = document.getElementById("bibtex-code").innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("BibTeX citation copied to clipboard!");
    });
}
</script>
