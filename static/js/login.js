/* =========================================================
   WAINGO FARM — OWNER LOGIN
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initOwnerLogin();
});


function initOwnerLogin() {
    initPasswordToggle();
    initLoginForm();
    initRememberMe();
}


/* =========================================================
   PASSWORD SHOW / HIDE
   ========================================================= */

function initPasswordToggle() {
    const toggle = document.getElementById("passwordToggle");
    const password = document.getElementById("id_password");

    if (!toggle || !password) {
        return;
    }

    toggle.addEventListener("click", () => {

        const icon = toggle.querySelector("i");

        if (password.type === "password") {

            password.type = "text";

            if (icon) {
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            }

            toggle.setAttribute(
                "aria-label",
                "Hide password"
            );

        } else {

            password.type = "password";

            if (icon) {
                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }

            toggle.setAttribute(
                "aria-label",
                "Show password"
            );
        }

        password.focus();
    });
}


/* =========================================================
   LOGIN FORM
   ========================================================= */

function initLoginForm() {
    const form = document.getElementById("ownerLoginForm");
    const button = document.getElementById("loginButton");

    if (!form || !button) {
        return;
    }

    form.addEventListener("submit", (event) => {

        /*
         * Let Django perform the actual authentication.
         * We only change the visual state while the request
         * is being submitted.
         */

        if (!form.checkValidity()) {
            return;
        }

        button.classList.add("loading");

        button.disabled = true;

        button.setAttribute(
            "aria-busy",
            "true"
        );
    });
}


/* =========================================================
   REMEMBER ME
   ========================================================= */

function initRememberMe() {
    const remember = document.getElementById("rememberMe");

    if (!remember) {
        return;
    }

    /*
     * We don't store passwords or usernames here.
     * The checkbox is simply submitted to Django.
     */

    remember.addEventListener("change", () => {
        remember.setAttribute(
            "aria-checked",
            remember.checked ? "true" : "false"
        );
    });
}


/* =========================================================
   ENTER KEY SUPPORT
   ========================================================= */

document.addEventListener("keydown", (event) => {

    if (event.key !== "Enter") {
        return;
    }

    const activeElement = document.activeElement;

    if (!activeElement) {
        return;
    }

    if (
        activeElement.id === "id_username" ||
        activeElement.id === "id_password"
    ) {
        const form = document.getElementById(
            "ownerLoginForm"
        );

        if (form) {
            /*
             * Don't manually submit with form.submit(),
             * because that bypasses browser validation.
             */
            if (form.requestSubmit) {
                form.requestSubmit();
            }
        }
    }
});