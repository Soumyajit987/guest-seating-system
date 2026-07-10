// ==============================
// SMART EVENT SEATING PLANNER
// ==============================

document.addEventListener("DOMContentLoaded", () => {

    // -----------------------------
    // File Upload Preview
    // -----------------------------

    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");

    if (fileInput) {

        fileInput.addEventListener("change", function () {

            if (this.files.length > 0) {

                fileName.innerHTML =
                    `<i class="fa-solid fa-file-lines"></i> ${this.files[0].name}`;

                showToast("Dataset uploaded successfully ✔");

            }

        });

    }

    // -----------------------------
    // Form Validation
    // -----------------------------

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", function (e) {

            const tables =
                document.querySelector('input[name="tables"]');

            const capacity =
                document.querySelector('input[name="capacity"]');

            if (tables.value <= 0 || capacity.value <= 0) {

                e.preventDefault();

                showToast("Enter valid values!");

                return;

            }

            loadingAnimation();

        });

    }

    // -----------------------------
    // Table Card Animation
    // -----------------------------

    const cards =
        document.querySelectorAll(".table-card");

    cards.forEach((card, index) => {

        card.style.opacity = 0;

        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition =
                "0.7s ease";

            card.style.opacity = 1;

            card.style.transform =
                "translateY(0px)";

        }, index * 200);

    });

    // -----------------------------
    // Button Hover Glow
    // -----------------------------

    const button =
        document.querySelector(".generate-btn");

    if (button) {

        button.addEventListener("mouseenter", () => {

            button.style.boxShadow =
                "0 0 30px rgba(255,193,7,.7)";

        });

        button.addEventListener("mouseleave", () => {

            button.style.boxShadow =
                "";

        });

    }

});

// ===================================
// Toast Notification
// ===================================

function showToast(message) {

    const toast =
        document.createElement("div");

    toast.className = "toast";

    toast.innerHTML =
        `<i class="fa-solid fa-circle-check"></i> ${message}`;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 500);

    }, 2500);

}

// ===================================
// Loading Animation
// ===================================

function loadingAnimation() {

    const button =
        document.querySelector(".generate-btn");

    button.disabled = true;

    button.innerHTML =

    `<i class="fa-solid fa-spinner fa-spin"></i>
     Generating Seating Plan...`;

}