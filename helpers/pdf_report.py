from dataclasses import dataclass
from typing import Union, List
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image


@dataclass
class ReportContent:
    """Content for a single page in the PDF report"""

    content: Union[plt.Figure, Path, str]  # Figure or path to image
    title: str
    description: str = ""  # Optional description


def create_pdf_report(output_path: str, contents: List[ReportContent]) -> None:
    with PdfPages(output_path) as pdf:
        for content in contents:
            # Create figure with more space for description
            fig = plt.figure(figsize=(8.5, 11))

            # Add title at top
            fig.suptitle(content.title, fontsize=14, y=0.95)

            # Create subplot that leaves room for description
            gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.3)

            # Plot content in top subplot
            ax_plot = fig.add_subplot(gs[0])
            if isinstance(content.content, plt.Figure):
                temp_fig = content.content
                for ax_orig in temp_fig.axes:
                    for line in ax_orig.lines:
                        ax_plot.plot(*line.get_data(), label=line.get_label())
                    ax_plot.set_xlabel(ax_orig.get_xlabel())
                    ax_plot.set_ylabel(ax_orig.get_ylabel())
                    if ax_orig.get_legend():
                        ax_plot.legend()
            else:
                img_path = Path(content.content)
                if not img_path.exists():
                    raise FileNotFoundError(f"Image not found: {img_path}")
                img = Image.open(img_path)
                ax_plot.imshow(img)
                ax_plot.axis("off")

            # Add description in bottom subplot
            ax_text = fig.add_subplot(gs[1])
            ax_text.axis("off")
            if content.description:
                ax_text.text(
                    0.05,
                    0.8,
                    content.description,
                    wrap=True,
                    va="top",
                    fontsize=10,
                    transform=ax_text.transAxes,
                )

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
            if isinstance(content.content, plt.Figure):
                plt.close(content.content)

    print(f"PDF report saved to {output_path}")
