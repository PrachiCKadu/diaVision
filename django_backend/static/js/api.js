const API_BASE_URL = "/api";


async function refreshAccessToken() {

    const refreshToken =
        localStorage.getItem("refresh_token");

    if (!refreshToken) {
        return false;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/accounts/token/refresh/`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    refresh: refreshToken,
                }),
            }
        );


        if (!response.ok) {
            throw new Error("Refresh token expired.");
        }


        const data =
            await response.json();


        if (!data.access) {
            throw new Error(
                "No access token received."
            );
        }


        localStorage.setItem(
            "access_token",
            data.access
        );


        if (data.refresh) {
            localStorage.setItem(
                "refresh_token",
                data.refresh
            );
        }


        return true;

    } catch (error) {

        console.error(
            "Token refresh failed:",
            error
        );

        return false;
    }
}


async function apiRequest(
    endpoint,
    options = {},
    retry = true
) {

    const token =
        localStorage.getItem("access_token");


    const headers = {
        ...(options.headers || {}),
    };


    if (token) {
        headers["Authorization"] =
            `Bearer ${token}`;
    }


    const response =
        await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                ...options,
                headers,
            }
        );


    if (response.status === 401 && retry) {

        const refreshed =
            await refreshAccessToken();


        if (refreshed) {

            return apiRequest(
                endpoint,
                options,
                false
            );
        }


        logout();

        throw new Error(
            "Your session has expired. Please login again."
        );
    }


    let data = null;


    try {

        data =
            await response.json();

    } catch {

        data = null;
    }


    if (!response.ok) {

        const errorMessage =
            data?.detail ||
            data?.error ||
            "Something went wrong. Please try again.";

        throw new Error(errorMessage);
    }


    return data;
}


function saveAuthData(data) {

    if (data?.tokens?.access) {

        localStorage.setItem(
            "access_token",
            data.tokens.access
        );
    }


    if (data?.tokens?.refresh) {

        localStorage.setItem(
            "refresh_token",
            data.tokens.refresh
        );
    }


    if (data?.user) {

        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );
    }
}


function getCurrentUser() {

    const user =
        localStorage.getItem("user");


    if (!user) {
        return null;
    }


    try {

        return JSON.parse(user);

    } catch {

        return null;
    }
}


function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "refresh_token"
    );

    localStorage.removeItem(
        "user"
    );


    window.location.href =
        "/login/";
}