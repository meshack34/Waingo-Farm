/*
=========================================================
WAINGO FARM OWNER PORTAL
owner.js
=========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeSidebar();

    initializeActiveLinks();

    initializeTooltips();

});



/*=========================================================
SIDEBAR
=========================================================*/

function initializeSidebar() {

    const sidebar = document.querySelector(".owner-sidebar");

    const toggle = document.querySelector(".sidebar-toggle");

    if (!sidebar || !toggle) return;

    toggle.addEventListener("click", () => {

        sidebar.classList.toggle("show");

    });

}



/*=========================================================
ACTIVE MENU
=========================================================*/

function initializeActiveLinks() {

    const current = window.location.pathname;

    const links = document.querySelectorAll(".sidebar-menu a");

    links.forEach(link => {

        link.classList.remove("active");

        if (link.getAttribute("href") === current) {

            link.classList.add("active");

        }

    });

}



/*=========================================================
TOOLTIPS
=========================================================*/

function initializeTooltips() {

    const elements = document.querySelectorAll("[data-tooltip]");

    elements.forEach(element => {

        element.addEventListener("mouseenter", () => {

            const tooltip = document.createElement("span");

            tooltip.className = "owner-tooltip";

            tooltip.innerText = element.dataset.tooltip;

            document.body.appendChild(tooltip);

            const rect = element.getBoundingClientRect();

            tooltip.style.left = rect.left + rect.width / 2 + "px";

            tooltip.style.top = rect.top - 42 + "px";

            element.tooltip = tooltip;

        });

        element.addEventListener("mouseleave", () => {

            if (element.tooltip) {

                element.tooltip.remove();

            }

        });

    });

}



/*=========================================================
UTILITIES
=========================================================*/

function showMessage(message) {

    console.log(message);

}