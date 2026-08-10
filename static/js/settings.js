/* =========================================================
   WAINGO FARM — OWNER SETTINGS
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initSettingsPage();
});


function initSettingsPage() {
    initSettingsCards();
    initKeyboardNavigation();
}


/* =========================================================
   CARD INTERACTIONS
   ========================================================= */

function initSettingsCards() {
    const cards = document.querySelectorAll(".settings-card");

    cards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            card.classList.add("settings-card-active");
        });

        card.addEventListener("mouseleave", () => {
            card.classList.remove("settings-card-active");
        });
    });
}


/* =========================================================
   KEYBOARD SUPPORT
   ========================================================= */

function initKeyboardNavigation() {
    const items = document.querySelectorAll(
        ".settings-page .settings-item, " +
        ".settings-page .security-btn"
    );

    items.forEach((item) => {
        item.addEventListener("keydown", (event) => {

            if (
                event.key === "Enter" ||
                event.key === " "
            ) {
                event.preventDefault();

                item.click();
            }

        });
    });
}