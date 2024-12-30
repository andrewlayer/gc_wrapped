import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
from PIL import Image
from typing import List


class ReportContent:
    def __init__(self, content: str | Path, title: str, description: str):
        self.content = content
        self.title = title
        self.description = description


def create_pdf_report(output_path: str, contents: List[ReportContent]) -> None:
    with PdfPages(output_path) as pdf:
        for content in contents:
            # Create wrapper figure
            wrapper_fig = plt.figure(figsize=(8.5, 11))
            gs = wrapper_fig.add_gridspec(3, 1, height_ratios=[0.5, 4, 1], hspace=0.3)

            # Add title
            title_ax = wrapper_fig.add_subplot(gs[0])
            title_ax.axis("off")
            title_ax.text(
                0.5,
                0.5,
                content.title,
                horizontalalignment="center",
                fontsize=14,
                transform=title_ax.transAxes,
            )

            # Add image
            content_ax = wrapper_fig.add_subplot(gs[1])
            img_path = Path(content.content)
            if not img_path.exists():
                raise FileNotFoundError(f"Image not found: {img_path}")
            img = Image.open(img_path)
            content_ax.imshow(img)
            content_ax.axis("off")

            # Add description
            desc_ax = wrapper_fig.add_subplot(gs[2])
            desc_ax.axis("off")
            if content.description:
                desc_ax.text(
                    0.05,
                    0.8,
                    content.description,
                    wrap=True,
                    va="top",
                    fontsize=10,
                    transform=desc_ax.transAxes,
                )

            pdf.savefig(wrapper_fig, bbox_inches="tight")
            plt.close(wrapper_fig)

    print(f"PDF report saved to {output_path}")
