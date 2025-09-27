// static/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // --- THEME SWITCH LOGIC ---
    const themeToggle = document.getElementById('checkbox');
    if (themeToggle) {
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme) {
            document.body.classList.add(currentTheme);
            if (currentTheme === 'light-mode') {
                themeToggle.checked = true;
            }
        }
        themeToggle.addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.add('light-mode');
                localStorage.setItem('theme', 'light-mode');
            } else {
                document.body.classList.remove('light-mode');
                localStorage.setItem('theme', 'dark');
            }
        });
    }

    // --- TYPED.JS ANIMATION (CORRECTED) ---
    // Only run the typing animation if the element exists on the page
    const typedElement = document.getElementById('typed-text');
    if (typedElement) {
        new Typed('#typed-text', {
            strings: ["Programmer.", "Developer."],
            typeSpeed: 70,
            backSpeed: 30,
            loop: true,
            smartBackspace: true,
        });
    }

    // --- PARTICLES.JS INITIALIZATION ---
    // This will now run correctly on all pages
    particlesJS("particles-js", {
        "particles": {
            "number": { "value": 60, "density": { "enable": true, "value_area": 800 } },
            "color": { "value": "#a0a0a0" },
            "shape": { "type": "circle" },
            "opacity": { "value": 0.5, "random": false },
            "size": { "value": 2, "random": true },
            "line_linked": { "enable": true, "distance": 150, "color": "#a0a0a0", "opacity": 0.4, "width": 1 },
            "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": { "onhover": { "enable": true, "mode": "grab" }, "onclick": { "enable": true, "mode": "push" }, "resize": true },
            "modes": { "grab": { "distance": 140, "line_linked": { "opacity": 1 } }, "push": { "particles_nb": 4 } }
        },
        "retina_detect": true
    });

    // --- SCROLL REVEAL (Intersection Observer) ---
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.1 });
    revealElements.forEach(el => observer.observe(el));
});