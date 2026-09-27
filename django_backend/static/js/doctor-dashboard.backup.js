document.addEventListener("DOMContentLoaded", async () => {

    const container =
        document.getElementById("doctor-cases-container");

    const countElement =
        document.getElementById("doctor-case-count");

    const statusElement =
        document.getElementById("doctor-case-status");

    const messageElement =
        document.getElementById("doctor-case-message");


    if (!container || !countElement) {
        return;
    }


    function getAccessToken() {
        return localStorage.getItem("access_token");
    }


    function escapeHtml(value) {

        const div = document.createElement("div");

        div.textContent = value ?? "";

        return div.innerHTML;
    }


    function formatDate(dateString) {

        if (!dateString) {
            return "—";
        }

        const date = new Date(dateString);

        if (Number.isNaN(date.getTime())) {
            return "—";
        }

        return date.toLocaleString();
    }


    function showMessage(message, type = "error") {

        if (!messageElement) {
            return;
        }

        messageElement.textContent = message;
        messageElement.className =
            `form-message ${type}`;

        messageElement.style.display = "block";
    }


    function getPredictionStatus(prediction) {

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


    function getConfidence(prediction) {

        if (
            !prediction ||
            prediction.confidence === null ||
            prediction.confidence === undefined
        ) {
            return "—";
        }

        return `${(
            Number(prediction.confidence) * 100
        ).toFixed(1)}%`;
    }


    function renderCases(cases) {

        countElement.textContent =
            `${cases.length} Cases`;

        if (statusElement) {
            statusElement.textContent =
                `${cases.length} Available`;
        }


        if (cases.length === 0) {

            container.innerHTML = `
                <div class="empty-state">

                    <h3>No Retinal Cases</h3>

                    <p>
                        There are currently no retinal
                        cases available for review.
                    </p>

                </div>
            `;

            return;
        }


        container.innerHTML = cases.map((caseItem) => {

            const prediction =
                caseItem.prediction;

            return `

                <div class="dashboard-card doctor-case-card">

                    <div class="case-card-header">

                        <div>

                            <h3>
                                Retinal Case #${caseItem.id}
                            </h3>

                            <p>
                                Patient ID:
                                ${escapeHtml(
                                    caseItem.patient_id
                                )}
                            </p>

                        </div>

                        ${getPredictionStatus(
                            prediction
                        )}

                    </div>


                    <div class="case-card-body">

                        <div class="case-image-wrapper">

                            <img
                                src="${escapeHtml(
                                    caseItem.image
                                )}"
                                alt="Retinal image"
                                class="retinal-case-image"
                            >

                        </div>


                        <div class="case-information">

                            <div class="case-info-row">

                                <strong>
                                    Uploaded
                                </strong>

                                <span>
                                    ${formatDate(
                                        caseItem.uploaded_at
                                    )}
                                </span>

                            </div>


                            <div class="case-info-row">

                                <strong>
                                    AI Diagnosis
                                </strong>

                                <span>
                                    ${prediction
                                        ? escapeHtml(
                                            prediction.predicted_class
                                        )
                                        : "Pending"}
                                </span>

                            </div>


                            <div class="case-info-row">

                                <strong>
                                    Confidence
                                </strong>

                                <span>
                                    ${getConfidence(
                                        prediction
                                    )}
                                </span>

                            </div>


                            <div class="case-info-row">

                                <strong>
                                    Grad-CAM
                                </strong>

                                <span>
                                    ${
                                        prediction?.gradcam_image
                                            ? "Available"
                                            : "Not Available"
                                    }
                                </span>

                            </div>

                        </div>

                    </div>


                    <div class="doctor-case-actions">

                        <a
                            href="/doctor/cases/${caseItem.id}/"
                            class="dashboard-button"
                        >
                            Review Case
                        </a>

                    </div>

                </div>

            `;

        }).join("");
    }


    async function loadDoctorCases() {

        const token =
            getAccessToken();


        if (!token) {

            container.innerHTML = `
                <div class="empty-state">

                    <h3>Authentication Required</h3>

                    <p>
                        Please login again to access
                        doctor cases.
                    </p>

                </div>
            `;

            countElement.textContent =
                "Authentication Required";

            return;
        }


        try {

            const response = await fetch(
                "/api/doctors/cases/",
                {
                    method: "GET",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`,

                        "Content-Type":
                            "application/json"
                    }
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to load doctor cases."
                );
            }


            renderCases(data);


        } catch (error) {

            console.error(
                "Doctor case loading error:",
                error
            );


            container.innerHTML = `
                <div class="empty-state">

                    <h3>
                        Unable to Load Cases
                    </h3>

                    <p>
                        ${escapeHtml(
                            error.message
                        )}
                    </p>

                </div>
            `;


            countElement.textContent =
                "Error";


            if (statusElement) {
                statusElement.textContent =
                    "Error";
            }


            showMessage(
                error.message,
                "error"
            );
        }
    }


    await loadDoctorCases();

});