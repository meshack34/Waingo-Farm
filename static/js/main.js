document.addEventListener("DOMContentLoaded", function () {

    /*
    =========================================================
    MOBILE NAVIGATION
    =========================================================
    */

    const mobileMenuButton =
        document.getElementById("mobileMenuButton");

    const navMenu =
        document.getElementById("navMenu");


    if (mobileMenuButton && navMenu) {

        mobileMenuButton.addEventListener("click", function () {

            navMenu.classList.toggle("show");

            const isOpen =
                navMenu.classList.contains("show");

            mobileMenuButton.setAttribute(
                "aria-expanded",
                isOpen
            );


            /*
            Change hamburger icon
            */

            const icon =
                mobileMenuButton.querySelector("i");

            if (icon) {

                if (isOpen) {

                    icon.classList.remove("bi-list");

                    icon.classList.add("bi-x-lg");

                } else {

                    icon.classList.remove("bi-x-lg");

                    icon.classList.add("bi-list");

                }

            }

        });

    }


    /*
    =========================================================
    PRODUCT CATEGORY DROPDOWN
    =========================================================
    */

    const categoriesButton =
        document.getElementById("categoriesButton");

    const categoryDropdown =
        document.getElementById("categoryDropdown");


    if (categoriesButton && categoryDropdown) {

        categoriesButton.addEventListener(
            "click",
            function () {

                categoryDropdown.classList.toggle("show");

                categoriesButton.classList.toggle("open");

            }
        );

    }


    /*
    =========================================================
    CLOSE MOBILE MENU WHEN LINK IS CLICKED
    =========================================================
    */

    const navLinks =
        document.querySelectorAll(".nav-link");


    navLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 850) {

                navMenu.classList.remove("show");

                mobileMenuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );


                const icon =
                    mobileMenuButton.querySelector("i");


                if (icon) {

                    icon.classList.remove("bi-x-lg");

                    icon.classList.add("bi-list");

                }

            }

        });

    });


    /*
    =========================================================
    WINDOW RESIZE
    =========================================================
    */

    window.addEventListener("resize", function () {

        if (window.innerWidth > 850) {

            navMenu.classList.remove("show");

            if (mobileMenuButton) {

                mobileMenuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );

                const icon =
                    mobileMenuButton.querySelector("i");

                if (icon) {

                    icon.classList.remove("bi-x-lg");

                    icon.classList.add("bi-list");

                }

            }

        }

    });

});