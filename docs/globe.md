---
layout: default
title: 3D Mars Globe
permalink: /globe/
---

<div class="card">
    <h2>Interactive 3D Mars Magnetic Field Globe</h2>
    <p>Explore the Martian crustal magnetic field in three dimensions. Toggle the crustal magnetic field heatmap overlay to examine the sharp dichotomy between the intensely magnetized southern highlands and demagnetized northern lowlands. Click or hover on any landing site pin to view local magnetic measurements and astrobiological risk profiles.</p>
    
    <div id="globe-container">
        <div class="globe-controls">
            <label>
                <input type="checkbox" id="toggle-magnetic" checked>
                <span>Magnetic Field Heatmap</span>
            </label>
            <label>
                <input type="checkbox" id="toggle-rotation" checked>
                <span>Auto-Rotation</span>
            </label>
            <label>
                <input type="checkbox" id="toggle-pins" checked>
                <span>Landing Site Pins</span>
            </label>
            <div style="margin-top: 6px;">
                <label for="opacity-slider" style="font-size: 0.8rem;">Heatmap Opacity:</label>
                <input type="range" id="opacity-slider" min="0" max="1" step="0.05" value="0.75" style="width: 100%;">
            </div>
        </div>
        <div id="globe-tooltip" class="globe-tooltip"></div>
    </div>
</div>

<div class="card">
    <h3>Landing Site Magnetic Legend</h3>
    <div style="display: flex; gap: 2rem; flex-wrap: wrap; margin-top: 0.8rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: #ef4444; border: 1px solid black;"></span>
            <span><strong>High Field (&gt;1000 nT Surface)</strong>: Terra Sirenum, InSight Ground Truth</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: #f59e0b; border: 1px solid black;"></span>
            <span><strong>Moderate Field (150–1000 nT Surface)</strong>: Spirit / Gusev Crater Margin</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: #0ea5e9; border: 1px solid black;"></span>
            <span><strong>Low/Null-Field (&lt;150 nT Surface)</strong>: Perseverance, Arcadia Planitia, Oxia Planum</span>
        </div>
    </div>
</div>

<!-- Three.js and OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="{{ site.baseurl }}/assets/js/mars_globe.js"></script>
