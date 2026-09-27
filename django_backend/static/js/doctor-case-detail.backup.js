document.addEventListener("DOMContentLoaded", async () => {

    const caseId = window.DOCTOR_CASE_ID;

    const loadingElement =
        document.getElementById("case-loading");

    const contentElement =
        document.getElementById("case-content");

    const messageElement =
        document.getElementById("case-message");

    const reviewForm =
        document.getElementById("doctor-review-form");

    const reviewButton =
        document.getElementById("review-submit-btn");


    if (!caseId) {
        showMessage("Invalid retinal case.", true);
        return;
    }


    function showMessage(message, isError = false) {

        messageElement.textContent = message;
        messageElement.style.display = "block";

        if (isError) {
            messageElement.classList.add("error");
        } else {
            messageElement.classList.remove("error");
        }
    }


    function formatPercentage(value) {

        if (value === null || value === undefined) {
            return "—";
        }

        return `${(Number(value) * 100).toFixed(1)}%`;
    }


    function formatDate(value) {

        if (!value) {
            return "—";
        }

        return new Date(value).toLocaleString();
    }


    function setText(id, value) {

        const element =
            document.getElementById(id);

        if (element) {
            element.textContent =
                value ?? "—";
        }
    }


    function renderProbabilities(prediction) {

        const container =
            document.getElementById("probability-list");

        if (!container) {
            return;
        }

        const probabilities = [
            {
                label: "No DR",
                value: prediction.no_dr_probability,
            },
            {
                label: "Mild DR",
                value: prediction.mild_probability,
            },
            {
                label: "Moderate DR",
                value: prediction.moderate_probability,
            },
            {
                label: "Severe DR",
                value: prediction.severe_probability,
            },
            {
                label: "Proliferative DR",
                value: prediction.proliferative_dr_probability,
            },
        ];

        container.innerHTML = "";

        probabilities.forEach((item) => {

            const row =
                document.createElement("div");

            row.className =
                "probability-row";

            row.innerHTML = `
                <div class="probability-header">
                    <span>${item.label}</span>
                    <strong>
                        ${formatPercentage(item.value)}
                    </strong>
                </div>

                <div class="probability-bar">
                    <div
                        class="probability-fill"
                        style="width: ${Number(item.value || 0) * 100
                }%"
                    ></div>
                </div>
            `;

            container.appendChild(row);
        });
    }


    async function loadCase() {

        try {

            const data =
                await apiRequest(
                    `/doctors/cases/${caseId}/`
                );


            const prediction =
                data.prediction;


            document.getElementById("case-title")
                .textContent =
                `Retinal Case #${data.id}`;


            setText(
                "patient-username",
                data.patient_username
            );

            setText(
                "patient-age",
                data.patient_age
                    ? `${data.patient_age} years`
                    : "Not provided"
            );

            setText(
                "patient-gender",
                data.patient_gender || "Not provided"
            );

            setText(
                "diabetes-duration",
                data.diabetes_duration_years !== null &&
                    data.diabetes_duration_years !== undefined
                    ? `${data.diabetes_duration_years} years`
                    : "Not provided"
            );


            const retinalImage =
                document.getElementById("retinal-image");

            retinalImage.src =
                data.image;


            if (prediction) {

                setText(
                    "predicted-class",
                    prediction.predicted_class
                );

                setText(
                    "prediction-confidence",
                    formatPercentage(
                        prediction.confidence
                    )
                );


                renderProbabilities(
                    prediction
                );


                const gradcamImage =
                    document.getElementById(
                        "gradcam-image"
                    );


                if (prediction.gradcam_image) {

                    let gradcamUrl =
                        prediction.gradcam_image;

                    if (
                        gradcamUrl.startsWith("/")
                    ) {
                        gradcamUrl =
                            `${window.location.origin}${gradcamUrl}`;
                    }

                    gradcamImage.src =
                        gradcamUrl;

                } else {

                    gradcamImage.style.display =
                        "none";

                    const parent =
                        gradcamImage.parentElement;

                    parent.insertAdjacentHTML(
                        "beforeend",
                        "<p>Grad-CAM is not available for this prediction.</p>"
                    );
                }

            } else {

                setText(
                    "predicted-class",
                    "Prediction unavailable"
                );

                setText(
                    "prediction-confidence",
                    "—"
                );

                document.getElementById(
                    "probability-list"
                ).textContent =
                    "No prediction available.";
            }

            const existingReview =
                data.doctor_review;

            const reviewFormContainer =
                document.getElementById(
                    "doctor-review-form-container"
                );

            const existingReviewContainer =
                document.getElementById(
                    "existing-doctor-review"
                );


            if (existingReview) {

                if (reviewFormContainer) {
                    reviewFormContainer.style.display =
                        "none";
                }

                if (existingReviewContainer) {

                    existingReviewContainer.innerHTML = `
            <div class="review-summary">

                <h3>Clinical Review Completed</h3>

                <p>
                    <strong>Reviewed by:</strong>
                    Dr. ${existingReview.doctor_name}
                </p>

                <p>
                    <strong>Reviewed at:</strong>
                    ${formatDate(
                        existingReview.reviewed_at
                    )}
                </p>

                <div class="review-notes">

                    <strong>Clinical Notes</strong>

                    <p>
                        ${existingReview.review_notes}
                    </p>

                </div>

                <div class="review-status">
                    Clinical review completed
                </div>

            </div>
        `;

                    existingReviewContainer.style.display =
                        "block";
                }

            } else {

                if (reviewFormContainer) {
                    reviewFormContainer.style.display =
                        "block";
                }

                if (existingReviewContainer) {
                    existingReviewContainer.style.display =
                        "none";
                }
            }


            loadingElement.style.display =
                "none";

            contentElement.style.display =
                "block";

        } catch (error) {

            console.error(
                "Case loading error:",
                error
            );

            loadingElement.style.display =
                "none";

            showMessage(
                `Unable to load case: ${error.message}`,
                true
            );
        }
    }


    reviewForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            const reviewNotes =
                document.getElementById(
                    "review-notes"
                ).value.trim();


            if (!reviewNotes) {

                showMessage(
                    "Please enter clinical review notes.",
                    true
                );

                return;
            }


            reviewButton.disabled =
                true;

            reviewButton.textContent =
                "Saving Review...";


            try {

                await apiRequest(
                    `/doctors/cases/${caseId}/review/`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify({
                            retinal_image:
                                Number(caseId),

                            review_notes:
                                reviewNotes,
                        }),
                    }
                );


                showMessage(
                    "Clinical review saved successfully."
                );


                reviewForm.reset();


            } catch (error) {

                console.error(
                    "Review save error:",
                    error
                );

                showMessage(
                    `Unable to save review: ${error.message}`,
                    true
                );


            } finally {

                reviewButton.disabled =
                    false;

                reviewButton.textContent =
                    "Save Clinical Review";
            }
        }
    );


    await loadCase();

});