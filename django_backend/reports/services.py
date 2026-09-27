from .models import MedicalReport
from io import BytesIO

from django.core.files.base import ContentFile

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def generate_medical_report(retinal_image, doctor=None):

    prediction = getattr(
        retinal_image,
        "prediction",
        None,
    )

    doctor_review = getattr(
        retinal_image,
        "doctor_review",
        None,
    )

    if not prediction:
        raise ValueError(
            "AI prediction is required before generating a report."
        )

    clinical_summary = (
        f"The AI model classified this retinal image as "
        f"{prediction.predicted_class} with a confidence of "
        f"{prediction.confidence:.1%}."
    )

    doctor_notes = ""

    if doctor_review:
        doctor_notes = doctor_review.review_notes

    recommendation = (
        "Clinical correlation and routine ophthalmic "
        "follow-up are recommended."
    )

    if doctor_review and doctor_review.review_notes:
        clinical_summary += (
            " The AI assessment was reviewed by a doctor."
        )

    report, created = MedicalReport.objects.update_or_create(
        retinal_image=retinal_image,
        defaults={
            "generated_by": (
                doctor.user
                if doctor
                else None
            ),
            "ai_prediction": prediction.predicted_class,
            "ai_confidence": prediction.confidence,
            "clinical_summary": clinical_summary,
            "doctor_notes": doctor_notes,
            "recommendation": recommendation,
        },
    )

    return report, created




def generate_medical_report_pdf(report):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Diabetic Retinopathy Assessment Report",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Case ID:</b> "
            f"{report.retinal_image.id}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Patient:</b> "
            f"{report.retinal_image.patient.user.username}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>AI Assessment</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Prediction:</b> "
            f"{report.ai_prediction}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> "
            f"{report.ai_confidence:.1%}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Clinical Summary</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            report.clinical_summary or "—",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Doctor's Clinical Notes</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            report.doctor_notes or "—",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            report.recommendation or "—",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{report.generated_at.strftime('%d %B %Y, %H:%M')}",
            styles["Normal"],
        )
    )

    document.build(story)

    buffer.seek(0)

    return ContentFile(
        buffer.read(),
        name=(
            f"medical_report_case_"
            f"{report.retinal_image.id}.pdf"
        ),
    )