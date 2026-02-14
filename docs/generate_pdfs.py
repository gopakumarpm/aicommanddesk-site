"""
AICommandDesk.com - Professional PDF Generator
Converts all markdown strategy documents to branded PDFs.
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from datetime import datetime

# ─── Brand Colors ───
NAVY_DARK = HexColor('#1a1a2e')
ELECTRIC = HexColor('#4361ee')
ELECTRIC_DARK = HexColor('#1b3bdb')
ELECTRIC_LIGHT = HexColor('#eef0fd')
TEXT_DARK = HexColor('#1B1B1B')
TEXT_GRAY = HexColor('#4A4A4A')
TEXT_LIGHT = HexColor('#6B7280')
WHITE = HexColor('#FFFFFF')
PALE_BLUE = HexColor('#EEF2FF')
BORDER_GRAY = HexColor('#D1D5DB')

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 0.75 * inch
MARGIN_RIGHT = 0.75 * inch
MARGIN_TOP = 0.9 * inch
MARGIN_BOTTOM = 0.85 * inch
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='DocTitle', fontName='Helvetica-Bold', fontSize=24,
        textColor=NAVY_DARK, spaceAfter=6, alignment=TA_LEFT, leading=30,
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle', fontName='Helvetica', fontSize=14,
        textColor=TEXT_GRAY, spaceAfter=4, alignment=TA_LEFT, leading=18,
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader', fontName='Helvetica-Bold', fontSize=16,
        textColor=NAVY_DARK, spaceBefore=18, spaceAfter=8, leading=20,
    ))
    styles.add(ParagraphStyle(
        name='SubHeader', fontName='Helvetica-Bold', fontSize=13,
        textColor=ELECTRIC_DARK, spaceBefore=14, spaceAfter=6, leading=17,
    ))
    styles.add(ParagraphStyle(
        name='SubSubHeader', fontName='Helvetica-Bold', fontSize=11,
        textColor=HexColor('#2d3748'), spaceBefore=10, spaceAfter=4, leading=14,
    ))
    styles.add(ParagraphStyle(
        name='H4Header', fontName='Helvetica-Bold', fontSize=10,
        textColor=HexColor('#374151'), spaceBefore=8, spaceAfter=3, leading=13,
    ))
    styles.add(ParagraphStyle(
        name='BodyJustified', fontName='Helvetica', fontSize=9.5,
        textColor=TEXT_DARK, spaceBefore=2, spaceAfter=5, leading=13,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name='BulletText', fontName='Helvetica', fontSize=9.5,
        textColor=TEXT_DARK, spaceBefore=1, spaceAfter=2, leading=13,
        leftIndent=18, bulletIndent=8,
    ))
    styles.add(ParagraphStyle(
        name='SubBulletText', fontName='Helvetica', fontSize=9,
        textColor=TEXT_GRAY, spaceBefore=1, spaceAfter=1, leading=12,
        leftIndent=36, bulletIndent=26,
    ))
    styles.add(ParagraphStyle(
        name='CodeBlock', fontName='Courier', fontSize=8,
        textColor=HexColor('#1f2937'), spaceBefore=4, spaceAfter=6, leading=11,
        leftIndent=12, backColor=HexColor('#f3f4f6'),
    ))
    styles.add(ParagraphStyle(
        name='CaptionText', fontName='Helvetica-Oblique', fontSize=8,
        textColor=TEXT_LIGHT, spaceBefore=2, spaceAfter=6, alignment=TA_LEFT,
    ))
    return styles


def get_table_style():
    return TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_DARK),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BACKGROUND', (0, 0), (-1, 0), ELECTRIC),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
    ])


def draw_cover(c_obj, doc, title, subtitle, date_str):
    c_obj.saveState()
    w, h = A4

    # Dark navy header block (top 45%)
    c_obj.setFillColor(NAVY_DARK)
    c_obj.rect(0, h * 0.52, w, h * 0.48, fill=True, stroke=False)

    # Electric blue accent line
    c_obj.setStrokeColor(ELECTRIC)
    c_obj.setLineWidth(4)
    c_obj.line(MARGIN_LEFT, h * 0.52, w - MARGIN_RIGHT, h * 0.52)

    # Brand mark
    c_obj.setFillColor(ELECTRIC)
    c_obj.setFont('Helvetica-Bold', 14)
    c_obj.drawString(MARGIN_LEFT, h * 0.88, "AICommandDesk.com")

    c_obj.setFillColor(HexColor('#94a3b8'))
    c_obj.setFont('Helvetica', 10)
    c_obj.drawString(MARGIN_LEFT, h * 0.855, "AI Productivity for Managers & Professionals")

    # Title (wrap manually)
    c_obj.setFillColor(WHITE)
    c_obj.setFont('Helvetica-Bold', 26)
    max_w = w - 2 * MARGIN_LEFT
    words = title.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if c_obj.stringWidth(test, 'Helvetica-Bold', 26) < max_w:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)

    y = h * 0.72
    for line in lines:
        c_obj.drawString(MARGIN_LEFT, y, line)
        y -= 36

    # Subtitle
    if subtitle:
        c_obj.setFillColor(HexColor('#93c5fd'))
        c_obj.setFont('Helvetica', 13)
        c_obj.drawString(MARGIN_LEFT, y - 8, subtitle)

    # Date and info below accent line
    c_obj.setFillColor(TEXT_GRAY)
    c_obj.setFont('Helvetica', 10)
    c_obj.drawString(MARGIN_LEFT, h * 0.42, f"Date: {date_str}")
    c_obj.drawString(MARGIN_LEFT, h * 0.39, "Prepared for: Founder, AICommandDesk.com")
    c_obj.drawString(MARGIN_LEFT, h * 0.36, "Classification: Confidential - Internal Use")

    # Bottom decoration
    c_obj.setFillColor(ELECTRIC)
    c_obj.rect(0, 0, w, 8, fill=True, stroke=False)

    c_obj.restoreState()


def header_footer(c_obj, doc, doc_title):
    c_obj.saveState()
    w, h = A4

    # Header line
    c_obj.setStrokeColor(ELECTRIC)
    c_obj.setLineWidth(1)
    c_obj.line(MARGIN_LEFT, h - 0.55 * inch, w - MARGIN_RIGHT, h - 0.55 * inch)

    # Header text
    c_obj.setFillColor(TEXT_GRAY)
    c_obj.setFont('Helvetica', 7)
    c_obj.drawString(MARGIN_LEFT, h - 0.48 * inch, doc_title)

    c_obj.setFillColor(ELECTRIC)
    c_obj.setFont('Helvetica-Bold', 7)
    c_obj.drawRightString(w - MARGIN_RIGHT, h - 0.48 * inch, "AICommandDesk.com")

    # Footer line
    c_obj.setStrokeColor(BORDER_GRAY)
    c_obj.setLineWidth(0.5)
    c_obj.line(MARGIN_LEFT, 0.6 * inch, w - MARGIN_RIGHT, 0.6 * inch)

    # Page number
    c_obj.setFillColor(TEXT_GRAY)
    c_obj.setFont('Helvetica', 8)
    c_obj.drawCentredString(w / 2, 0.4 * inch, f"Page {doc.page}")

    # Footer left
    c_obj.setFont('Helvetica', 7)
    c_obj.drawString(MARGIN_LEFT, 0.4 * inch, "Confidential - AICommandDesk.com")

    c_obj.restoreState()


def clean_text(text):
    """Clean markdown formatting from text for PDF."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier" size="8" color="#4361ee">\1</font>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = text.replace('&', '&amp;')
    text = re.sub(r'&amp;(amp;|lt;|gt;|quot;|apos;|#\d+;)', r'&\1', text)
    text = text.replace('<b>', '<b>').replace('</b>', '</b>')
    text = text.replace('<i>', '<i>').replace('</i>', '</i>')
    text = re.sub(r'&amp;(lt|gt|amp|quot);', r'&\1;', text)
    return text


def parse_markdown_table(lines):
    """Parse markdown table lines into list of lists."""
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and not re.match(r'^\|[\s\-\|:]+\|$', line):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells:
                rows.append(cells)
    return rows


def parse_markdown(md_text):
    """Parse markdown into structured elements."""
    elements = []
    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    table_lines = []

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                elements.append({'type': 'code', 'text': '\n'.join(code_lines)})
                code_lines = []
                in_code_block = False
            else:
                # Flush table
                if table_lines:
                    rows = parse_markdown_table(table_lines)
                    if rows:
                        elements.append({'type': 'table', 'rows': rows})
                    table_lines = []
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Table lines
        if line.strip().startswith('|'):
            table_lines.append(line)
            i += 1
            continue
        elif table_lines:
            rows = parse_markdown_table(table_lines)
            if rows:
                elements.append({'type': 'table', 'rows': rows})
            table_lines = []

        stripped = line.strip()

        # Headings
        if stripped.startswith('#### '):
            elements.append({'type': 'h4', 'text': stripped[5:]})
        elif stripped.startswith('### '):
            elements.append({'type': 'h3', 'text': stripped[4:]})
        elif stripped.startswith('## '):
            elements.append({'type': 'h2', 'text': stripped[3:]})
        elif stripped.startswith('# '):
            elements.append({'type': 'h1', 'text': stripped[2:]})
        elif stripped.startswith('---'):
            elements.append({'type': 'hr'})
        elif stripped.startswith('- [ ] ') or stripped.startswith('- [x] '):
            checkbox = "[ ]" if "[ ]" in stripped else "[x]"
            text = stripped.split('] ', 1)[1] if '] ' in stripped else stripped[6:]
            elements.append({'type': 'bullet', 'text': f"{checkbox} {text}", 'level': 0})
        elif stripped.startswith('- '):
            elements.append({'type': 'bullet', 'text': stripped[2:], 'level': 0})
        elif stripped.startswith('  - ') or stripped.startswith('   - '):
            elements.append({'type': 'bullet', 'text': stripped.strip()[2:], 'level': 1})
        elif re.match(r'^\d+\.\s', stripped):
            text = re.sub(r'^\d+\.\s', '', stripped)
            elements.append({'type': 'numbered', 'text': text})
        elif stripped == '':
            elements.append({'type': 'spacer'})
        else:
            elements.append({'type': 'paragraph', 'text': stripped})

        i += 1

    # Flush remaining table
    if table_lines:
        rows = parse_markdown_table(table_lines)
        if rows:
            elements.append({'type': 'table', 'rows': rows})

    return elements


def build_pdf_elements(parsed, styles):
    """Convert parsed markdown elements to ReportLab flowables."""
    flowables = []
    counter = 0

    for elem in parsed:
        t = elem['type']

        if t == 'h1':
            text = clean_text(elem['text'])
            if text.startswith('TABLE OF CONTENTS') or text.startswith('AICommandDesk'):
                flowables.append(Paragraph(text, styles['SectionHeader']))
            else:
                flowables.append(PageBreak())
                flowables.append(Paragraph(text, styles['SectionHeader']))
                flowables.append(HRFlowable(width="100%", thickness=1.5, color=ELECTRIC,
                                            spaceBefore=2, spaceAfter=8))

        elif t == 'h2':
            text = clean_text(elem['text'])
            flowables.append(Paragraph(text, styles['SubHeader']))

        elif t == 'h3':
            text = clean_text(elem['text'])
            flowables.append(Paragraph(text, styles['SubSubHeader']))

        elif t == 'h4':
            text = clean_text(elem['text'])
            flowables.append(Paragraph(text, styles['H4Header']))

        elif t == 'paragraph':
            text = clean_text(elem['text'])
            if text:
                flowables.append(Paragraph(text, styles['BodyJustified']))

        elif t == 'bullet':
            text = clean_text(elem['text'])
            level = elem.get('level', 0)
            bullet_char = '\u2022' if level == 0 else '\u25E6'
            style = styles['BulletText'] if level == 0 else styles['SubBulletText']
            flowables.append(Paragraph(f"{bullet_char}  {text}", style))

        elif t == 'numbered':
            counter += 1
            text = clean_text(elem['text'])
            flowables.append(Paragraph(f"{counter}.  {text}", styles['BulletText']))

        elif t == 'code':
            code_text = elem['text'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            code_lines = code_text.split('\n')
            for cl in code_lines[:30]:  # Limit code block length
                flowables.append(Paragraph(cl if cl.strip() else '&nbsp;', styles['CodeBlock']))

        elif t == 'table':
            rows = elem['rows']
            if len(rows) < 2:
                continue

            # Clean cell text
            clean_rows = []
            for row in rows:
                clean_row = []
                for cell in row:
                    cell_text = clean_text(cell)
                    clean_row.append(Paragraph(cell_text, ParagraphStyle(
                        'TableCell', fontName='Helvetica', fontSize=8,
                        textColor=TEXT_DARK, leading=10, alignment=TA_LEFT,
                    )))
                clean_rows.append(clean_row)

            # Make header cells bold
            if clean_rows:
                header_row = []
                for cell in rows[0]:
                    cell_text = clean_text(cell)
                    header_row.append(Paragraph(f"<b>{cell_text}</b>", ParagraphStyle(
                        'TableHeader', fontName='Helvetica-Bold', fontSize=8,
                        textColor=WHITE, leading=10, alignment=TA_CENTER,
                    )))
                clean_rows[0] = header_row

            # Calculate column widths
            num_cols = max(len(r) for r in clean_rows)
            col_width = CONTENT_WIDTH / num_cols
            col_widths = [col_width] * num_cols

            try:
                table = Table(clean_rows, colWidths=col_widths, repeatRows=1)
                table.setStyle(get_table_style())
                flowables.append(Spacer(1, 4))
                flowables.append(table)
                flowables.append(Spacer(1, 8))
            except Exception:
                pass

        elif t == 'hr':
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY,
                                        spaceBefore=6, spaceAfter=6))

        elif t == 'spacer':
            flowables.append(Spacer(1, 3))

        # Reset counter on non-numbered items
        if t != 'numbered':
            counter = 0

    return flowables


def generate_pdf(md_path, pdf_path, title, subtitle):
    """Generate a single PDF from a markdown file."""
    print(f"  Generating: {os.path.basename(pdf_path)}")

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Remove the first heading (we use it in the cover page)
    lines = md_text.split('\n')
    filtered_lines = []
    skip_first_h1 = True
    for line in lines:
        if skip_first_h1 and line.strip().startswith('# '):
            skip_first_h1 = False
            continue
        filtered_lines.append(line)
    md_text = '\n'.join(filtered_lines)

    parsed = parse_markdown(md_text)
    styles = get_styles()
    flowables = build_pdf_elements(parsed, styles)

    date_str = datetime.now().strftime('%B %Y')

    def on_first_page(c_obj, doc):
        draw_cover(c_obj, doc, title, subtitle, date_str)

    def on_later_pages(c_obj, doc):
        header_footer(c_obj, doc, title)

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=MARGIN_LEFT, rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
    )

    # Add a page break after cover (first page is blank body for cover)
    all_flowables = [PageBreak()] + flowables

    doc.build(all_flowables, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"  Done: {pdf_path}")


def main():
    docs_dir = os.path.dirname(os.path.abspath(__file__))

    documents = [
        {
            'md': '01-Business-Monetisation-Plan.md',
            'pdf': '01-Business-Monetisation-Plan.pdf',
            'title': 'Business Development & Monetisation Plan',
            'subtitle': 'AICommandDesk.com - Strategic Growth Roadmap',
        },
        {
            'md': '02-Content-Calendar-SEO-Strategy.md',
            'pdf': '02-Content-Calendar-SEO-Strategy.pdf',
            'title': '90-Day Content Calendar & SEO Strategy',
            'subtitle': 'AICommandDesk.com - Content & Search Playbook',
        },
        {
            'md': '03-Traffic-Generation-Playbook.md',
            'pdf': '03-Traffic-Generation-Playbook.pdf',
            'title': 'Traffic Generation Playbook',
            'subtitle': 'AICommandDesk.com - Multi-Channel Growth Strategy',
        },
        {
            'md': '04-Technical-Deployment-Guide.md',
            'pdf': '04-Technical-Deployment-Guide.pdf',
            'title': 'Technical Deployment Guide',
            'subtitle': 'AICommandDesk.com - GitHub + Netlify Setup',
        },
        {
            'md': '05-Affiliate-Revenue-Playbook.md',
            'pdf': '05-Affiliate-Revenue-Playbook.pdf',
            'title': 'Affiliate & Revenue Playbook',
            'subtitle': 'AICommandDesk.com - Monetisation Deep Dive',
        },
    ]

    print("=" * 60)
    print("AICommandDesk.com - PDF Generation")
    print("=" * 60)

    for doc_info in documents:
        md_path = os.path.join(docs_dir, doc_info['md'])
        pdf_path = os.path.join(docs_dir, doc_info['pdf'])

        if not os.path.exists(md_path):
            print(f"  SKIP: {doc_info['md']} not found")
            continue

        try:
            generate_pdf(md_path, pdf_path, doc_info['title'], doc_info['subtitle'])
        except Exception as e:
            print(f"  ERROR generating {doc_info['pdf']}: {e}")

    print("=" * 60)
    print("All PDFs generated!")
    print("=" * 60)


if __name__ == '__main__':
    main()
