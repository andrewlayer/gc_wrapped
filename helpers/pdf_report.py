from pathlib import Path
from typing import List
from PIL import Image
import re
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as ReportLabImage,
    PageBreak,
)


class ReportContent:
    def __init__(self, content: str | Path, title: str, description: str):
        self.content = content
        self.title = title
        self.description = description


def create_pdf_report(output_path: str, contents: List[ReportContent]) -> None:
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Create custom style for descriptions
    styles.add(
        ParagraphStyle(
            name="Description",
            parent=styles["BodyText"],
            spaceBefore=12,
            spaceAfter=12,
            leading=16,
        )
    )

    for content in contents:
        # Add title
        title = Paragraph(content.title, styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Add image
        img_path = Path(content.content)
        if not img_path.exists():
            raise FileNotFoundError(f"Image not found: {img_path}")
        img = ReportLabImage(str(img_path), width=400, height=300)
        elements.append(img)
        elements.append(Spacer(1, 12))

        # Add description
        if content.description:
            html_description = markdown2.markdown(content.description)
            description = Paragraph(html_description, styles["Description"])
            elements.append(description)
            elements.append(Spacer(1, 12))

        elements.append(PageBreak())

    doc.build(elements)
    print(f"PDF report saved to {output_path}")
