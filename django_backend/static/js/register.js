document.addEventListener("DOMContentLoaded", () => {

const registerForm =
    document.getElementById("register-form");

const patientRole =
    document.getElementById("patientRole");

const doctorRole =
    document.getElementById("doctorRole");

const roleSlider =
    document.getElementById("roleSlider");

const patientForm =
    document.getElementById("patientForm");

const doctorForm =
    document.getElementById("doctorForm");

const formTitle =
    document.getElementById("formTitle");

const formSubtitle =
    document.getElementById("formSubtitle");

const errorElement =
    document.getElementById("register-error");

const registerButton =
    document.getElementById("register-btn");

const terms =
    document.getElementById("terms");


if (!registerForm) {
    return;
}


let selectedRole = "patient";


/* =========================
   ROLE SWITCHING
========================= */

function switchRole(role) {

    selectedRole = role;

    errorElement.style.display = "none";
    errorElement.textContent = "";


    if (role === "patient") {

        roleSlider.classList.remove("doctor");

        patientRole.classList.add("active");
        doctorRole.classList.remove("active");

        patientForm.style.display = "block";
        doctorForm.style.display = "none";

        formTitle.textContent =
            "Create Patient Account";

        formSubtitle.textContent =
            "Register to access your diabetic eye screening";

    } else {

        roleSlider.classList.add("doctor");

        doctorRole.classList.add("active");
        patientRole.classList.remove("active");

        patientForm.style.display = "none";
        doctorForm.style.display = "block";

        formTitle.textContent =
            "Create Doctor Account";

        formSubtitle.textContent =
            "Register as a medical professional";
    }
}


patientRole.addEventListener(
    "click",
    () => switchRole("patient")
);


doctorRole.addEventListener(
    "click",
    () => switchRole("doctor")
);


/* =========================
   PASSWORD VISIBILITY
========================= */

const passwordToggles =
    document.querySelectorAll(".password-toggle");


passwordToggles.forEach((toggle) => {

    toggle.addEventListener("click", function () {

        const inputId =
            this.dataset.target;

        const password =
            document.getElementById(inputId);


        if (password.type === "password") {

            password.type = "text";

            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");

        } else {

            password.type = "password";

            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        }

    });

});


/* =========================
   HELPERS
========================= */

function showError(message, elementId) {

    errorElement.textContent = message;
    errorElement.style.display = "block";

    const element =
        document.getElementById(elementId);

    if (element) {
        element.focus();
    }
}


function isValidEmail(email) {

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return emailPattern.test(email);
}


function splitFullName(fullName) {

    const parts =
        fullName.trim().split(/\s+/);

    const firstName =
        parts.shift() || "";

    const lastName =
        parts.join(" ");

    return {
        first_name: firstName,
        last_name: lastName
    };
}


/* =========================
   REGISTRATION
========================= */

registerForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        errorElement.style.display = "none";
        errorElement.textContent = "";


        /* TERMS */

        if (!terms.checked) {

            showError(
                "Please agree to the Terms of Service and Privacy Policy.",
                "terms"
            );

            return;
        }


        let fullName;
        let email;
        let password;
        let confirmPassword;


        /* =========================
           PATIENT VALIDATION
        ========================= */

        if (selectedRole === "patient") {

            fullName =
                document
                    .getElementById("patientFullName")
                    .value
                    .trim();

            email =
                document
                    .getElementById("patientEmail")
                    .value
                    .trim();

            password =
                document
                    .getElementById("patientPassword")
                    .value;

            confirmPassword =
                document
                    .getElementById("patientConfirmPassword")
                    .value;


            if (fullName === "") {

                showError(
                    "Please enter your Full Name.",
                    "patientFullName"
                );

                return;
            }


            if (email === "") {

                showError(
                    "Please enter your Email Address.",
                    "patientEmail"
                );

                return;
            }


            if (!isValidEmail(email)) {

                showError(
                    "Please enter a valid Email Address.",
                    "patientEmail"
                );

                return;
            }


            if (password === "") {

                showError(
                    "Please enter your Password.",
                    "patientPassword"
                );

                return;
            }


            if (password.length < 8) {

                showError(
                    "Password must be at least 8 characters.",
                    "patientPassword"
                );

                return;
            }


            if (confirmPassword === "") {

                showError(
                    "Please confirm your Password.",
                    "patientConfirmPassword"
                );

                return;
            }


            if (password !== confirmPassword) {

                showError(
                    "Passwords do not match.",
                    "patientConfirmPassword"
                );

                return;
            }

const dateOfBirth =
    document
        .getElementById("patientDob")
        .value;

const gender =
    document
        .getElementById("patientGender")
        .value;


if (dateOfBirth === "") {

    showError(
        "Please enter your Date of Birth.",
        "patientDob"
    );

    return;
}


if (gender === "") {

    showError(
        "Please select your Gender.",
        "patientGender"
    );

    return;
}

        }


        /* =========================
           DOCTOR VALIDATION
        ========================= */

        else {

            fullName =
                document
                    .getElementById("doctorFullName")
                    .value
                    .trim();

            email =
                document
                    .getElementById("doctorEmail")
                    .value
                    .trim();

            password =
                document
                    .getElementById("doctorPassword")
                    .value;

            confirmPassword =
                document
                    .getElementById("doctorConfirmPassword")
                    .value;


            const registrationNumber =
                document
                    .getElementById("registrationNumber")
                    .value
                    .trim();

            const medicalCouncil =
                document
                    .getElementById("medicalCouncil")
                    .value;

            const qualification =
                document
                    .getElementById("qualification")
                    .value;

            const specialization =
                document
                    .getElementById("specialization")
                    .value;


            if (fullName === "") {

                showError(
                    "Please enter your Full Name.",
                    "doctorFullName"
                );

                return;
            }


            if (email === "") {

                showError(
                    "Please enter your Email Address.",
                    "doctorEmail"
                );

                return;
            }


            if (!isValidEmail(email)) {

                showError(
                    "Please enter a valid Email Address.",
                    "doctorEmail"
                );

                return;
            }


            if (registrationNumber === "") {

                showError(
                    "Please enter your Medical Registration Number.",
                    "registrationNumber"
                );

                return;
            }


            if (medicalCouncil === "") {

                showError(
                    "Please select your Medical Council.",
                    "medicalCouncil"
                );

                return;
            }


            if (qualification === "") {

                showError(
                    "Please select your Qualification.",
                    "qualification"
                );

                return;
            }


            if (specialization === "") {

                showError(
                    "Please select your Specialization.",
                    "specialization"
                );

                return;
            }


            if (password === "") {

                showError(
                    "Please enter your Password.",
                    "doctorPassword"
                );

                return;
            }


            if (password.length < 8) {

                showError(
                    "Password must be at least 8 characters.",
                    "doctorPassword"
                );

                return;
            }


            if (confirmPassword === "") {

                showError(
                    "Please confirm your Password.",
                    "doctorConfirmPassword"
                );

                return;
            }


            if (password !== confirmPassword) {

                showError(
                    "Passwords do not match.",
                    "doctorConfirmPassword"
                );

                return;
            }


            /* =========================
               DOCTOR API DATA
            ========================= */

        }


        /* =========================
           SPLIT FULL NAME
        ========================= */

        const name =
            splitFullName(fullName);


        /* =========================
           API PAYLOAD
        ========================= */

        const payload = {

            first_name:
                name.first_name,

            last_name:
                name.last_name,

            username:
                email,

            email:
                email,

            password:
                password,

            role:
                selectedRole === "patient"
                    ? "PATIENT"
                    : "DOCTOR"
        };

        /* PATIENT FIELDS */

if (selectedRole === "patient") {

    payload.date_of_birth =
        document
            .getElementById("patientDob")
            .value;

    payload.gender =
        document
            .getElementById("patientGender")
            .value;
}

        /* DOCTOR FIELDS */

        if (selectedRole === "doctor") {

            payload.medical_registration_number =
                document
                    .getElementById("registrationNumber")
                    .value
                    .trim();

            payload.medical_council =
                document
                    .getElementById("medicalCouncil")
                    .value;

            payload.qualification =
                document
                    .getElementById("qualification")
                    .value;

            payload.specialization =
                document
                    .getElementById("specialization")
                    .value;
        }


        /* =========================
           API REQUEST
        ========================= */

        registerButton.disabled = true;

        registerButton.textContent =
            "Creating Account...";


        try {

            const response =
                await fetch(
                    "/api/accounts/register/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                let message =
                    data?.detail ||
                    data?.error ||
                    "Registration failed.";


                if (data?.doctor_verification) {

                    message =
                        Array.isArray(
                            data.doctor_verification
                        )
                            ? data.doctor_verification[0]
                            : data.doctor_verification;
                }


                throw new Error(message);
            }


            if (selectedRole === "doctor") {

                alert(
                    "Registration successful. Your doctor account is pending administrator verification."
                );

            } else {

                alert(
                    "Registration successful."
                );
            }


            window.location.href =
                "/login/";


        } catch (error) {

            errorElement.textContent =
                error.message;

            errorElement.style.display =
                "block";


        } finally {

            registerButton.disabled =
                false;

            registerButton.textContent =
                "Create Account";
        }

    }
);


});
