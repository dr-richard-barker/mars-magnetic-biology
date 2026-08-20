---
layout: default
title: Data Explorer
permalink: /data/
---

<div class="card">
    <h2>Martian Landing Sites & Candidate Habitats Data Explorer</h2>
    <p>Interactive catalog of magnetic field parameters extracted from MGS/MAVEN models and InSight surface observations. Filter and search across active rovers, historical landers, and future candidate human habitats.</p>
    
    <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
        <input type="text" id="site-search" placeholder="Search landing sites or missions..." style="flex: 1; min-width: 240px; padding: 0.6rem 1rem; border-radius: 6px; border: 1px solid var(--border-color); font-size: 0.9rem;">
        <select id="class-filter" style="padding: 0.6rem 1rem; border-radius: 6px; border: 1px solid var(--border-color); font-size: 0.9rem;">
            <option value="all">All Classifications</option>
            <option value="high-field">High-Field (&gt;1000 nT)</option>
            <option value="moderate">Moderate Field (150–1000 nT)</option>
            <option value="low/null-field">Low/Null-Field (&lt;150 nT)</option>
        </select>
        <a href="{{ site.baseurl }}/assets/data/mag_field_data.json" download="mars_mag_field_data.json" class="btn btn-secondary"><i class="fas fa-download"></i> JSON Data</a>
        <a href="https://github.com/dr-richard-barker/mars-magnetic-biology/raw/main/data/processed/mars_landing_sites_magnetic.csv" class="btn btn-secondary"><i class="fas fa-file-csv"></i> CSV Data</a>
    </div>

    <div class="table-responsive">
        <table id="sites-table">
            <thead>
                <tr>
                    <th>Site / Region</th>
                    <th>Mission / Entity</th>
                    <th>Lat (°N)</th>
                    <th>Lon (°E)</th>
                    <th>|B| 400km (nT)</th>
                    <th>|B| Surface Est (nT)</th>
                    <th>Classification</th>
                </tr>
            </thead>
            <tbody id="sites-tbody">
                <!-- Dynamically Populated -->
            </tbody>
        </table>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('sites-tbody');
    const searchInput = document.getElementById('site-search');
    const classFilter = document.getElementById('class-filter');
    let allSites = [];

    const currentPath = window.location.pathname;
    const basePath = currentPath.includes('/mars-magnetic-biology') ? '/mars-magnetic-biology' : '';
    const dataUrl = `${basePath}/assets/data/mag_field_data.json`;

    fetch(dataUrl)
        .then(res => res.json())
        .then(data => {
            allSites = data.landing_sites || [];
            renderTable(allSites);
        })
        .catch(err => {
            console.error("Error loading sites data:", err);
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: red;">Failed to load data.</td></tr>';
        });

    function renderTable(sites) {
        tbody.innerHTML = '';
        if (sites.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #64748b;">No matching landing sites found.</td></tr>';
            return;
        }

        sites.forEach(site => {
            const tr = document.createElement('tr');
            const badgeClass = site.classification === 'high-field' ? 'badge-high' : 
                              (site.classification === 'moderate' ? 'badge-moderate' : 'badge-low');

            tr.innerHTML = `
                <td><strong>${site.name}</strong><br><small style="color: #64748b;">${site.geological_setting}</small></td>
                <td>${site.mission}</td>
                <td>${site.lat.toFixed(2)}</td>
                <td>${site.lon.toFixed(2)}</td>
                <td>${site.Bmag_400km.toFixed(2)}</td>
                <td><strong>${site.B_surface_est.toFixed(1)}</strong></td>
                <td><span class="badge ${badgeClass}">${site.classification}</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    function filterData() {
        const query = searchInput.value.toLowerCase();
        const selectedClass = classFilter.value;

        const filtered = allSites.filter(site => {
            const matchesQuery = site.name.toLowerCase().includes(query) || 
                                 site.mission.toLowerCase().includes(query) ||
                                 site.geological_setting.toLowerCase().includes(query);
            const matchesClass = selectedClass === 'all' || site.classification === selectedClass;
            return matchesQuery && matchesClass;
        });

        renderTable(filtered);
    }

    searchInput.addEventListener('input', filterData);
    classFilter.addEventListener('change', filterData);
});
</script>
