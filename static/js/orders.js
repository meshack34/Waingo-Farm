document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.querySelector(".toolbar-search input");

    const statusFilter = document.querySelectorAll(".orders-toolbar select")[0];

    const countyFilter = document.querySelectorAll(".orders-toolbar select")[1];

    const cards = document.querySelectorAll(".order-card");



    function filterOrders() {

        const search = searchInput.value.toLowerCase().trim();

        const status = statusFilter.value.toLowerCase();

        const county = countyFilter.value.toLowerCase();



        cards.forEach(card => {

            const customer = card.querySelector(".customer-info strong").textContent.toLowerCase();

            const phone = card.querySelector(".customer-info small").textContent.toLowerCase();

            const orderId = card.querySelector(".order-top h4").textContent.toLowerCase();

            const receiptBox = card.querySelector(".receipt-box strong");

            const receipt = receiptBox ? receiptBox.textContent.toLowerCase() : "";

            const cardStatus = card.querySelector(".status").textContent.toLowerCase();

            const cardCounty = card.querySelector(".order-details div strong").textContent.toLowerCase();



            const matchSearch =

                customer.includes(search) ||

                phone.includes(search) ||

                orderId.includes(search) ||

                receipt.includes(search);



            const matchStatus =

                status === "all status" ||

                status === cardStatus;



            const matchCounty =

                county === "all counties" ||

                county === cardCounty;



            if (matchSearch && matchStatus && matchCounty) {

                card.style.display = "";

            } else {

                card.style.display = "none";

            }

        });

    }



    if (searchInput) {

        searchInput.addEventListener("keyup", filterOrders);

    }



    if (statusFilter) {

        statusFilter.addEventListener("change", filterOrders);

    }



    if (countyFilter) {

        countyFilter.addEventListener("change", filterOrders);

    }

});