/* =========================================================
   WAINGO FARM — OWNER PROFILE
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initProfileInteractions();
});


function initProfileInteractions() {
    /*
     * Profile page currently uses normal Django links/forms.
     * This JS intentionally stays lightweight so it does not
     * interfere with Django's authentication or form handling.
     */

    initCardEffects();
    initStatusAnimation();
    initKeyboardSupport();
}


/* =========================================================
   CARD INTERACTIONS
   ========================================================= */

function initCardEffects() {
    const cards = document.querySelectorAll(".profile-card");

    if (!cards.length) {
        return;
    }

    cards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            card.classList.add("profile-card-active");
        });

        card.addEventListener("mouseleave", () => {
            card.classList.remove("profile-card-active");
        });
    });
}


/* =========================================================
   ACCOUNT STATUS
   ========================================================= */

function initStatusAnimation() {
    const statusDot = document.querySelector(".status-dot");

    if (!statusDot) {
        return;
    }

    /*
     * Small visual pulse to make the active account status
     * feel alive without being distracting.
     */

    statusDot.animate(
        [
            {
                opacity: 1,
                transform: "scale(1)"
            },
            {
                opacity: 0.65,
                transform: "scale(0.88)"
            },
            {
                opacity: 1,
                transform: "scale(1)"
            }
        ],
        {
            duration: 2200,
            iterations: Infinity,
            easing: "ease-in-out"
        }
    );
}


/* =========================================================
   KEYBOARD SUPPORT
   ========================================================= */

function initKeyboardSupport() {
    const actionLinks = document.querySelectorAll(
        ".profile-page .btn-owner, " +
        ".profile-page .security-action"
    );

    actionLinks.forEach((link) => {
        link.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                link.click();
            }
        });
    });
}