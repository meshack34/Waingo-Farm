document.addEventListener("DOMContentLoaded", function () {
               /* ============================================================
                  GALLERY FILTER
               ============================================================ */

               const filterButtons = document.querySelectorAll(".gallery-filter-btn");
               const galleryItems = document.querySelectorAll(".gallery-item");

               filterButtons.forEach(function (button) {
                              button.addEventListener("click", function () {
                                             const filter = this.dataset.filter;

                                             /* Remove active state */
                                             filterButtons.forEach(function (btn) {
                                                            btn.classList.remove("active");
                                             });

                                             /* Add active state */
                                             this.classList.add("active");

                                             /* Filter gallery */
                                             galleryItems.forEach(function (item) {
                                                            const category = item.dataset.category;

                                                            if (filter === "all" || category === filter) {
                                                                           item.classList.remove("hidden");

                                                                           setTimeout(function () {
                                                                                          item.classList.add("visible");
                                                                           }, 20);
                                                            } else {
                                                                           item.classList.remove("visible");
                                                                           item.classList.add("hidden");
                                                            }
                                             });
                              });
               });

               /* ============================================================
                  IMAGE LIGHTBOX
               ============================================================ */

               const lightbox = document.getElementById("galleryLightbox");
               const lightboxImage = document.getElementById("lightboxImage");
               const lightboxTitle = document.getElementById("lightboxTitle");
               const lightboxCategory = document.getElementById("lightboxCategory");
               const lightboxClose = document.getElementById("lightboxClose");
               const lightboxPrevious = document.getElementById("lightboxPrevious");
               const lightboxNext = document.getElementById("lightboxNext");

               let currentIndex = 0;
               let visibleItems = [];

               /* ============================================================
                  UPDATE VISIBLE ITEMS
               ============================================================ */

               function updateVisibleItems() {
                              visibleItems = Array.from(galleryItems).filter(function (item) {
                                             return !item.classList.contains("hidden");
                              });
               }

               /* ============================================================
                  GET IMAGE INFORMATION
               ============================================================ */

               function getImageFromItem(item) {
                              if (!item) {
                                             return null;
                              }

                              return item.querySelector("img");
               }

               /* ============================================================
                  UPDATE LIGHTBOX CONTENT
               ============================================================ */

               function updateLightbox() {
                              if (!visibleItems.length) {
                                             return;
                              }

                              const item = visibleItems[currentIndex];

                              if (!item) {
                                             return;
                              }

                              const image = getImageFromItem(item);

                              if (!image) {
                                             return;
                              }

                              const title =
                                             item.dataset.title ||
                                             image.dataset.title ||
                                             image.alt ||
                                             "Gallery Image";

                              const category =
                                             item.dataset.categoryLabel ||
                                             item.dataset.category ||
                                             "Gallery";

                              /* Update image */
                              lightboxImage.src = image.src;
                              lightboxImage.alt = title;

                              /* Update title */
                              if (lightboxTitle) {
                                             lightboxTitle.textContent = title;
                              }

                              /* Update category */
                              if (lightboxCategory) {
                                             lightboxCategory.textContent = category;
                              }

                              /* Disable/enable navigation appropriately */
                              if (visibleItems.length <= 1) {
                                             if (lightboxPrevious) {
                                                            lightboxPrevious.disabled = true;
                                             }

                                             if (lightboxNext) {
                                                            lightboxNext.disabled = true;
                                             }
                              } else {
                                             if (lightboxPrevious) {
                                                            lightboxPrevious.disabled = false;
                                             }

                                             if (lightboxNext) {
                                                            lightboxNext.disabled = false;
                                             }
                              }
               }

               /* ============================================================
                  OPEN LIGHTBOX
               ============================================================ */

               function openLightbox(item) {
                              updateVisibleItems();

                              currentIndex = visibleItems.indexOf(item);

                              if (currentIndex === -1) {
                                             currentIndex = 0;
                              }

                              updateLightbox();

                              if (!lightbox) {
                                             return;
                              }

                              lightbox.classList.add("active");

                              /* Prevent background page scrolling */
                              document.body.classList.add("lightbox-open");

                              /* Accessibility */
                              lightbox.setAttribute("aria-hidden", "false");

                              /* Focus close button */
                              if (lightboxClose) {
                                             setTimeout(function () {
                                                            lightboxClose.focus();
                                             }, 50);
                              }
               }

               /* ============================================================
                  CLOSE LIGHTBOX
               ============================================================ */

               function closeLightbox() {
                              if (!lightbox) {
                                             return;
                              }

                              lightbox.classList.remove("active");

                              document.body.classList.remove("lightbox-open");

                              lightbox.setAttribute("aria-hidden", "true");

                              /* Stop image loading when closed */
                              if (lightboxImage) {
                                             lightboxImage.src = "";
                              }
               }

               /* ============================================================
                  SHOW PREVIOUS IMAGE
               ============================================================ */

               function showPreviousImage() {
                              updateVisibleItems();

                              if (!visibleItems.length) {
                                             return;
                              }

                              currentIndex =
                                             (currentIndex - 1 + visibleItems.length) % visibleItems.length;

                              updateLightbox();
               }

               /* ============================================================
                  SHOW NEXT IMAGE
               ============================================================ */

               function showNextImage() {
                              updateVisibleItems();

                              if (!visibleItems.length) {
                                             return;
                              }

                              currentIndex = (currentIndex + 1) % visibleItems.length;

                              updateLightbox();
               }

               /* ============================================================
                  CLICK GALLERY ITEMS
               ============================================================ */

               galleryItems.forEach(function (item) {
                              item.addEventListener("click", function (event) {
                                             /*
                                              * If the HTML contains buttons/links inside the gallery item,
                                              * don't open the lightbox when those controls are clicked.
                                              */
                                             if (
                                                            event.target.closest("button") ||
                                                            event.target.closest("a")
                                             ) {
                                                            return;
                                             }

                                             openLightbox(item);
                              });

                              /* Keyboard accessibility */
                              item.setAttribute("tabindex", "0");

                              item.addEventListener("keydown", function (event) {
                                             if (event.key === "Enter" || event.key === " ") {
                                                            event.preventDefault();
                                                            openLightbox(item);
                                             }
                              });
               });

               /* ============================================================
                  CLOSE BUTTON
               ============================================================ */

               if (lightboxClose) {
                              lightboxClose.addEventListener("click", function (event) {
                                             event.stopPropagation();
                                             closeLightbox();
                              });
               }

               /* ============================================================
                  PREVIOUS BUTTON
               ============================================================ */

               if (lightboxPrevious) {
                              lightboxPrevious.addEventListener("click", function (event) {
                                             event.stopPropagation();
                                             showPreviousImage();
                              });
               }

               /* ============================================================
                  NEXT BUTTON
               ============================================================ */

               if (lightboxNext) {
                              lightboxNext.addEventListener("click", function (event) {
                                             event.stopPropagation();
                                             showNextImage();
                              });
               }

               /* ============================================================
                  CLOSE WHEN CLICKING LIGHTBOX BACKGROUND
               ============================================================ */

               if (lightbox) {
                              lightbox.addEventListener("click", function (event) {
                                             /*
                                              * Only close when the actual lightbox background is clicked.
                                              * Clicking the image/content will not close it.
                                              */
                                             if (event.target === lightbox) {
                                                            closeLightbox();
                                             }
                              });
               }

               /* ============================================================
                  KEYBOARD CONTROLS
               ============================================================ */

               document.addEventListener("keydown", function (event) {
                              if (!lightbox || !lightbox.classList.contains("active")) {
                                             return;
                              }

                              switch (event.key) {
                                             case "Escape":
                                                            closeLightbox();
                                                            break;

                                             case "ArrowLeft":
                                                            showPreviousImage();
                                                            break;

                                             case "ArrowRight":
                                                            showNextImage();
                                                            break;
                              }
               });

               /* ============================================================
                  TOUCH / SWIPE SUPPORT
               ============================================================ */

               let touchStartX = 0;
               let touchEndX = 0;

               if (lightbox) {
                              lightbox.addEventListener(
                                             "touchstart",
                                             function (event) {
                                                            touchStartX = event.changedTouches[0].screenX;
                                             },
                                             { passive: true }
                              );

                              lightbox.addEventListener(
                                             "touchend",
                                             function (event) {
                                                            touchEndX = event.changedTouches[0].screenX;

                                                            handleSwipe();
                                             },
                                             { passive: true }
                              );
               }

               function handleSwipe() {
                              const swipeDistance = touchEndX - touchStartX;

                              /* Minimum swipe distance */
                              if (Math.abs(swipeDistance) < 50) {
                                             return;
                              }

                              if (swipeDistance > 0) {
                                             showPreviousImage();
                              } else {
                                             showNextImage();
                              }
               }

               /* ============================================================
                  INITIAL GALLERY STATE
               ============================================================ */

               galleryItems.forEach(function (item) {
                              /*
                               * Make all gallery items visible initially.
                               * The "all" filter is the default.
                               */
                              item.classList.remove("hidden");

                              setTimeout(function () {
                                             item.classList.add("visible");
                              }, 20);
               });

               /* Set initial active filter */
               if (filterButtons.length > 0) {
                              let activeButton = document.querySelector(
                                             ".gallery-filter-btn.active"
                              );

                              if (!activeButton) {
                                             activeButton = filterButtons[0];
                                             activeButton.classList.add("active");
                              }
               }

               /* ============================================================
                  PRELOAD GALLERY IMAGES
               ============================================================ */

               galleryItems.forEach(function (item) {
                              const image = item.querySelector("img");

                              if (image && image.src) {
                                             const preloadImage = new Image();
                                             preloadImage.src = image.src;
                              }
               });
});