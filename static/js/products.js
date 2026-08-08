/*
=========================================================
WAINGO FARM
PRODUCTS.JS
=========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeSearch();

    initializeFilters();

    animateCards();

});


/*=========================================================
SEARCH
=========================================================*/

function initializeSearch(){

    const searchInput = document.querySelector(".toolbar-search input");

    const cards = document.querySelectorAll(".product-card");

    if(!searchInput) return;

    searchInput.addEventListener("keyup", function(){

        const value = this.value.toLowerCase();

        cards.forEach(card=>{

            const title = card.querySelector("h3").textContent.toLowerCase();

            const category = card.querySelector(".product-category").textContent.toLowerCase();

            if(

                title.includes(value) ||

                category.includes(value)

            ){

                card.style.display="flex";

            }

            else{

                card.style.display="none";

            }

        });

    });

}



/*=========================================================
FILTERS
=========================================================*/

function initializeFilters(){

    const selects=document.querySelectorAll(".products-toolbar select");

    const cards=document.querySelectorAll(".product-card");

    if(selects.length===0) return;

    const categorySelect=selects[0];

    const statusSelect=selects[1];

    const sortSelect=selects[2];



    categorySelect.addEventListener("change", filterProducts);

    statusSelect.addEventListener("change", filterProducts);

    sortSelect.addEventListener("change", sortProducts);



    function filterProducts(){

        const category=categorySelect.value.toLowerCase();

        const status=statusSelect.value.toLowerCase();

        cards.forEach(card=>{

            let show=true;

            if(category!=="all categories"){

                const productCategory=

                    card.querySelector(".product-category")

                    .textContent

                    .trim()

                    .toLowerCase();

                if(productCategory!==category){

                    show=false;

                }

            }

            if(status!=="availability"){

                const badge=

                    card.querySelector(".stock-badge")

                    .textContent

                    .toLowerCase();

                if(status==="available"){

                    if(badge.includes("out")){

                        show=false;

                    }

                }

                if(status==="unavailable"){

                    if(!badge.includes("out")){

                        show=false;

                    }

                }

            }

            card.style.display=show?"flex":"none";

        });

    }



    function sortProducts(){

        const grid=document.querySelector(".products-grid");

        const cardsArray=[...cards];

        switch(sortSelect.value){

            case "Name":

                cardsArray.sort((a,b)=>{

                    return a.querySelector("h3").innerText

                    .localeCompare(

                        b.querySelector("h3").innerText

                    );

                });

                break;

            case "Price ↑":

                cardsArray.sort((a,b)=>{

                    return getPrice(a)-getPrice(b);

                });

                break;

            case "Price ↓":

                cardsArray.sort((a,b)=>{

                    return getPrice(b)-getPrice(a);

                });

                break;

            default:

                return;

        }

        cardsArray.forEach(card=>grid.appendChild(card));

    }

}



/*=========================================================
PRICE
=========================================================*/

function getPrice(card){

    return parseFloat(

        card.querySelector(".product-price")

        .innerText

        .replace("KSh","")

        .replace(/,/g,"")

        .trim()

    );

}



/*=========================================================
ANIMATION
=========================================================*/

function animateCards(){

    const cards=document.querySelectorAll(".product-card");

    cards.forEach((card,index)=>{

        card.style.opacity="0";

        card.style.transform="translateY(20px)";

        setTimeout(()=>{

            card.style.transition=".45s";

            card.style.opacity="1";

            card.style.transform="translateY(0)";

        },index*80);

    });

}



/*=========================================================
READY FOR AJAX
=========================================================*/

function reloadProducts(){

    // Future:
    // Fetch products using AJAX
    // Update cards without refreshing page.

}