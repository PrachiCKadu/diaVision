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

    const reviewFormContainer =
        document.getElementById(
            "doctor-review-form-container"
        );

    const existingReviewContainer =
        document.getElementById(
            "existing-doctor-review"
        );

    const editReviewContainer =
        document.getElementById(
            "doctor-review-edit-container"
        );

    const editReviewForm =
        document.getElementById(
            "doctor-review-edit-form"
        );

    const editReviewNotes =
        document.getElementById(
            "edit-review-notes"
        );

    const updateReviewButton =
        document.getElementById(
            "review-update-btn"
        );

    const cancelEditButton =
        document.getElementById(
            "review-cancel-btn"
        );


    let currentReview = null;


    if (!caseId) {
        showMessage(
            "Invalid retinal case.",
            true
        );
        return;
    }


    function showMessage(
        message,
        isError = false
    ) {

        if (!messageElement) {
            return;
        }

        messageElement.textContent =
            message;

        messageElement.style.display =
            "block";

        if (isError) {
            messageElement.classList.add(
                "error"
            );
        } else {
            messageElement.classList.remove(
                "error"
            );
        }
    }


    function hideMessage() {

        if (!messageElement) {
            return;
        }

        messageElement.style.display =
            "none";
    }


    function formatPercentage(value) {

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


    function formatDate(value) {

        if (!value) {
            return "—";
        }

        return new Date(value)
            .toLocaleString();
    }


async function loadMedicalReport() {

    const reportContainer =
        document.getElementById("medical-report-container");

    const reportNotAvailable =
        document.getElementById("report-not-available");

    const reportStatus =
        document.getElementById("report-status");

    const reportMessage =
        document.getElementById("report-message");


    try {

        const report =
            await apiRequest(
                `/reports/${caseId}/`
            );


        setText(
            "report-title",
            report.report_title
        );

        setText(
            "report-ai-prediction",
            report.ai_prediction
        );

        setText(
            "report-ai-confidence",
            formatPercentage(
                report.ai_confidence
            )
        );

        setText(
            "report-generated-at",
            formatDate(
                report.generated_at
            )
        );

        setText(
            "report-clinical-summary",
            report.clinical_summary
        );

        setText(
            "report-doctor-notes",
            report.doctor_notes
        );

        setText(
            "report-recommendation",
            report.recommendation
        );


        if (reportContainer) {
            reportContainer.style.display =
                "block";
        }

        if (reportNotAvailable) {
            reportNotAvailable.style.display =
                "none";
        }

        if (reportStatus) {
            reportStatus.textContent =
                "Generated";
        }

//         const downloadReportButton =
//     document.getElementById(
//         "download-report-btn"
//     );

// if (downloadReportButton) {

//     downloadReportButton.style.display =
//         "inline-block";

//     downloadReportButton.onclick = async () => {

//         try {

//             downloadReportButton.disabled =
//                 true;

//             downloadReportButton.textContent =
//                 "Preparing PDF...";

//             const response =
//                 await fetch(
//                     `/api/reports/${caseId}/pdf/`,
//                     {
//                         method: "GET",

//                         headers: {
//                             Authorization:
//                                 `Bearer ${localStorage.getItem("access_token")}`,
//                         },
//                     }
//                 );

//             if (!response.ok) {
//                 throw new Error(
//                     "Unable to generate medical report PDF."
//                 );
//             }

//             const blob =
//                 await response.blob();

//             const url =
//                 window.URL.createObjectURL(blob);

//             const link =
//                 document.createElement("a");

//             link.href = url;

//             link.download =
//                 `medical_report_case_${caseId}.pdf`;

//             document.body.appendChild(link);

//             link.click();

//             link.remove();

//             window.URL.revokeObjectURL(url);

//         } catch (error) {

//             console.error(
//                 "PDF download error:",
//                 error
//             );

//             showMessage(
//                 `Unable to download report: ${error.message}`,
//                 true
//             );

//         } finally {

//             downloadReportButton.disabled =
//                 false;

//             downloadReportButton.textContent =
//                 "Download Medical Report (PDF)";
//         }
//     };
// }


    } catch (error) {

        console.error(
            "Medical report loading error:",
            error
        );


        if (reportContainer) {
            reportContainer.style.display =
                "none";
        }

        if (reportNotAvailable) {
            reportNotAvailable.style.display =
                "block";
        }

        if (reportStatus) {
            reportStatus.textContent =
                "Not Available";
        }

    }
}

const downloadReportButton =
    document.getElementById(
        "download-report-btn"
    );

if (downloadReportButton) {

    downloadReportButton.style.display =
        "inline-block";

    downloadReportButton.onclick =
        async () => {

            try {

                downloadReportButton.disabled =
                    true;

                downloadReportButton.textContent =
                    "Preparing PDF...";


                const token =
                    localStorage.getItem(
                        "access_token"
                    );


                if (!token) {
                    throw new Error(
                        "Authentication required."
                    );
                }


                const response =
                    await fetch(
                        `/api/reports/${caseId}/pdf/`,
                        {
                            method: "GET",

                            headers: {
                                Authorization:
                                    `Bearer ${token}`,
                            },
                        }
                    );


                if (
                    response.status === 401
                ) {

                    throw new Error(
                        "Your session has expired. Please login again."
                    );
                }


                if (!response.ok) {
                    throw new Error(
                        "Unable to generate medical report PDF."
                    );
                }


                const blob =
                    await response.blob();


                const url =
                    window.URL.createObjectURL(
                        blob
                    );


                const link =
                    document.createElement("a");

                link.href = url;

                link.download =
                    `medical_report_case_${caseId}.pdf`;

                document.body.appendChild(
                    link
                );

                link.click();

                link.remove();

                window.URL.revokeObjectURL(
                    url
                );


            } catch (error) {

                console.error(
                    "PDF download error:",
                    error
                );

                showMessage(
                    `Unable to download report: ${error.message}`,
                    true
                );


            } finally {

                downloadReportButton.disabled =
                    false;

                downloadReportButton.textContent =
                    "Download Medical Report (PDF)";
            }
        };
}

    function setText(id, value) {

        const element =
            document.getElementById(id);

        if (element) {
            element.textContent =
                value ?? "—";
        }
    }


    function renderProbabilities(
        prediction
    ) {

        const container =
            document.getElementById(
                "probability-list"
            );

        if (!container) {
            return;
        }

        const probabilities = [
            {
                label: "No DR",
                value:
                    prediction.no_dr_probability,
            },
            {
                label: "Mild DR",
                value:
                    prediction.mild_probability,
            },
            {
                label: "Moderate DR",
                value:
                    prediction.moderate_probability,
            },
            {
                label: "Severe DR",
                value:
                    prediction.severe_probability,
            },
            {
                label: "Proliferative DR",
                value:
                    prediction
                        .proliferative_dr_probability,
            },
        ];

        container.innerHTML = "";

        probabilities.forEach(
            (item) => {

                const row =
                    document.createElement(
                        "div"
                    );

                row.className =
                    "probability-row";

                row.innerHTML = `
                    <div class="probability-header">
                        <span>${item.label}</span>

                        <strong>
                            ${formatPercentage(
                                item.value
                            )}
                        </strong>
                    </div>

                    <div class="probability-bar">
                        <div
                            class="probability-fill"
                            style="width: ${
                                Number(
                                    item.value || 0
                                ) * 100
                            }%"
                        ></div>
                    </div>
                `;

                container.appendChild(row);
            }
        );
    }


    function renderReview(
        review
    ) {

        currentReview =
            review || null;


        if (!review) {

            if (existingReviewContainer) {
                existingReviewContainer.innerHTML =
                    "";

                existingReviewContainer.style.display =
                    "none";
            }

            if (editReviewContainer) {
                editReviewContainer.style.display =
                    "none";
            }

            if (reviewFormContainer) {
                reviewFormContainer.style.display =
                    "block";
            }

            return;
        }


        if (reviewFormContainer) {
            reviewFormContainer.style.display =
                "none";
        }

        if (editReviewContainer) {
            editReviewContainer.style.display =
                "none";
        }


        if (existingReviewContainer) {

            existingReviewContainer.innerHTML = `
                <div class="review-summary">

                    <h3>
                        Clinical Review Completed
                    </h3>

                    <p>
                        <strong>Reviewed by:</strong>
                        Dr. ${review.doctor_name}
                    </p>

                    <p>
                        <strong>Reviewed at:</strong>
                        ${formatDate(
                            review.reviewed_at
                        )}
                    </p>

                    <div class="review-notes">

                        <strong>
                            Clinical Notes
                        </strong>

                        <p>
                            ${review.review_notes}
                        </p>

                    </div>

                    <div class="review-status">
                        Clinical review completed
                    </div>

                    <div class="review-actions">

                        <button
                            type="button"
                            id="edit-review-btn"
                            class="auth-button"
                        >
                            Edit Review
                        </button>

                        <button
                            type="button"
                            id="delete-review-btn"
                            class="dashboard-button"
                        >
                            Delete Review
                        </button>

                    </div>

                </div>
            `;

            existingReviewContainer.style.display =
                "block";


            const editButton =
                document.getElementById(
                    "edit-review-btn"
                );

            const deleteButton =
                document.getElementById(
                    "delete-review-btn"
                );


            if (editButton) {

                editButton.addEventListener(
                    "click",
                    openEditReview
                );
            }


            if (deleteButton) {

                deleteButton.addEventListener(
                    "click",
                    deleteReview
                );
            }
        }
    }


    function openEditReview() {

        if (!currentReview) {
            return;
        }

        if (editReviewNotes) {

            editReviewNotes.value =
                currentReview.review_notes || "";
        }

        if (existingReviewContainer) {
            existingReviewContainer.style.display =
                "none";
        }

        if (editReviewContainer) {
            editReviewContainer.style.display =
                "block";
        }

        hideMessage();
    }


    function cancelEditReview() {

        if (editReviewContainer) {
            editReviewContainer.style.display =
                "none";
        }

        if (currentReview) {

            if (existingReviewContainer) {
                existingReviewContainer.style.display =
                    "block";
            }

        } else {

            if (reviewFormContainer) {
                reviewFormContainer.style.display =
                    "block";
            }
        }

        hideMessage();
    }


    async function updateReview(
        event
    ) {

        event.preventDefault();


        const reviewNotes =
            editReviewNotes
                ?.value
                .trim();


        if (!reviewNotes) {

            showMessage(
                "Please enter clinical review notes.",
                true
            );

            return;
        }


        if (!currentReview) {
            return;
        }


        updateReviewButton.disabled =
            true;

        updateReviewButton.textContent =
            "Saving Changes...";


        try {

            const updatedReview =
                await apiRequest(
                    `/doctors/cases/${caseId}/review/detail/`,
                    {
                        method: "PATCH",

                        headers: {
                            "Content-Type":
                                "application/json",
                        },

                        body: JSON.stringify({
                            review_notes:
                                reviewNotes,
                        }),
                    }
                );


            renderReview(
    updatedReview
);

await loadMedicalReport();

showMessage(
    "Clinical review updated successfully."
);


        } catch (error) {

            console.error(
                "Review update error:",
                error
            );

            showMessage(
                `Unable to update review: ${error.message}`,
                true
            );

        } finally {

            updateReviewButton.disabled =
                false;

            updateReviewButton.textContent =
                "Save Changes";
        }
    }


    async function deleteReview() {

        if (!currentReview) {
            return;
        }


        const confirmed =
            window.confirm(
                "Are you sure you want to delete this clinical review?"
            );


        if (!confirmed) {
            return;
        }


        const deleteButton =
            document.getElementById(
                "delete-review-btn"
            );


        if (deleteButton) {

            deleteButton.disabled =
                true;

            deleteButton.textContent =
                "Deleting...";
        }


        try {

            await apiRequest(
                `/doctors/cases/${caseId}/review/detail/`,
                {
                    method: "DELETE",
                }
            );


            currentReview = null;

            renderReview(null);


            if (reviewForm) {
                reviewForm.reset();
            }


            showMessage(
                "Clinical review deleted successfully."
            );


        } catch (error) {

            console.error(
                "Review delete error:",
                error
            );

            showMessage(
                `Unable to delete review: ${error.message}`,
                true
            );


            if (deleteButton) {

                deleteButton.disabled =
                    false;

                deleteButton.textContent =
                    "Delete Review";
            }
        }
    }


    async function loadCase() {

        try {

            const data =
                await apiRequest(
                    `/doctors/cases/${caseId}/`
                );


            const prediction =
                data.prediction;


            document.getElementById(
                "case-title"
            ).textContent =
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
                data.patient_gender ||
                    "Not provided"
            );

            setText(
                "diabetes-duration",
                data.diabetes_duration_years !==
                    null &&
                data.diabetes_duration_years !==
                    undefined
                    ? `${data.diabetes_duration_years} years`
                    : "Not provided"
            );


            const retinalImage =
                document.getElementById(
                    "retinal-image"
                );

            if (retinalImage) {
                retinalImage.src =
                    data.image;
            }


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

                    gradcamImage.style.display =
                        "block";

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


            renderReview(
                data.doctor_review
            );


            if (loadingElement) {
                loadingElement.style.display =
                    "none";
            }

            if (contentElement) {
                contentElement.style.display =
                    "block";
            }


        } catch (error) {

            console.error(
                "Case loading error:",
                error
            );


            if (loadingElement) {
                loadingElement.style.display =
                    "none";
            }


            showMessage(
                `Unable to load case: ${error.message}`,
                true
            );
        }
    }


    /*
     * CREATE REVIEW
     */

    if (reviewForm) {

        reviewForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                const reviewNotes =
                    document.getElementById(
                        "review-notes"
                    )
                    .value
                    .trim();


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

                    const createdReview =
                        await apiRequest(
                            `/doctors/cases/${caseId}/review/`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json",
                                },

                                body:
                                    JSON.stringify({
                                        retinal_image:
                                            Number(
                                                caseId
                                            ),

                                        review_notes:
                                            reviewNotes,
                                    }),
                            }
                        );


                   renderReview(
    createdReview
);

reviewForm.reset();

await loadMedicalReport();

showMessage(
    "Clinical review saved successfully."
);


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
    }


    /*
     * UPDATE REVIEW
     */

    if (editReviewForm) {

        editReviewForm.addEventListener(
            "submit",
            updateReview
        );
    }


    /*
     * CANCEL EDIT
     */

    if (cancelEditButton) {

        cancelEditButton.addEventListener(
            "click",
            cancelEditReview
        );
    }


await loadCase();
await loadMedicalReport();

});