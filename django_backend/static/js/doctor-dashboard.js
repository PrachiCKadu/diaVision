document.addEventListener("DOMContentLoaded", async () => {
    "use strict";

    /* =========================================================
       ELEMENT REFERENCES
    ========================================================= */

    const container = document.getElementById("doctor-cases-container");
    const tableBody = document.getElementById("doctor-cases-table-body");
    const countElement = document.getElementById("doctor-case-count");
    const statusElement = document.getElementById("doctor-case-status");
    const messageElement = document.getElementById("doctor-case-message");
    const overviewStatus = document.getElementById("overview-status");

    const totalCasesElement = document.getElementById("metric-total-cases");
    const pendingReviewsElement = document.getElementById("metric-pending-reviews");
    const reviewedCasesElement = document.getElementById("metric-reviewed-cases");
    const reportsElement = document.getElementById("metric-reports");

    const searchInput = document.getElementById("case-search");
    const reviewStatusFilter = document.getElementById("review-status-filter");

    const pendingList = document.getElementById("pending-cases-list");
    const pendingListCount = document.getElementById("pending-list-count");

    let allCases = [];
    let overviewData = null;

    if (!container || !tableBody || !countElement) {
        return;
    }

    /* =========================================================
       HELPERS
    ========================================================= */

    function escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = value ?? "";
        return div.innerHTML;
    }

    function formatDate(dateString) {
        if (!dateString) return "—";
        const date = new Date(dateString);
        if (Number.isNaN(date.getTime())) return "—";
        return date.toLocaleString();
    }

    function formatConfidence(value) {
        if (value === null || value === undefined) return "—";
        return `${(Number(value) * 100).toFixed(1)}%`;
    }

    function showMessage(message, type = "error") {
        if (!messageElement) return;
        messageElement.textContent = message;
        messageElement.className = `form-message ${type}`;
        messageElement.style.display = "block";
    }

    function getDiagnosisBadge(prediction) {
        if (!prediction) {
            return `<span class="status-badge">Pending</span>`;
        }
        return `<span class="status-badge">${escapeHtml(prediction.predicted_class)}</span>`;
    }

    function getGradcamStatus(prediction) {
        if (prediction && prediction.gradcam_image) {
            return `<span class="status-badge">Available</span>`;
        }
        return `<span class="status-badge">Not Available</span>`;
    }

    function getReviewStatus(caseItem) {
        if (caseItem.doctor_review) {
            return `<span class="status-badge">Reviewed</span>`;
        }
        return `<span class="status-badge">Pending Review</span>`;
    }

    function getReportStatus(caseItem) {
        if (caseItem.medical_report) {
            return `<span class="status-badge">Generated</span>`;
        }
        return `<span class="status-badge">Not Generated</span>`;
    }

    /* =========================================================
       FILTER + RENDER CASE TABLE
    ========================================================= */

    function filterCases() {
        const searchTerm = searchInput?.value.trim().toLowerCase() || "";
        const status = reviewStatusFilter?.value || "all";

        const filteredCases = allCases.filter((caseItem) => {
            const patientId = String(caseItem.patient_id ?? "").toLowerCase();
            const caseId = String(caseItem.id ?? "").toLowerCase();

            const matchesSearch =
                !searchTerm ||
                caseId.includes(searchTerm) ||
                patientId.includes(searchTerm);

            const isReviewed = Boolean(caseItem.doctor_review);

            const matchesStatus =
                status === "all" ||
                (status === "reviewed" && isReviewed) ||
                (status === "pending" && !isReviewed);

            return matchesSearch && matchesStatus;
        });

        renderCases(filteredCases);
    }

    function renderCases(cases) {
        countElement.textContent = `${cases.length} Cases`;

        if (statusElement) {
            statusElement.textContent = `${cases.length} Available`;
        }

        if (!cases.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="10" class="empty-state">
                        <h3>No Retinal Cases</h3>
                        <p>There are currently no retinal cases available for review.</p>
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = cases.map((caseItem) => {
            const prediction = caseItem.prediction;

            return `
                <tr>
                    <td><strong>#${caseItem.id}</strong></td>
                    <td>Patient #${escapeHtml(caseItem.patient_id)}</td>
                    <td>
                        <img
                            src="${escapeHtml(caseItem.image)}"
                            alt="Retinal image for Case #${caseItem.id}"
                            class="retinal-table-image"
                        >
                    </td>
                    <td>${getDiagnosisBadge(prediction)}</td>
                    <td>${formatConfidence(prediction?.confidence)}</td>
                    <td>${getGradcamStatus(prediction)}</td>
                    <td>${getReviewStatus(caseItem)}</td>
                    <td>${getReportStatus(caseItem)}</td>
                    <td>${formatDate(caseItem.uploaded_at)}</td>
                    <td>
                        <div class="table-actions">
                            <a href="/doctor/cases/${caseItem.id}/" class="dashboard-button">
                                Review Case
                            </a>
                        </div>
                    </td>
                </tr>
            `;
        }).join("");
    }

    /* =========================================================
       PENDING CASES SIDE LIST (driven by real case data)
    ========================================================= */

    const avatarClasses = ["avatar-pink", "avatar-green", "avatar-orange", "avatar-purple"];

    function renderPendingList() {
        if (!pendingList) return;

        const pending = allCases.filter((c) => !c.doctor_review);

        if (pendingListCount) {
            pendingListCount.textContent = pending.length;
        }

        if (!pending.length) {
            pendingList.innerHTML = `<div class="pending-empty">No cases pending review.</div>`;
            return;
        }

        const topPending = pending
            .slice()
            .sort((a, b) => new Date(b.uploaded_at || 0) - new Date(a.uploaded_at || 0))
            .slice(0, 5);

        pendingList.innerHTML = topPending.map((caseItem, index) => {
            const avatarClass = avatarClasses[index % avatarClasses.length];
            const prediction = caseItem.prediction;
            const label = prediction ? escapeHtml(prediction.predicted_class) : "Awaiting AI analysis";

            return `
                <a class="patient" href="/doctor/cases/${caseItem.id}/">
                    <div class="patient-avatar ${avatarClass}">#${escapeHtml(caseItem.id)}</div>
                    <div class="patient-info">
                        <strong>Patient #${escapeHtml(caseItem.patient_id)}</strong>
                        <span>${label}</span>
                    </div>
                    <span class="arrow">›</span>
                </a>
            `;
        }).join("");
    }

    /* =========================================================
       DATA LOADING
    ========================================================= */

    if (searchInput) {
        searchInput.addEventListener("input", filterCases);
    }

    if (reviewStatusFilter) {
        reviewStatusFilter.addEventListener("change", filterCases);
    }

    async function loadDoctorCases() {
        tableBody.innerHTML = `
            <tr><td colspan="10" class="loading-state">Loading retinal cases...</td></tr>
        `;

        try {
            const cases = await apiRequest("/doctors/cases/");
            allCases = cases;
            renderCases(allCases);
            renderPendingList();
        } catch (error) {
            console.error("Doctor case loading error:", error);

            countElement.textContent = "Error";

            if (statusElement) {
                statusElement.textContent = "Unable to Load";
            }

            tableBody.innerHTML = `
                <tr>
                    <td colspan="10" class="empty-state">
                        <h3>Unable to Load Cases</h3>
                        <p>${escapeHtml(error.message)}</p>
                    </td>
                </tr>
            `;

            if (pendingList) {
                pendingList.innerHTML = `<div class="pending-empty">Unable to load cases.</div>`;
            }

            showMessage(error.message, "error");
        }
    }

    async function loadDashboardOverview() {
        try {
            const overview = await apiRequest("/doctors/dashboard/overview/");
            overviewData = overview;

            if (totalCasesElement) totalCasesElement.textContent = overview.total_cases ?? 0;
            if (pendingReviewsElement) pendingReviewsElement.textContent = overview.pending_reviews ?? 0;
            if (reviewedCasesElement) reviewedCasesElement.textContent = overview.reviewed_cases ?? 0;
            if (reportsElement) reportsElement.textContent = overview.reports_generated ?? 0;

            if (overviewStatus) overviewStatus.textContent = "Live";
        } catch (error) {
            console.error("Dashboard overview loading error:", error);
            if (overviewStatus) overviewStatus.textContent = "Unable to Load";
        }
    }

    await Promise.all([
        loadDashboardOverview(),
        loadDoctorCases(),
    ]);

    /* =========================================================
       UI CHROME: toast, sidebar nav, mobile menu, search shortcut
    ========================================================= */

    function showToast(message) {
        let toast = document.getElementById("dia-toast");

        if (!toast) {
            toast = document.createElement("div");
            toast.id = "dia-toast";

            Object.assign(toast.style, {
                position: "fixed",
                left: "50%",
                bottom: "25px",
                transform: "translateX(-50%)",
                padding: "12px 20px",
                background: "#0b2a50",
                color: "#ffffff",
                borderRadius: "10px",
                fontSize: "14px",
                fontWeight: "600",
                zIndex: "99999",
                boxShadow: "0 8px 25px rgba(0,0,0,.18)",
                opacity: "0",
                transition: "opacity .25s ease",
            });

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.style.opacity = "1";

        clearTimeout(window.diaToastTimer);
        window.diaToastTimer = setTimeout(() => {
            toast.style.opacity = "0";
        }, 2000);
    }

    // Sidebar nav: only intercept placeholder links (no real destination yet)
    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach((item) => {
        const href = item.getAttribute("href") || "";
        const isPlaceholder = href === "#";

        item.addEventListener("click", (event) => {
            navItems.forEach((nav) => nav.classList.remove("active"));
            item.classList.add("active");

            if (isPlaceholder) {
                event.preventDefault();
                showToast(`${item.dataset.action || item.textContent.trim()} — coming soon`);
            }
        });
    });

    // Data-action buttons in the top bar / sidebar footer
    document.querySelectorAll("[data-action]").forEach((el) => {
        if (el.classList.contains("nav-item")) return; // handled above
        el.addEventListener("click", () => {
            showToast(`${el.dataset.action} — coming soon`);
        });
    });

    // Ctrl/Cmd + K focuses search
    document.addEventListener("keydown", (event) => {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            event.preventDefault();
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
    });

    // Global top search jumps to case search + filters the table
    const globalSearch = document.getElementById("searchInput");
    if (globalSearch) {
        globalSearch.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                const value = globalSearch.value.trim();
                if (value && searchInput) {
                    searchInput.value = value;
                    filterCases();
                    document.getElementById("cases")?.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    }

    // Mobile sidebar toggle
    const mobileMenu = document.getElementById("mobileMenu");
    const sidebar = document.querySelector(".sidebar");

    if (mobileMenu && sidebar) {
        mobileMenu.addEventListener("click", (event) => {
            event.stopPropagation();
            sidebar.classList.toggle("open");
        });

        document.addEventListener("click", (event) => {
            if (window.innerWidth <= 1050 && sidebar.classList.contains("open")) {
                if (!sidebar.contains(event.target) && !mobileMenu.contains(event.target)) {
                    sidebar.classList.remove("open");
                }
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 1050) {
                sidebar.classList.remove("open");
            }
        });
    }

    /* =========================================================
       AI DOCTOR ASSISTANT — answers from real loaded data
    ========================================================= */

    const askAIButton = document.getElementById("askAi");
    const aiInput = document.getElementById("aiInput");
    const aiResponse = document.getElementById("aiResponse");

    function answerFromData(question) {
        const q = question.toLowerCase();
        const pendingCount = overviewData?.pending_reviews ?? allCases.filter((c) => !c.doctor_review).length;
        const reviewedCount = overviewData?.reviewed_cases ?? allCases.filter((c) => c.doctor_review).length;
        const totalCount = overviewData?.total_cases ?? allCases.length;
        const reportsCount = overviewData?.reports_generated ?? allCases.filter((c) => c.medical_report).length;

        if (q.includes("pending")) {
            return `You have ${pendingCount} case${pendingCount === 1 ? "" : "s"} pending review.`;
        }
        if (q.includes("reviewed") || q.includes("complete")) {
            return `${reviewedCount} case${reviewedCount === 1 ? "" : "s"} have been reviewed so far.`;
        }
        if (q.includes("total") || q.includes("how many case")) {
            return `There are ${totalCount} retinal case${totalCount === 1 ? "" : "s"} in total.`;
        }
        if (q.includes("report")) {
            return `${reportsCount} medical report${reportsCount === 1 ? "" : "s"} have been generated.`;
        }

        return `I can answer questions about your caseload — try asking about pending, reviewed, total cases, or reports.`;
    }

    function askAI(presetQuestion) {
        if (!aiInput) return;

        const question = presetQuestion ?? aiInput.value.trim();

        if (presetQuestion) {
            aiInput.value = presetQuestion;
        }

        if (!question) {
            if (aiResponse) {
                aiResponse.textContent = "Please enter a question.";
                aiResponse.classList.add("show");
            }
            return;
        }

        if (aiResponse) {
            aiResponse.textContent = answerFromData(question);
            aiResponse.classList.add("show");
        }
    }

    if (askAIButton) {
        askAIButton.addEventListener("click", () => askAI());
    }

    if (aiInput) {
        aiInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                askAI();
            }
        });
    }

    document.querySelectorAll("[data-question]").forEach((button) => {
        button.addEventListener("click", () => askAI(button.dataset.question));
    });
});