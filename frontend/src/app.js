// ----------------------
// Header & Scroll Logic
// ----------------------
window.addEventListener('scroll', () => {
    const header = document.querySelector('.main-header');

    if (window.scrollY > 20) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// -----------------
// Navigation Logic
// -----------------
document.querySelectorAll(".nav-link, .header-logo").forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault();
        const page = link.dataset.page;

        if (page === "logo" || page === "home") {
            window.location.href = "/";
            return;
        }

        if (page === "learn") {
            window.location.href = "/learn";
            return;
        }

        if (page === "practice") {
            window.location.href = "/practice";
            return;
        }
    });
});

document.querySelectorAll(".learn-card button").forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        const page = btn.dataset.page;

        if (page === "practice") {
            window.location.href = "/practice";
        }

        if (page === "file-analysis") {
            window.location.href = "/learn/file-analysis"
        }

        if (page === "metadata") {
            window.location.href = "/learn/metadata-investigation";
        }

        if (page === "footprint") {
            window.location.href = "/learn/digital-footprint";
        }
    });
});

// --------------------------------------------
// Start Practice btn (Digital Forensics Only)
// --------------------------------------------
document.querySelectorAll(".card a").forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        window.location.href = "/learn";
    });
});

function scrollToSection(selector) {
    const section = document.querySelector(selector);
    if (section) {
        section.scrollIntoView({ behavior: "smooth" });
    }
}

// -------------------------------------
// Fade-In & Animation Load
// -------------------------------------
window.addEventListener("load", () => {
    const initializeAndAnimation = (selector) => {
        const element = document.querySelector(selector);

        if (element) {
            element.style.opacity = 0;
            element.style.transform = "translateY(40px)";

            setTimeout(() => {
                element.style.transition = "1.5s ease";
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }, 150);
        }
    };

    const fadeInAnimation = (selector) => {
        const fadeInElements = document.querySelector(selector);

        if (fadeInElements) {
            fadeInElements.style.opacity = "0";
            fadeInElements.style.transform = "scale(0.9)";

            setTimeout(() => {
                fadeInElements.style.opacity = "1";
                fadeInElements.style.transition = "1s ease";
                fadeInElements.style.transform = "scale(1)";
            }, 150);
        }
    };

    initializeAndAnimation(".landing-container");
    initializeAndAnimation(".card-section");
    
    fadeInAnimation(".container.content")
});