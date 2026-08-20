/**
 * mars_globe.js
 * Interactive 3D WebGL Mars Globe with Crustal Magnetic Field Heatmap Overlay
 * Built with Three.js
 */

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('globe-container');
    const tooltip = document.getElementById('globe-tooltip');
    const toggleMagnetic = document.getElementById('toggle-magnetic');
    const toggleRotation = document.getElementById('toggle-rotation');
    const togglePins = document.getElementById('toggle-pins');
    const opacitySlider = document.getElementById('opacity-slider');

    if (!container) return;

    // Dimensions
    let width = container.clientWidth;
    let height = container.clientHeight;

    // Three.js Scene Setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x06080e);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 1.2, 3.8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // OrbitControls
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 2.0;
    controls.maxDistance = 7.0;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.8;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffeedd, 1.2);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);

    // Globe Group
    const globeGroup = new THREE.Group();
    scene.add(globeGroup);

    // 1. Procedural Base Mars Texture Canvas
    function createMarsBaseTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 2048;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Mars rust-orange gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
        gradient.addColorStop(0, '#d17a58');    // North Polar region
        gradient.addColorStop(0.3, '#c1440e');  // Northern Lowlands
        gradient.addColorStop(0.5, '#993d15');  // Dichotomy / Equator
        gradient.addColorStop(0.8, '#7e2d08');  // Southern cratered highlands
        gradient.addColorStop(1.0, '#df8968');  // South Polar Cap

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Add procedural Martian craters and albedo features
        for (let i = 0; i < 400; i++) {
            const x = Math.random() * canvas.width;
            const y = (Math.random() * 0.7 + 0.2) * canvas.height;
            const radius = Math.random() * 30 + 5;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = (Math.random() > 0.5) ? 'rgba(60, 20, 5, 0.25)' : 'rgba(230, 160, 120, 0.2)';
            ctx.fill();
        }

        // Polar ice caps
        ctx.fillStyle = 'rgba(245, 245, 255, 0.9)';
        ctx.beginPath();
        ctx.ellipse(canvas.width / 2, 25, 220, 25, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.ellipse(canvas.width / 2, canvas.height - 25, 200, 25, 0, 0, Math.PI * 2);
        ctx.fill();

        return new THREE.CanvasTexture(canvas);
    }

    // Mars Base Sphere
    const sphereRadius = 1.2;
    const geometry = new THREE.SphereGeometry(sphereRadius, 64, 64);
    const marsMaterial = new THREE.MeshStandardMaterial({
        map: createMarsBaseTexture(),
        roughness: 0.85,
        metalness: 0.1
    });
    const marsMesh = new THREE.Mesh(geometry, marsMaterial);
    globeGroup.add(marsMesh);

    // 2. Magnetic Heatmap Overlay Sphere
    const textureLoader = new THREE.TextureLoader();
    let magneticMesh = null;

    // Construct path to texture
    const currentPath = window.location.pathname;
    const basePath = currentPath.includes('/mars-magnetic-biology') ? '/mars-magnetic-biology' : '';
    const textureUrl = `${basePath}/assets/img/mars_mag_texture.png`;

    textureLoader.load(textureUrl, (texture) => {
        const magMaterial = new THREE.MeshBasicMaterial({
            map: texture,
            transparent: true,
            opacity: 0.75,
            depthWrite: false
        });
        const magGeometry = new THREE.SphereGeometry(sphereRadius * 1.002, 64, 64);
        magneticMesh = new THREE.Mesh(magGeometry, magMaterial);
        globeGroup.add(magneticMesh);
    }, undefined, (err) => {
        console.warn("Could not load magnetic texture, using fallback overlay.", err);
    });

    // 3. Coordinate Conversion
    function latLonToVector3(lat, lon, radius) {
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = lon * (Math.PI / 180);

        const x = -(radius * Math.sin(phi) * Math.cos(theta));
        const z = (radius * Math.sin(phi) * Math.sin(theta));
        const y = (radius * Math.cos(phi));

        return new THREE.Vector3(x, y, z);
    }

    // 4. Landing Site Markers
    const pinGroup = new THREE.Group();
    globeGroup.add(pinGroup);
    const pinMeshes = [];

    // Load Data JSON
    const dataUrl = `${basePath}/assets/js/mag_field_data.json`;

    fetch(dataUrl)
        .then(res => res.json())
        .then(data => {
            const sites = data.landing_sites || [];
            
            sites.forEach(site => {
                const pos = latLonToVector3(site.lat, site.lon, sphereRadius * 1.015);
                
                // Color coding
                let pinColor = 0x0ea5e9; // Blue: Low field
                if (site.classification === 'high-field') {
                    pinColor = 0xef4444; // Red: High field
                } else if (site.classification === 'moderate') {
                    pinColor = 0xf59e0b; // Orange: Moderate field
                }

                // Marker Pin Head
                const pinGeo = new THREE.SphereGeometry(0.024, 16, 16);
                const pinMat = new THREE.MeshStandardMaterial({
                    color: pinColor,
                    emissive: pinColor,
                    emissiveIntensity: 0.4,
                    roughness: 0.2
                });
                const pinMesh = new THREE.Mesh(pinGeo, pinMat);
                pinMesh.position.copy(pos);
                pinMesh.userData = site;

                // Marker Stem
                const basePos = latLonToVector3(site.lat, site.lon, sphereRadius);
                const stemGeo = new THREE.BufferGeometry().setFromPoints([basePos, pos]);
                const stemMat = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
                const stemLine = new THREE.Line(stemGeo, stemMat);

                pinGroup.add(pinMesh);
                pinGroup.add(stemLine);
                pinMeshes.push(pinMesh);
            });
        })
        .catch(err => {
            console.error("Error loading landing site JSON:", err);
        });

    // 5. Raycasting for Tooltip Interactivity
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function onPointerMove(event) {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(pinMeshes);

        if (intersects.length > 0) {
            const site = intersects[0].object.userData;
            const badgeClass = site.classification === 'high-field' ? 'badge-high' : 
                              (site.classification === 'moderate' ? 'badge-moderate' : 'badge-low');

            tooltip.innerHTML = `
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: #f87171;">${site.name}</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 6px;">${site.mission}</div>
                <div style="margin-bottom: 4px;"><strong>Coords:</strong> ${site.lat.toFixed(2)}°N, ${site.lon.toFixed(2)}°E</div>
                <div style="margin-bottom: 4px;"><strong>Orbital |B| (400km):</strong> ${site.Bmag_400km.toFixed(1)} nT</div>
                <div style="margin-bottom: 4px;"><strong>Surface |B| Est:</strong> <span style="color: #fbbf24; font-weight: 700;">${site.B_surface_est.toFixed(0)} nT</span></div>
                <div style="margin-top: 6px;"><span class="badge ${badgeClass}">${site.classification}</span></div>
            `;
            tooltip.style.display = 'block';
            tooltip.style.left = `${event.clientX - rect.left + 15}px`;
            tooltip.style.top = `${event.clientY - rect.top + 15}px`;
            container.style.cursor = 'pointer';
        } else {
            tooltip.style.display = 'none';
            container.style.cursor = 'default';
        }
    }

    container.addEventListener('mousemove', onPointerMove);

    // 6. UI Controls Event Listeners
    if (toggleMagnetic) {
        toggleMagnetic.addEventListener('change', (e) => {
            if (magneticMesh) magneticMesh.visible = e.target.checked;
        });
    }

    if (toggleRotation) {
        toggleRotation.addEventListener('change', (e) => {
            controls.autoRotate = e.target.checked;
        });
    }

    if (togglePins) {
        togglePins.addEventListener('change', (e) => {
            pinGroup.visible = e.target.checked;
        });
    }

    if (opacitySlider) {
        opacitySlider.addEventListener('input', (e) => {
            if (magneticMesh) {
                magneticMesh.material.opacity = parseFloat(e.target.value);
            }
        });
    }

    // 7. Window Resize Handling
    window.addEventListener('resize', () => {
        width = container.clientWidth;
        height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    // 8. Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
});
