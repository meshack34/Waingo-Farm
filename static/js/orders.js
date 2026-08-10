document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       ELEMENTS
       ========================================================= */

    const searchInput =
        document.getElementById("orderSearch");

    const statusFilter =
        document.getElementById("statusFilter");

    const countyFilter =
        document.getElementById("countyFilter");

    const cards =
        document.querySelectorAll(".order-card");


    /* =========================================================
       FILTER ORDERS
       ========================================================= */

    function filterOrders() {

        const search =
            searchInput
                ? searchInput.value
                    .toLowerCase()
                    .trim()
                : "";


        const selectedStatus =
            statusFilter
                ? statusFilter.value
                    .toLowerCase()
                    .trim()
                : "all";


        const selectedCounty =
            countyFilter
                ? countyFilter.value
                    .toLowerCase()
                    .trim()
                : "all";


        /* =====================================================
           LOOP THROUGH ORDER CARDS
           ===================================================== */

        cards.forEach(function (card) {

            /* -------------------------------------------------
               DATA FROM CARD
               ------------------------------------------------- */

            const cardStatus =
                (card.dataset.status || "")
                    .toLowerCase()
                    .trim();


            const cardCounty =
                (card.dataset.county || "")
                    .toLowerCase()
                    .trim();


            /* -------------------------------------------------
               CUSTOMER
               ------------------------------------------------- */

            const customerElement =
                card.querySelector(
                    ".customer-info strong"
                );


            const customer =
                customerElement
                    ? customerElement.textContent
                        .toLowerCase()
                        .trim()
                    : "";


            /* -------------------------------------------------
               PHONE
               ------------------------------------------------- */

            const phoneElement =
                card.querySelector(
                    ".customer-info small"
                );


            const phone =
                phoneElement
                    ? phoneElement.textContent
                        .toLowerCase()
                        .trim()
                    : "";


            /* -------------------------------------------------
               ORDER ID
               ------------------------------------------------- */

            const orderIdElement =
                card.querySelector(
                    ".order-top h4"
                );


            const orderId =
                orderIdElement
                    ? orderIdElement.textContent
                        .toLowerCase()
                        .trim()
                    : "";


            /* -------------------------------------------------
               MPESA RECEIPT
               ------------------------------------------------- */

            const receiptElement =
                card.querySelector(
                    ".receipt-box strong"
                );


            const receipt =
                receiptElement
                    ? receiptElement.textContent
                        .toLowerCase()
                        .trim()
                    : "";


            /* =================================================
               SEARCH MATCH
               ================================================= */

            const matchesSearch =
                search === "" ||

                customer.includes(search) ||

                phone.includes(search) ||

                orderId.includes(search) ||

                receipt.includes(search);


            /* =================================================
               STATUS MATCH
               ================================================= */

            const matchesStatus =
                selectedStatus === "all" ||

                selectedStatus === cardStatus;


            /* =================================================
               COUNTY MATCH
               ================================================= */

            const matchesCounty =
                selectedCounty === "all" ||

                selectedCounty === cardCounty;


            /* =================================================
               FINAL MATCH
               ================================================= */

            const shouldShow =
                matchesSearch &&
                matchesStatus &&
                matchesCounty;


            /* =================================================
               SHOW / HIDE
               ================================================= */

            if (shouldShow) {

                card.style.display = "";

            } else {

                card.style.display = "none";

            }

        });

    }


    /* =========================================================
       SEARCH
       ========================================================= */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            filterOrders
        );

    }


    /* =========================================================
       STATUS FILTER
       ========================================================= */

    if (statusFilter) {

        statusFilter.addEventListener(
            "change",
            filterOrders
        );

    }


    /* =========================================================
       COUNTY FILTER
       ========================================================= */

    if (countyFilter) {

        countyFilter.addEventListener(
            "change",
            filterOrders
        );

    }


    /* =========================================================
       INITIAL FILTER
       ========================================================= */

    filterOrders();

});