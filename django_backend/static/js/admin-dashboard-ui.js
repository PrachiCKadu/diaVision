/* =========================================================
   ADMIN DASHBOARD — Topbar profile + logout
   Loaded AFTER admin-dashboard.js. Does not fetch any new data
   itself — it mirrors whatever admin-dashboard.js already puts
   into #admin-welcome ("Welcome, <name>.") into the avatar/name
   in the topbar, and provides a safety-net logout in case the
   site's global auth.js does not already bind #logout-btn.
========================================================= */

(function () {
    "use strict";

    function getInitials(name) {
        if (!name) return "A";
        var parts = name.trim().split(/\s+/).filter(Boolean);
        if (parts.length === 0) return "A";
        var initials = parts.slice(0, 2).map(function (p) {
            return p.charAt(0).toUpperCase();
        });
        return initials.join("") || "A";
    }

    function syncProfileFromWelcome() {
        var source = document.getElementById("admin-welcome");
        if (!source) return;

        var raw = source.textContent.trim();
        if (!raw || /loading/i.test(raw)) return;

        // "Welcome, Dr. Priya." -> "Dr. Priya"
        var displayName = raw
            .replace(/^welcome,?\s*/i, "")
            .replace(/\.$/, "")
            .trim() || "Admin";

        var initials = getInitials(displayName);

        ["admin-profile-name", "admin-profile-name-lg"].forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.textContent = displayName;
        });

        ["admin-avatar", "admin-avatar-lg"].forEach(function (id) {
            var el = document.getElementById(id);
            if (el) el.textContent = initials;
        });
    }

    function setupLogoutFallback() {
        var logoutBtn = document.getElementById("logout-btn");
        if (!logoutBtn || logoutBtn.dataset.fallbackBound === "true") return;

        logoutBtn.dataset.fallbackBound = "true";

        logoutBtn.addEventListener("click", function () {
            // Give the site's own auth.js a chance to handle this click first
            // (it may already redirect the page). This only fires if nothing
            // else has navigated away in the meantime.
            window.setTimeout(function () {
                try {
                    localStorage.removeItem("authToken");
                    localStorage.removeItem("accessToken");
                    localStorage.removeItem("token");
                    sessionStorage.clear();
                } catch (err) {
                    /* storage may be unavailable — ignore */
                }
                window.location.href = "/login/";
            }, 250);
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        syncProfileFromWelcome();
        setupLogoutFallback();

        var watchTarget = document.getElementById("admin-welcome");
        if (watchTarget && window.MutationObserver) {
            new MutationObserver(syncProfileFromWelcome).observe(watchTarget, {
                childList: true,
                characterData: true,
                subtree: true,
            });
        }
    });
})();