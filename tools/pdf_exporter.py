"""
PDF Exporter - Export des rapports en PDF
"""

from typing import Optional
from loguru import logger

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
except ImportError:
    logger.warning("⚠ ReportLab non installé, PDF export désactivé")


def markdown_to_pdf(markdown_content: str, output_path: str, title: str = "Report") -> Optional[str]:
    """
    Convertit un contenu Markdown en PDF.
    
    Args:
        markdown_content: Contenu en Markdown
        output_path: Chemin du fichier PDF de sortie
        title: Titre du rapport
    
    Returns:
        Chemin du fichier généré ou None
    """
    logger.info(f"Conversion PDF: {output_path}")
    
    try:
        # Crée le document PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title=title
        )
        
        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="CustomHeading",
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor("#1f1f1f"),
            spaceAfter=12,
            alignment=1  # Center
        ))
        
        # Contenu
        story = []
        
        # Parse simple du Markdown (amélioration future: utiliser un vrai parser)
        lines = markdown_content.split("\n")
        current_paragraph = []
        
        for line in lines:
            if line.startswith("# "):
                if current_paragraph:
                    story.append(Paragraph(" ".join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Paragraph(line[2:], styles['CustomHeading']))
                story.append(Spacer(1, 0.2*inch))
            
            elif line.startswith("## "):
                if current_paragraph:
                    story.append(Paragraph(" ".join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Paragraph(line[3:], styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
            
            elif line.startswith("### "):
                if current_paragraph:
                    story.append(Paragraph(" ".join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Paragraph(line[4:], styles['Heading3']))
                story.append(Spacer(1, 0.05*inch))
            
            elif line.strip() == "":
                if current_paragraph:
                    story.append(Paragraph(" ".join(current_paragraph), styles['Normal']))
                    story.append(Spacer(1, 0.05*inch))
                    current_paragraph = []
            
            else:
                current_paragraph.append(line)
        
        if current_paragraph:
            story.append(Paragraph(" ".join(current_paragraph), styles['Normal']))
        
        # Build PDF
        doc.build(story)
        logger.success(f"✓ PDF généré: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Erreur lors de la génération PDF: {e}")
        return None


def export_report(markdown_path: str, pdf_path: str, title: str = "Research Report") -> Optional[str]:
    """
    Exporte un fichier Markdown en PDF.
    
    Args:
        markdown_path: Chemin du fichier Markdown
        pdf_path: Chemin de sortie du PDF
        title: Titre du rapport
    
    Returns:
        Chemin du PDF ou None
    """
    logger.info(f"Export rapport: {markdown_path} → {pdf_path}")
    
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return markdown_to_pdf(content, pdf_path, title)
    
    except Exception as e:
        logger.error(f"Erreur lors de l'export: {e}")
        return None


if __name__ == "__main__":
    # Test
    sample_md = """# Sample Report

## Introduction

This is a test report.

## Section 1

Some content here.

### Subsection

More details.

## Conclusion

Summary.
"""
    
    output = markdown_to_pdf(sample_md, "test_report.pdf", "Test Report")
    if output:
        print(f"✅ PDF créé: {output}")
