document.addEventListener("DOMContentLoaded", async () => {

    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    try {
        const response = await fetch(
            "/api/accounts/me/",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            }
        );

        if (!response.ok) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("user");

            window.location.href = "/login/";
            return;
        }

        const data = await response.json();

        const requiredRole =
            document.body.dataset.requiredRole;

        const currentRole =
            data.user?.role;

        if (
            requiredRole &&
            currentRole !== requiredRole
        ) {
            if (currentRole === "PATIENT") {
                window.location.href =
                    "/patient/dashboard/";
            }

            else if (currentRole === "DOCTOR") {
                window.location.href =
                    "/doctor/dashboard/";
            }

            else if (currentRole === "ADMIN") {
                window.location.href =
                    "/admin-dashboard/";
            }

            return;
        }

    } catch (error) {

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");

        window.location.href = "/login/";
    }
});