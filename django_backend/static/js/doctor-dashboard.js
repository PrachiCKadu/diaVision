document.addEventListener("DOMContentLoaded", async () => {

    const container =
        document.getElementById("doctor-cases-container");

    const tableBody =
        document.getElementById("doctor-cases-table-body");

    const countElement =
        document.getElementById("doctor-case-count");

    const statusElement =
        document.getElementById("doctor-case-status");

    const messageElement =
        document.getElementById("doctor-case-message");

    const overviewStatus =
        document.getElementById("overview-status");

    const totalCasesElement =
        document.getElementById("metric-total-cases");

    const pendingReviewsElement =
        document.getElementById("metric-pending-reviews");

    const reviewedCasesElement =
        document.getElementById("metric-reviewed-cases");

    const reportsElement =
        document.getElementById("metric-reports");

    const searchInput =
        document.getElementById("case-search");

    const reviewStatusFilter =
        document.getElementById("review-status-filter");

    let allCases = [];


    if (!container || !tableBody || !countElement) {
        return;
    }


    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent =
            value ?? "";

        return div.innerHTML;
    }


    function formatDate(dateString) {

        if (!dateString) {
            return "—";
        }

        const date =
            new Date(dateString);

        if (Number.isNaN(date.getTime())) {
            return "—";
        }

        return date.toLocaleString();
    }


    function formatConfidence(value) {

        if (
            value === null ||
            value === undefined
        ) {
            return "—";
        }

        return `${(
            Number(value) * 100
        ).toFixed(1)}%`;
    }


    function showMessage(
        message,
        type = "error"
    ) {

        if (!messageElement) {
            return;
        }

        messageElement.textContent =
            message;

        messageElement.className =
            `form-message ${type}`;

        messageElement.style.display =
            "block";
    }


    function getDiagnosisBadge(prediction) {

        if (!prediction) {

            return `
                <span class="status-badge">
                    Pending
                </span>
            `;
        }

        return `
            <span class="status-badge">
                ${escapeHtml(
            prediction.predicted_class
        )}
            </span>
        `;
    }


    function getGradcamStatus(prediction) {

        if (
            prediction &&
            prediction.gradcam_image
        ) {

            return `
                <span class="status-badge">
                    Available
                </span>
            `;
        }

        return `
            <span class="status-badge">
                Not Available
            </span>
        `;
    }


    function getReviewStatus(caseItem) {

        if (caseItem.doctor_review) {

            return `
                <span class="status-badge">
                    Reviewed
                </span>
            `;
        }

        return `
            <span class="status-badge">
                Pending Review
            </span>
        `;
    }
    
function getReportStatus(caseItem) {

    if (caseItem.medical_report) {

        return `
            <span class="status-badge">
                Generated
            </span>
        `;
    }

    return `
        <span class="status-badge">
            Not Generated
        </span>
    `;
}

    function filterCases() {

        const searchTerm =
            searchInput?.value
                .trim()
                .toLowerCase() || "";

        const status =
            reviewStatusFilter?.value || "all";


        const filteredCases =
            allCases.filter((caseItem) => {

                const patientId =
                    String(
                        caseItem.patient_id ?? ""
                    ).toLowerCase();

                const caseId =
                    String(
                        caseItem.id ?? ""
                    ).toLowerCase();

                const matchesSearch =
                    !searchTerm ||
                    caseId.includes(searchTerm) ||
                    patientId.includes(searchTerm);


                const isReviewed =
                    Boolean(
                        caseItem.doctor_review
                    );


                const matchesStatus =
                    status === "all" ||
                    (
                        status === "reviewed" &&
                        isReviewed
                    ) ||
                    (
                        status === "pending" &&
                        !isReviewed
                    );


                return (
                    matchesSearch &&
                    matchesStatus
                );
            });


        renderCases(filteredCases);
    }


    function renderCases(cases) {

        countElement.textContent =
            `${cases.length} Cases`;

        if (statusElement) {

            statusElement.textContent =
                `${cases.length} Available`;
        }


        if (!cases.length) {

            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="10"
                        class="empty-state"
                    >
                        <h3>No Retinal Cases</h3>

                        <p>
                            There are currently no
                            retinal cases available
                            for review.
                        </p>
                    </td>
                </tr>
            `;

            return;
        }


        tableBody.innerHTML =
            cases.map((caseItem) => {

                const prediction =
                    caseItem.prediction;

                const review =
                    caseItem.doctor_review;

                return `
                    <tr>

                        <td>
                            <strong>
                                #${caseItem.id}
                            </strong>
                        </td>


                        <td>
                            Patient #${escapeHtml(
                    caseItem.patient_id
                )}
                        </td>

                        <td>
    <img
        src="${escapeHtml(caseItem.image)}"
        alt="Retinal image for Case #${caseItem.id}"
        class="retinal-table-image"
    >
</td>


                        <td>
                            ${getDiagnosisBadge(
                    prediction
                )}
                        </td>


                        <td>
                            ${formatConfidence(
                    prediction?.confidence
                )}
                        </td>


                        <td>
                            ${getGradcamStatus(
                    prediction
                )}
                        </td>


                        <td>
    ${getReviewStatus(caseItem)}
</td>

<td>
    ${getReportStatus(caseItem)}
</td>


                        <td>
                            ${formatDate(
                    caseItem.uploaded_at
                )}
                        </td>


                        <td>

                            <div
                                class="table-actions"
                            >

                                <div class="table-actions">

    <a
        href="/doctor/cases/${caseItem.id}/"
        class="dashboard-button"
    >
        Review Case
    </a>

</div>

                            </div>

                        </td>

                    </tr>
                `;

            }).join("");
    }


    if (searchInput) {

        searchInput.addEventListener(
            "input",
            filterCases
        );
    }


    if (reviewStatusFilter) {

        reviewStatusFilter.addEventListener(
            "change",
            filterCases
        );
    }

    async function loadDoctorCases() {

        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="10"
                    class="loading-state"
                >
                    Loading retinal cases...
                </td>
            </tr>
        `;


        try {

            const cases =
                await apiRequest(
                    "/doctors/cases/"
                );


            allCases = cases;

            renderCases(allCases);

        } catch (error) {

            console.error(
                "Doctor case loading error:",
                error
            );


            countElement.textContent =
                "Error";


            if (statusElement) {

                statusElement.textContent =
                    "Unable to Load";
            }


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="10"
                        class="empty-state"
                    >

                        <h3>
                            Unable to Load Cases
                        </h3>

                        <p>
                            ${escapeHtml(
                error.message
            )}
                        </p>

                    </td>
                </tr>
            `;


            showMessage(
                error.message,
                "error"
            );
        }
    }


    async function loadDashboardOverview() {

        try {

            const overview =
                await apiRequest(
                    "/doctors/dashboard/overview/"
                );


            if (totalCasesElement) {
                totalCasesElement.textContent =
                    overview.total_cases ?? 0;
            }

            if (pendingReviewsElement) {
                pendingReviewsElement.textContent =
                    overview.pending_reviews ?? 0;
            }

            if (reviewedCasesElement) {
                reviewedCasesElement.textContent =
                    overview.reviewed_cases ?? 0;
            }

            if (reportsElement) {
                reportsElement.textContent =
                    overview.reports_generated ?? 0;
            }


            if (overviewStatus) {
                overviewStatus.textContent =
                    "Live";
            }


        } catch (error) {

            console.error(
                "Dashboard overview loading error:",
                error
            );


            if (overviewStatus) {
                overviewStatus.textContent =
                    "Unable to Load";
            }

        }
    }

    await Promise.all([
        loadDashboardOverview(),
        loadDoctorCases(),
    ]);

});