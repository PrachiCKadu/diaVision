function saveAuthData(data) {

    localStorage.setItem(
        "access_token",
        data.tokens.access
    );

    localStorage.setItem(
        "refresh_token",
        data.tokens.refresh
    );

    localStorage.setItem(
        "user",
        JSON.stringify(data.user)
    );
}


document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("login-form");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const username =
            document.getElementById("username").value.trim();

        const password =
            document.getElementById("password").value;

        const errorElement =
            document.getElementById("login-error");

        const loginButton =
            document.getElementById("login-btn");

        errorElement.style.display = "none";
        errorElement.textContent = "";

        loginButton.disabled = true;
        loginButton.textContent = "Signing in...";

        try {

            const response = await fetch(
                "/api/accounts/login/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        username,
                        password,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data?.error ||
                    data?.detail ||
                    "Invalid username or password."
                );
            }

            saveAuthData(data);

            const role = data.user?.role;

            if (role === "PATIENT") {
                window.location.href = "/patient/dashboard/";
            }

            else if (role === "DOCTOR") {
                window.location.href = "/doctor/dashboard/";
            }

            else if (role === "ADMIN") {
                window.location.href = "/admin-dashboard/";
            }

            else {
                throw new Error(
                    "Your account does not have a valid application role."
                );
            }

        } catch (error) {

            errorElement.textContent =
                error.message;

            errorElement.style.display =
                "block";

        } finally {

            loginButton.disabled = false;
            loginButton.textContent = "Login";
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("login-form");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const username =
            document.getElementById("username").value.trim();

        const password =
            document.getElementById("password").value;

        const errorElement =
            document.getElementById("login-error");

        const loginButton =
            document.getElementById("login-btn");

        errorElement.style.display = "none";
        errorElement.textContent = "";

        loginButton.disabled = true;
        loginButton.textContent = "Signing in...";

        try {

            const response = await fetch(
                "/api/accounts/login/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        username,
                        password,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data?.error ||
                    data?.detail ||
                    "Invalid username or password."
                );
            }

            saveAuthData(data);

            const role = data.user?.role;

            if (role === "PATIENT") {
                window.location.href = "/patient/dashboard/";
            }

            else if (role === "DOCTOR") {
                window.location.href = "/doctor/dashboard/";
            }

            else if (role === "ADMIN") {
                window.location.href = "/admin-dashboard/";
            }

            else {
                throw new Error(
                    "Your account does not have a valid application role."
                );
            }

           

        } catch (error) {

            errorElement.textContent =
                error.message;

            errorElement.style.display =
                "block";

        } finally {

            loginButton.disabled = false;
            loginButton.textContent = "Login";
        }
    });
});