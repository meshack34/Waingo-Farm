/* =========================================================
   WAINGO FARM — OWNER CATEGORIES
   Categories filtering, search and sorting
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const page = document.querySelector(".categories-page");

    if (!page) {
        return;
    }


    /* =====================================================
       ELEMENTS
       ===================================================== */

    const searchInput = document.getElementById("categorySearch");

    const clearSearchButton =
        document.getElementById("clearCategorySearch");

    const statusFilter =
        document.getElementById("categoryStatusFilter");

    const sortSelect =
        document.getElementById("categorySort");

    const resetButton =
        document.getElementById("resetCategoryFilters");

    const grid =
        document.getElementById("categoriesGrid");

    const noResults =
        document.getElementById("categoriesNoResults");


    if (!grid) {
        return;
    }


    /* =====================================================
       CATEGORY CARDS
       ===================================================== */

    let cards = Array.from(
        grid.querySelectorAll(".category-card")
    );


    /* =====================================================
       SEARCH STATE
       ===================================================== */

    function updateSearchState() {

        if (!searchInput) {
            return;
        }

        const searchWrapper =
            searchInput.closest(".category-search");

        if (!searchWrapper) {
            return;
        }

        if (searchInput.value.trim() !== "") {
            searchWrapper.classList.add("has-value");
        } else {
            searchWrapper.classList.remove("has-value");
        }
    }


    /* =====================================================
       NORMALIZE TEXT
       ===================================================== */

    function normalize(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }


    /* =====================================================
       GET CARD DATA
       ===================================================== */

    function getCardName(card) {
        return normalize(
            card.dataset.name
        );
    }


    function getCardProductCount(card) {

        const count =
            Number(card.dataset.productCount);

        return Number.isNaN(count)
            ? 0
            : count;
    }


    function getCardStatus(card) {

        return normalize(
            card.dataset.status
        );
    }


    /* =====================================================
       SORT CARDS
       ===================================================== */

    function sortCards() {

        if (!sortSelect) {
            return;
        }

        const sortValue =
            sortSelect.value;

        const sortedCards =
            [...cards];

        sortedCards.sort((a, b) => {

            const nameA =
                getCardName(a);

            const nameB =
                getCardName(b);

            const productsA =
                getCardProductCount(a);

            const productsB =
                getCardProductCount(b);


            switch (sortValue) {

                case "name-desc":

                    return nameB.localeCompare(
                        nameA
                    );


                case "products-desc":

                    return productsB - productsA;


                case "products-asc":

                    return productsA - productsB;


                case "name-asc":
                default:

                    return nameA.localeCompare(
                        nameB
                    );
            }

        });


        sortedCards.forEach(card => {
            grid.appendChild(card);
        });


        cards =
            Array.from(
                grid.querySelectorAll(".category-card")
            );
    }


    /* =====================================================
       FILTER CATEGORIES
       ===================================================== */

    function filterCategories() {

        const searchTerm =
            searchInput
                ? normalize(searchInput.value)
                : "";

        const selectedStatus =
            statusFilter
                ? normalize(statusFilter.value)
                : "all";


        let visibleCount = 0;


        cards.forEach(card => {

            const name =
                getCardName(card);

            const status =
                getCardStatus(card);


            /* ---------------------------------------------
               SEARCH
               --------------------------------------------- */

            const matchesSearch =
                searchTerm === "" ||
                name.includes(searchTerm);


            /* ---------------------------------------------
               STATUS
               --------------------------------------------- */

            const matchesStatus =
                selectedStatus === "all" ||
                status === selectedStatus;


            /* ---------------------------------------------
               FINAL RESULT
               --------------------------------------------- */

            const visible =
                matchesSearch &&
                matchesStatus;


            if (visible) {

                card.classList.remove(
                    "category-hidden"
                );

                visibleCount++;

                /*
                 * Highlight matching cards when a search
                 * is being used.
                 */
                if (searchTerm !== "") {
                    card.classList.add(
                        "search-match"
                    );
                } else {
                    card.classList.remove(
                        "search-match"
                    );
                }

            } else {

                card.classList.add(
                    "category-hidden"
                );

                card.classList.remove(
                    "search-match"
                );
            }

        });


        /* =================================================
           SHOW / HIDE NO RESULTS
           ================================================= */

        if (visibleCount === 0) {

            grid.classList.add(
                "no-visible-categories"
            );

            if (noResults) {
                noResults.hidden = false;
            }

        } else {

            grid.classList.remove(
                "no-visible-categories"
            );

            if (noResults) {
                noResults.hidden = true;
            }

        }


        updateSearchState();
    }


    /* =====================================================
       APPLY ALL FILTERS
       ===================================================== */

    function refreshCategories() {

        page.classList.add(
            "is-loading"
        );


        /*
         * Sorting is performed first so the visible cards
         * remain in the selected order.
         */

        sortCards();

        filterCategories();


        /*
         * Remove loading state after the browser has had
         * time to update the DOM.
         */

        window.requestAnimationFrame(() => {

            page.classList.remove(
                "is-loading"
            );

        });
    }


    /* =====================================================
       SEARCH INPUT
       ===================================================== */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            () => {

                filterCategories();

            }
        );

    }


    /* =====================================================
       CLEAR SEARCH
       ===================================================== */

    if (clearSearchButton) {

        clearSearchButton.addEventListener(
            "click",
            () => {

                if (searchInput) {

                    searchInput.value = "";

                    searchInput.focus();

                }

                filterCategories();

            }
        );

    }


    /* =====================================================
       STATUS FILTER
       ===================================================== */

    if (statusFilter) {

        statusFilter.addEventListener(
            "change",
            () => {

                filterCategories();

            }
        );

    }


    /* =====================================================
       SORT
       ===================================================== */

    if (sortSelect) {

        sortSelect.addEventListener(
            "change",
            () => {

                refreshCategories();

            }
        );

    }


    /* =====================================================
       RESET FILTERS
       ===================================================== */

    if (resetButton) {

        resetButton.addEventListener(
            "click",
            () => {

                if (searchInput) {
                    searchInput.value = "";
                }

                if (statusFilter) {
                    statusFilter.value = "all";
                }

                if (sortSelect) {
                    sortSelect.value = "name-asc";
                }

                refreshCategories();

            }
        );

    }


    /* =====================================================
       ESCAPE KEY
       ===================================================== */

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Escape" &&
                    searchInput.value !== ""
                ) {

                    searchInput.value = "";

                    filterCategories();

                }

            }
        );

    }


    /* =====================================================
       INITIAL STATE
       ===================================================== */

    updateSearchState();

    sortCards();

    filterCategories();

});