(async () => {
    "use strict";

    /* =========================================================
       ELEMENTS
    ========================================================= */

    const pendingDoctorsContainer =
        document.getElementById("pending-doctors-container");

    const pendingDoctorCount =
        document.getElementById("pending-doctor-count");

    const doctorVerificationMessage =
        document.getElementById("doctor-verification-message");

    const statisticsStatus =
        document.getElementById("statistics-status");

    const statisticsMessage =
        document.getElementById("admin-statistics-message");

    const userManagementMessage =
        document.getElementById("user-management-message");

    const patientManagementCount =
        document.getElementById("patient-management-count");

    const doctorManagementCount =
        document.getElementById("doctor-management-count");

    const patientsManagementContainer =
        document.getElementById("patients-management-container");

    const doctorsManagementContainer =
        document.getElementById("doctors-management-container");


    /* =========================================================
       AUTHENTICATION
    ========================================================= */

    function getAccessToken() {
        return localStorage.getItem("access_token");
    }


    /* =========================================================
       HTML ESCAPE
    ========================================================= */

    function escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = value ?? "";
        return div.innerHTML;
    }


    /* =========================================================
       MESSAGES
    ========================================================= */

    function showMessage(element, message, type = "error") {

        if (!element) {
            return;
        }

        element.textContent = message;
        element.className = `form-message ${type}`;
        element.style.display = "block";
    }


    function hideMessage(element) {

        if (!element) {
            return;
        }

        element.style.display = "none";
    }


    /* =========================================================
       CURRENT ADMIN
    ========================================================= */

    async function loadCurrentUser() {

        const token = getAccessToken();

        if (!token) {
            return;
        }

        try {

            const response = await fetch(
                "/api/accounts/me/",
                {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to load admin profile."
                );
            }

            const username =
                data?.user?.username || "Admin";

            const welcomeElement =
                document.getElementById("admin-welcome");

            if (welcomeElement) {
                welcomeElement.textContent =
                    `Welcome, ${username}.`;
            }

        } catch (error) {

            console.error(
                "Current user loading error:",
                error
            );
        }
    }


    /* =========================================================
       STATISTICS
    ========================================================= */

    function setStatistic(id, value) {

        const element =
            document.getElementById(id);

        if (element) {
            element.textContent =
                value ?? "0";
        }
    }


    async function loadStatistics() {

        const token = getAccessToken();

        if (!token) {

            if (statisticsStatus) {
                statisticsStatus.textContent =
                    "Authentication Required";
            }

            showMessage(
                statisticsMessage,
                "Please login again.",
                "error"
            );

            return;
        }

        try {

            if (statisticsStatus) {
                statisticsStatus.textContent =
                    "Loading...";
            }

            const response = await fetch(
                "/api/accounts/admin/statistics/",
                {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to load system statistics."
                );
            }

            setStatistic(
                "stat-users",
                data.users
            );

            setStatistic(
                "stat-patients",
                data.patients
            );

            setStatistic(
                "stat-doctors",
                data.doctors
            );

            setStatistic(
                "stat-pending-doctors",
                data.pending_doctors
            );

            setStatistic(
                "stat-approved-doctors",
                data.approved_doctors
            );

            setStatistic(
                "stat-retinal-cases",
                data.retinal_cases
            );

            setStatistic(
                "stat-predictions",
                data.predictions
            );

            setStatistic(
                "stat-medical-reports",
                data.medical_reports
            );

            if (statisticsStatus) {
                statisticsStatus.textContent = "Live";
            }

            hideMessage(statisticsMessage);

        } catch (error) {

            console.error(
                "Statistics loading error:",
                error
            );

            if (statisticsStatus) {
                statisticsStatus.textContent = "Error";
            }

            showMessage(
                statisticsMessage,
                error.message,
                "error"
            );
        }
    }


    /* =========================================================
       DOCTOR VERIFICATION
       PENDING ONLY
    ========================================================= */
function renderPendingDoctors(doctors) {

    if (pendingDoctorCount) {
        pendingDoctorCount.textContent =
            `${doctors.length} Pending`;
    }

    if (!pendingDoctorsContainer) {
        return;
    }

    if (!doctors.length) {

        pendingDoctorsContainer.innerHTML = `
            <tr>
                <td
                    colspan="8"
                    class="text-center py-4 text-muted"
                >
                    No pending doctor verification requests.
                </td>
            </tr>
        `;

        return;
    }


    pendingDoctorsContainer.innerHTML =
        doctors.map((doctor) => {

            const fullName =
                `${doctor.first_name || ""} ${doctor.last_name || ""}`
                    .trim();

            return `
                <tr>

                    <!-- Doctor -->
                    <td>
                        <strong>
                            Dr. ${escapeHtml(
                                fullName || doctor.username
                            )}
                        </strong>

                        <div class="small text-muted">
                            @${escapeHtml(
                                doctor.username
                            )}
                        </div>
                    </td>


                    <!-- Email -->
                    <td>
                        ${escapeHtml(
                            doctor.email || "—"
                        )}
                    </td>


                    <!-- Registration Number -->
                    <td>
                        ${escapeHtml(
                            doctor.medical_registration_number ||
                            doctor.license_number ||
                            "Not provided"
                        )}
                    </td>


                    <!-- Medical Council -->
                    <td>
                        ${escapeHtml(
                            doctor.medical_council ||
                            "Not provided"
                        )}
                    </td>


                    <!-- Qualification -->
                    <td>
                        ${escapeHtml(
                            doctor.qualification ||
                            "Not provided"
                        )}
                    </td>


                    <!-- Specialization -->
                    <td>
                        ${escapeHtml(
                            doctor.specialization ||
                            "Not provided"
                        )}
                    </td>


                    <!-- Status -->
                    <td>
                        <span class="badge text-bg-warning">
                            PENDING
                        </span>
                    </td>


                    <!-- Actions -->
                    <td class="text-end">

                        <div
                            class="d-flex justify-content-end gap-2"
                        >

                            <!-- View -->
                            <button
                                type="button"
                                class="btn btn-outline-primary btn-sm view-pending-doctor"
                                data-doctor-id="${doctor.id}"
                            >
                                View
                            </button>


                            <!-- Approve -->
                            <button
                                type="button"
                                class="btn btn-success btn-sm approve-doctor"
                                data-doctor-id="${doctor.id}"
                            >
                                Approve
                            </button>


                            <!-- Reject -->
                            <button
                                type="button"
                                class="btn btn-outline-danger btn-sm reject-doctor"
                                data-doctor-id="${doctor.id}"
                            >
                                Reject
                            </button>

                        </div>

                    </td>

                </tr>
            `;

        }).join("");


    attachVerificationHandlers();
}

    async function loadPendingDoctors() {

        const token = getAccessToken();

        if (!token) {

            if (pendingDoctorsContainer) {
                pendingDoctorsContainer.innerHTML = `
                    <tr>
                        <td
                            colspan="8"
                            class="text-center py-4 text-danger"
                        >
                            Authentication required. Please login again.
                        </td>
                    </tr>
                `;
            }

            return;
        }


        try {

            const response = await fetch(
                "/api/accounts/admin/doctors/pending/",
                {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );


            const data = await response.json();


            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to load pending doctors."
                );
            }


            /*
             * API may return either:
             *
             * [
             *   {...}
             * ]
             *
             * OR
             *
             * {
             *   value: [...]
             * }
             */

            const doctors =
                Array.isArray(data)
                    ? data
                    : data?.value || [];


            renderPendingDoctors(doctors);


        } catch (error) {

            console.error(
                "Pending doctor loading error:",
                error
            );


            if (pendingDoctorsContainer) {

                pendingDoctorsContainer.innerHTML = `
                    <tr>
                        <td
                            colspan="8"
                            class="text-center py-4 text-danger"
                        >
                            Unable to load pending doctors.
                            <div class="small mt-1">
                                ${escapeHtml(error.message)}
                            </div>
                        </td>
                    </tr>
                `;
            }


            if (pendingDoctorCount) {
                pendingDoctorCount.textContent = "Error";
            }
        }
    }


    /* =========================================================
       APPROVE / REJECT
    ========================================================= */
function attachVerificationHandlers() {

    /* =========================================================
       VIEW PENDING DOCTOR
    ========================================================= */

    document
        .querySelectorAll(".view-pending-doctor")
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    viewDoctor(
                        button.dataset.doctorId
                    );

                }
            );

        });


    /* =========================================================
       APPROVE DOCTOR
    ========================================================= */

    document
        .querySelectorAll(".approve-doctor")
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    updateDoctorStatus(
                        button.dataset.doctorId,
                        "APPROVED"
                    );

                }
            );

        });


    /* =========================================================
       REJECT DOCTOR
    ========================================================= */

    document
        .querySelectorAll(".reject-doctor")
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    updateDoctorStatus(
                        button.dataset.doctorId,
                        "REJECTED"
                    );

                }
            );

        });
}

    async function updateDoctorStatus(
        doctorId,
        status
    ) {

        const token = getAccessToken();

        if (!token) {

            showMessage(
                doctorVerificationMessage,
                "Authentication required.",
                "error"
            );

            return;
        }


        const action =
            status === "APPROVED"
                ? "approve"
                : "reject";


        const confirmed =
            window.confirm(
                `Are you sure you want to ${action} this doctor?`
            );


        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `/api/accounts/admin/doctors/${doctorId}/verification/`,
                {
                    method: "PATCH",

                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        status: status
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    data?.non_field_errors?.[0] ||
                    "Unable to update doctor status."
                );
            }


            showMessage(
                doctorVerificationMessage,
                data.message ||
                "Doctor verification status updated successfully.",
                "success"
            );


            /*
             * Refresh:
             *
             * 1. Pending verification table
             * 2. Statistics
             * 3. Approved doctor management table
             */

            await Promise.all([
                loadPendingDoctors(),
                loadStatistics(),
                loadUserManagement()
            ]);


        } catch (error) {

            console.error(
                "Doctor verification error:",
                error
            );


            showMessage(
                doctorVerificationMessage,
                error.message,
                "error"
            );
        }
    }


    /* =========================================================
       USER MANAGEMENT
       PATIENTS + APPROVED DOCTORS
    ========================================================= */

    function renderPatients(patients) {

        if (patientManagementCount) {
            patientManagementCount.textContent =
                `${patients.length} Patients`;
        }


        if (!patientsManagementContainer) {
            return;
        }


        if (!patients.length) {

            patientsManagementContainer.innerHTML = `
                <tr>
                    <td
                        colspan="6"
                        class="text-center py-4 text-muted"
                    >
                        No registered patients.
                    </td>
                </tr>
            `;

            return;
        }


        patientsManagementContainer.innerHTML =
            patients.map((patient) => {

                const fullName =
                    `${patient.first_name || ""} ${patient.last_name || ""}`
                        .trim();


                return `
                    <tr>

                        <td>

                            <strong>
                                ${escapeHtml(
                                    fullName ||
                                    patient.username
                                )}
                            </strong>

                            <div class="small text-muted">
                                @${escapeHtml(
                                    patient.username
                                )}
                            </div>

                        </td>


                        <td>
                            ${escapeHtml(
                                patient.email
                            )}
                        </td>


                        <td>
                            ${patient.age ?? "—"}
                        </td>


                        <td>
                            ${escapeHtml(
                                patient.gender || "—"
                            )}
                        </td>


                        <td>
                            <span class="badge text-bg-primary">
                                ${patient.retinal_cases ?? 0}
                            </span>
                        </td>


                        <td class="text-end">

                            <button
                                type="button"
                                class="btn btn-outline-danger btn-sm delete-patient"
                                data-patient-id="${patient.id}"
                                data-username="${escapeHtml(
                                    patient.username
                                )}"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>
                `;

            }).join("");


        attachUserManagementHandlers();
    }


    function renderManagedDoctors(doctors) {

        /*
         * IMPORTANT:
         *
         * User Management should show ONLY APPROVED doctors.
         */

        const approvedDoctors =
            doctors.filter(
                (doctor) =>
                    doctor.verification_status === "APPROVED" ||
                    doctor.doctor_verification_status === "APPROVED"
            );


        if (doctorManagementCount) {
            doctorManagementCount.textContent =
                `${approvedDoctors.length} Doctors`;
        }


        if (!doctorsManagementContainer) {
            return;
        }


        if (!approvedDoctors.length) {

            doctorsManagementContainer.innerHTML = `
                <tr>
                    <td
                        colspan="7"
                        class="text-center py-4 text-muted"
                    >
                        No approved doctors found.
                    </td>
                </tr>
            `;

            return;
        }


        doctorsManagementContainer.innerHTML =
            approvedDoctors.map((doctor) => {

                const fullName =
                    `${doctor.first_name || ""} ${doctor.last_name || ""}`
                        .trim();


                return `
                    <tr>

                        <td>

                            <strong>
                                Dr. ${escapeHtml(
                                    fullName ||
                                    doctor.username
                                )}
                            </strong>

                            <div class="small text-muted">
                                @${escapeHtml(
                                    doctor.username
                                )}
                            </div>

                        </td>


                        <td>
                            ${escapeHtml(
                                doctor.email
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                doctor.specialization ||
                                "—"
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                doctor.hospital_clinic ||
                                "—"
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                doctor.license_number ||
                                doctor.medical_registration_number ||
                                "—"
                            )}
                        </td>


                        <td>
                            <span class="badge text-bg-success">
                                APPROVED
                            </span>
                        </td>


                        <td class="text-end">

                            <div
                                class="d-flex justify-content-end gap-2"
                            >

                                <button
                                    type="button"
                                    class="btn btn-outline-primary btn-sm view-doctor"
                                    data-doctor-id="${doctor.id}"
                                >
                                    View
                                </button>


                                <button
                                    type="button"
                                    class="btn btn-outline-danger btn-sm delete-doctor"
                                    data-doctor-id="${doctor.id}"
                                    data-username="${escapeHtml(
                                        doctor.username
                                    )}"
                                >
                                    Delete
                                </button>

                            </div>

                        </td>

                    </tr>
                `;

            }).join("");


        attachUserManagementHandlers();
    }


    /* =========================================================
       LOAD USERS
    ========================================================= */

    async function loadUserManagement() {

        const token = getAccessToken();

        if (!token) {

            showMessage(
                userManagementMessage,
                "Authentication required. Please login again.",
                "error"
            );

            return;
        }


        try {

            if (patientManagementCount) {
                patientManagementCount.textContent =
                    "Loading...";
            }

            if (doctorManagementCount) {
                doctorManagementCount.textContent =
                    "Loading...";
            }


            const response = await fetch(
                "/api/accounts/admin/users/",
                {
                    method: "GET",

                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            );


            const data = await response.json();


            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to load users."
                );
            }


            renderPatients(
                data.patients || []
            );


            renderManagedDoctors(
                data.doctors || []
            );


            hideMessage(userManagementMessage);


        } catch (error) {

            console.error(
                "User management loading error:",
                error
            );


            showMessage(
                userManagementMessage,
                error.message,
                "error"
            );


            if (patientManagementCount) {
                patientManagementCount.textContent =
                    "Error";
            }


            if (doctorManagementCount) {
                doctorManagementCount.textContent =
                    "Error";
            }
        }
    }


    /* =========================================================
       USER MANAGEMENT BUTTONS
    ========================================================= */

    function attachUserManagementHandlers() {

        document
            .querySelectorAll(".delete-patient")
            .forEach((button) => {

                button.addEventListener(
                    "click",
                    () => {

                        deletePatient(
                            button.dataset.patientId,
                            button.dataset.username
                        );

                    }
                );

            });


        document
            .querySelectorAll(".delete-doctor")
            .forEach((button) => {

                button.addEventListener(
                    "click",
                    () => {

                        deleteDoctor(
                            button.dataset.doctorId,
                            button.dataset.username
                        );

                    }
                );

            });


        document
            .querySelectorAll(".view-doctor")
            .forEach((button) => {

                button.addEventListener(
                    "click",
                    () => {

                        viewDoctor(
                            button.dataset.doctorId
                        );

                    }
                );

            });
    }


    /* =========================================================
       DELETE PATIENT
    ========================================================= */

    async function deletePatient(
        patientId,
        username
    ) {

        const token = getAccessToken();

        if (!token) {

            showMessage(
                userManagementMessage,
                "Authentication required.",
                "error"
            );

            return;
        }


        const confirmed =
            window.confirm(
                `Are you sure you want to permanently delete patient "${username}"?`
            );


        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `/api/accounts/admin/patients/${patientId}/delete/`,
                {
                    method: "DELETE",

                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            const data = await response.json();


            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to delete patient."
                );
            }


            showMessage(
                userManagementMessage,
                data.message ||
                "Patient deleted successfully.",
                "success"
            );


            await Promise.all([
                loadUserManagement(),
                loadStatistics()
            ]);


        } catch (error) {

            console.error(
                "Patient deletion error:",
                error
            );


            showMessage(
                userManagementMessage,
                error.message,
                "error"
            );
        }
    }


    /* =========================================================
       DELETE DOCTOR
    ========================================================= */

    async function deleteDoctor(
        doctorId,
        username
    ) {

        const token = getAccessToken();

        if (!token) {

            showMessage(
                userManagementMessage,
                "Authentication required.",
                "error"
            );

            return;
        }


        const confirmed =
            window.confirm(
                `Are you sure you want to permanently delete doctor "${username}"?`
            );


        if (!confirmed) {
            return;
        }


        try {

            const response = await fetch(
                `/api/accounts/admin/doctors/${doctorId}/delete/`,
                {
                    method: "DELETE",

                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );


            const data = await response.json();


            if (!response.ok) {
                throw new Error(
                    data?.detail ||
                    data?.error ||
                    "Unable to delete doctor."
                );
            }


            showMessage(
                userManagementMessage,
                data.message ||
                "Doctor deleted successfully.",
                "success"
            );


            await Promise.all([
                loadUserManagement(),
                loadStatistics()
            ]);


        } catch (error) {

            console.error(
                "Doctor deletion error:",
                error
            );


            showMessage(
                userManagementMessage,
                error.message,
                "error"
            );
        }
    }


    /* =========================================================
       VIEW DOCTOR
    ========================================================= */
async function viewDoctor(doctorId) {

    const token = getAccessToken();

    if (!token) {

        showMessage(
            userManagementMessage,
            "Authentication required. Please login again.",
            "error"
        );

        return;
    }


    /* =====================================================
       MODAL ELEMENTS
    ===================================================== */

    const modalElement =
        document.getElementById("doctorDetailsModal");

    const loadingElement =
        document.getElementById("doctor-details-loading");

    const contentElement =
        document.getElementById("doctor-details-content");

    const errorElement =
        document.getElementById("doctor-details-error");


    if (!modalElement) {

        console.error(
            "Doctor details modal was not found."
        );

        return;
    }


    /* =====================================================
       RESET MODAL
    ===================================================== */

    if (loadingElement) {
        loadingElement.style.display = "block";
    }

    if (contentElement) {
        contentElement.style.display = "none";
    }

    if (errorElement) {
        errorElement.style.display = "none";
        errorElement.textContent = "";
    }


    /* =====================================================
       SHOW MODAL
    ===================================================== */

    const modal =
        bootstrap.Modal.getOrCreateInstance(
            modalElement
        );

    modal.show();


    try {

        /* =================================================
           FETCH DOCTOR DETAILS
        ================================================= */

        const response = await fetch(
            `/api/accounts/admin/doctors/${doctorId}/`,
            {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            }
        );


        const data = await response.json();


        /* =================================================
           API ERROR
        ================================================= */

        if (!response.ok) {

            throw new Error(
                data?.detail ||
                data?.error ||
                "Unable to load doctor details."
            );
        }


        /* =================================================
           RESPONSE
           
           Backend returns doctor directly:
           
           {
               id,
               username,
               email,
               ...
           }
        ================================================= */

        const doctor =
            data?.doctor || data;


        if (!doctor || !doctor.id) {

            throw new Error(
                "Invalid doctor details received from server."
            );
        }


        /* =================================================
           BASIC INFORMATION
        ================================================= */

        const fullName =
            `${doctor.first_name || ""} ${doctor.last_name || ""}`
                .trim();


        const nameElement =
            document.getElementById(
                "doctor-detail-name"
            );

        const usernameElement =
            document.getElementById(
                "doctor-detail-username"
            );

        const emailElement =
            document.getElementById(
                "doctor-detail-email"
            );

        const statusElement =
            document.getElementById(
                "doctor-detail-status"
            );


        if (nameElement) {

            nameElement.textContent =
                fullName
                    ? `Dr. ${fullName}`
                    : "—";
        }


        if (usernameElement) {

            usernameElement.textContent =
                doctor.username || "—";
        }


        if (emailElement) {

            emailElement.textContent =
                doctor.email || "—";
        }


        if (statusElement) {

            const status =
                doctor.verification_status ||
                doctor.doctor_verification_status ||
                "—";

            statusElement.innerHTML =
                status === "APPROVED"
                    ? `<span class="badge text-bg-success">APPROVED</span>`
                    : `<span class="badge text-bg-secondary">${escapeHtml(status)}</span>`;
        }


        /* =================================================
           PROFESSIONAL INFORMATION
        ================================================= */

        const qualificationElement =
            document.getElementById(
                "doctor-detail-qualification"
            );

        const specializationElement =
            document.getElementById(
                "doctor-detail-specialization"
            );

        const councilElement =
            document.getElementById(
                "doctor-detail-council"
            );

        const registrationElement =
            document.getElementById(
                "doctor-detail-registration"
            );

        const hospitalElement =
            document.getElementById(
                "doctor-detail-hospital"
            );

        const licenseElement =
            document.getElementById(
                "doctor-detail-license"
            );


        if (qualificationElement) {

            qualificationElement.textContent =
                doctor.qualification || "—";
        }


        if (specializationElement) {

            specializationElement.textContent =
                doctor.specialization || "—";
        }


        if (councilElement) {

            councilElement.textContent =
                doctor.medical_council || "—";
        }


        if (registrationElement) {

            registrationElement.textContent =
                doctor.medical_registration_number || "—";
        }


        if (hospitalElement) {

            hospitalElement.textContent =
                doctor.hospital_clinic || "—";
        }


        if (licenseElement) {

            licenseElement.textContent =
                doctor.license_number || "—";
        }


        /* =================================================
           MODAL SUBTITLE
        ================================================= */

        const subtitleElement =
            document.getElementById(
                "doctor-details-subtitle"
            );

       if (subtitleElement) {

    const status =
        doctor.verification_status ||
        doctor.doctor_verification_status ||
        "";

    if (status === "APPROVED") {

        subtitleElement.textContent =
            doctor.specialization
                ? `${doctor.specialization} • Verified Medical Professional`
                : "Verified Medical Professional";

    } else if (status === "PENDING") {

        subtitleElement.textContent =
            doctor.specialization
                ? `${doctor.specialization} • Verification Pending`
                : "Verification Pending";

    } else if (status === "REJECTED") {

        subtitleElement.textContent =
            doctor.specialization
                ? `${doctor.specialization} • Verification Rejected`
                : "Verification Rejected";

    } else {

        subtitleElement.textContent =
            "Medical Professional Profile";
    }
}


        /* =================================================
           SHOW CONTENT
        ================================================= */

        if (loadingElement) {
            loadingElement.style.display = "none";
        }

        if (contentElement) {
            contentElement.style.display = "block";
        }


    } catch (error) {

        console.error(
            "Doctor detail loading error:",
            error
        );


        if (loadingElement) {
            loadingElement.style.display = "none";
        }

        if (contentElement) {
            contentElement.style.display = "none";
        }

        if (errorElement) {

            errorElement.textContent =
                error.message ||
                "Unable to load doctor details.";

            errorElement.style.display =
                "block";
        }
    }
}

    /* =========================================================
       INITIAL LOAD
    ========================================================= */

    await Promise.all([
        loadStatistics(),
        loadPendingDoctors(),
        loadCurrentUser(),
        loadUserManagement()
    ]);

})();