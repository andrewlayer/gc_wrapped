import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_pdf_report(output_path, figures_with_titles):
    """
    Creates a multi-page PDF using a list of (figure, title).
    Each figure is saved as one page in the PDF.
    """
    with PdfPages(output_path) as pdf:
        for fig, title in figures_with_titles:
            fig.suptitle(title, fontsize=14)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
    print(f"PDF report saved to {output_path}") 