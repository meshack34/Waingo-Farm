document.addEventListener("DOMContentLoaded", function () {

               /* ============================================================
                  SERVICES PAGE
               ============================================================ */

               const servicesPage = document.querySelector(".services-page");

               if (!servicesPage) {
                              return;
               }


               /* ============================================================
                  SCROLL REVEAL
               ============================================================ */

               const revealElements = document.querySelectorAll(
                              ".service-card, " +
                              ".benefit-item, " +
                              ".process-item, " +
                              ".services-intro-content, " +
                              ".services-intro-visual, " +
                              ".why-waingo-image, " +
                              ".why-waingo-content"
               );


               revealElements.forEach(function (element) {

                              element.classList.add("reveal-service");

               });


               if ("IntersectionObserver" in window) {

                              const revealObserver = new IntersectionObserver(
                                             function (entries, observer) {

                                                            entries.forEach(function (entry) {

                                                                           if (!entry.isIntersecting) {
                                                                                          return;
                                                                           }

                                                                           entry.target.classList.add("is-visible");

                                                                           observer.unobserve(entry.target);

                                                            });

                                             },
                                             {
                                                            threshold: 0.12,
                                                            rootMargin: "0px 0px -40px 0px"
                                             }
                              );


                              revealElements.forEach(function (element) {

                                             revealObserver.observe(element);

                              });

               } else {

                              revealElements.forEach(function (element) {

                                             element.classList.add("is-visible");

                              });

               }


               /* ============================================================
                  SERVICE CARD STAGGER
               ============================================================ */

               const serviceCards = document.querySelectorAll(
                              ".services-grid .service-card"
               );

               serviceCards.forEach(function (card, index) {

                              card.style.transitionDelay =
                                             (index * 60) + "ms";

               });


               /* ============================================================
                  BENEFIT STAGGER
               ============================================================ */

               const benefits = document.querySelectorAll(
                              ".benefit-item"
               );

               benefits.forEach(function (item, index) {

                              item.style.transitionDelay =
                                             (index * 80) + "ms";

               });


               /* ============================================================
                  PROCESS STAGGER
               ============================================================ */

               const processItems = document.querySelectorAll(
                              ".process-item"
               );

               processItems.forEach(function (item, index) {

                              item.style.transitionDelay =
                                             (index * 100) + "ms";

               });


               /* ============================================================
                  SMOOTH INTERNAL ANCHOR SCROLL
               ============================================================ */

               const internalLinks = servicesPage.querySelectorAll(
                              'a[href^="#"]'
               );

               internalLinks.forEach(function (link) {

                              link.addEventListener("click", function (event) {

                                             const targetId =
                                                            this.getAttribute("href");

                                             if (!targetId || targetId === "#") {
                                                            return;
                                             }

                                             const target =
                                                            document.querySelector(targetId);

                                             if (!target) {
                                                            return;
                                             }

                                             event.preventDefault();

                                             target.scrollIntoView({
                                                            behavior: "smooth",
                                                            block: "start"
                                             });

                              });

               });


               /* ============================================================
                  SERVICE CARD KEYBOARD ACCESS
               ============================================================ */

               serviceCards.forEach(function (card) {

                              card.addEventListener("mouseenter", function () {

                                             this.classList.add("service-card-hover");

                              });

                              card.addEventListener("mouseleave", function () {

                                             this.classList.remove("service-card-hover");

                              });

               });


               /* ============================================================
                  CTA VISIBILITY
               ============================================================ */

               const ctaSection =
                              document.querySelector(".services-cta");

               if (ctaSection && "IntersectionObserver" in window) {

                              const ctaObserver = new IntersectionObserver(
                                             function (entries, observer) {

                                                            entries.forEach(function (entry) {

                                                                           if (!entry.isIntersecting) {
                                                                                          return;
                                                                           }

                                                                           ctaSection.classList.add(
                                                                                          "services-cta-visible"
                                                                           );

                                                                           observer.unobserve(ctaSection);

                                                            });

                                             },
                                             {
                                                            threshold: 0.2
                                             }
                              );

                              ctaObserver.observe(ctaSection);

               }


               /* ============================================================
                  REDUCED MOTION
               ============================================================ */

               const prefersReducedMotion =
                              window.matchMedia &&
                              window.matchMedia(
                                             "(prefers-reduced-motion: reduce)"
                              ).matches;


               if (prefersReducedMotion) {

                              revealElements.forEach(function (element) {

                                             element.classList.add("is-visible");

                                             element.style.transitionDelay = "0ms";

                              });

               }

});