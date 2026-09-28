"""Editable resume source. Requires reportlab and Noto Sans Regular/Bold.

Run: python3 resume/build_resume.py
Optionally set RESUME_FONT_DIR to a directory containing NotoSans-*.ttf.
Output: output/pdf/Jan-Dranreb-Balangue-Resume.pdf
"""
from pathlib import Path
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(os.environ.get('RESUME_FONT_DIR', str(
    Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype'
)))
for name, file in [('Noto', 'NotoSans-Regular.ttf'), ('NotoBold', 'NotoSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
pdfmetrics.registerFont(TTFont('BulletFont', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFontFamily('Noto', normal='Noto', bold='NotoBold', italic='Noto', boldItalic='NotoBold')
OUTPUT = ROOT / 'output/pdf/Jan-Dranreb-Balangue-Resume.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUTPUT), pagesize=(612, 792))
c.setTitle('Jan Dranreb R. Balangue - Software Developer Resume')
c.setAuthor('Jan Dranreb R. Balangue')
body = ParagraphStyle('body', fontName='Noto', fontSize=11, leading=13.5)


def para(text, x, top, width, size=11, leading=13.5):
    style = ParagraphStyle('text', parent=body, fontSize=size, leading=leading)
    text = text.replace('◦', '<font name="BulletFont">◦</font>')
    p = Paragraph(text, style)
    _, height = p.wrap(width, 792)
    assert top + height <= 750, f'Text exceeds page bounds: {text}'
    p.drawOn(c, x, 792 - top - height)
    return top + height


def center(text, top, size, font='Noto', gray=0):
    c.setFillGray(gray)
    c.setFont(font, size)
    c.drawCentredString(306, 792-top-size, text)
    c.setFillGray(0)


def heading(text, x, top):
    return para(f'<b>{text}</b>', x, top, 500, 12, 15)


def experience(company, role, dates, bullets, top):
    top = para(f'• <b><u>{company}</u></b> - {role} <font color="#808080">( {dates} )</font>', 57, top, 498)
    for bullet in bullets:
        top = para('◦ ' + bullet, 95, top + 1, 460)
    return top + 12


center('JAN DRANREB R. BALANGUE', 60, 18, 'NotoBold')
center('Software Developer', 92, 16, gray=.6)
para('<u>jandranrebbalangue@gmail.com</u>', 155, 121, 220, 12, 15)
para('<u>09366482101</u>', 356, 121, 125, 12, 15)
para('<font color="#808080">Email</font>', 237, 138, 60)
para('<font color="#808080">Mobile no.</font>', 362, 138, 90)
heading('SKILLS', 59, 178)
para('<b>Responsive Web Design</b> (HTML5, CSS3)', 59, 202, 260)
para('<b>JavaScript</b> (ES, React, TypeScript, Next.js)', 59, 220, 260)
para('<b>Backend</b> (REST APIs, Node.js, Fastify,<br/>Express, BullMQ, Cron Jobs)', 59, 247, 260)
para('<b>Database</b> (MongoDB, PostgreSQL,<br/>Supabase)', 326, 202, 229)
para('<b>Version Control</b> (Git, GitHub, Bitbucket)', 326, 234, 229)
para('<b>Linux</b>', 326, 252, 229)
para('<b>DevOps</b> (Docker, Docker Compose, CI/CD, GitHub Actions, GHCR)', 59, 283, 496)
heading('WORK EXPERIENCE', 57, 327)
y = experience('Allied Marketing', 'Full Stack Developer', 'March 2023 - Present', [
    'Owned end-to-end project delivery and server operations, including installation, configuration, and deployment.',
    'Converted designs into responsive email templates compatible with devices and email clients.',
    'Developed in-house tools to streamline workflows and automate repetitive tasks.',
    'Designed and implemented Bitbucket CI/CD pipelines for automated deployments.',
    'Built a UI-based, API-driven email warm-up tool with scheduling, mail-class selection, and recipient management.'
], 343)
y = experience('PMHOA Pro', 'Software Developer', 'November 2024 - September 2026', [
    'Designed and developed an internal production CRM, defining its initial architecture and selecting Next.js and PostgreSQL as the core stack.',
    'Migrated the production PostgreSQL database and maintained database connectivity and production stability.',
    'Improved CI/CD and deployment workflows using GitHub Actions, Docker, and GHCR.',
    'Moved builds from the production server to GitHub Actions, improving deployment reliability and reducing server resource usage.',
    'Maintained email campaign operations and troubleshot sending issues to keep campaigns running reliably.',
    'Troubleshot production issues and maintained the application and deployment process.'
], y)
y = experience('Digiteer', 'Software Developer', 'September 2021 - December 2022', [
    'Developed, maintained, and enhanced full stack applications alongside the CTO.',
    'Managed and monitored AWS cloud services.'
], y)
y = experience('Splasheo', 'Software Developer', 'March 2021 - August 2021', [
    'Developed a REST API for video thumbnails, optimized for performance and security, and integrated it with other services.'
], y)
print(f'Page 1 content ends at {y-12:.1f} pt')
c.showPage()
heading('PROJECTS', 75.5, 92)
y = para('• <b>Internal Production CRM - PMHOA Pro</b>', 75.5, 122, 480)
y = para('<font color="#808080">Next.js, PostgreSQL, GitHub Actions, Docker, GHCR</font>', 95.5, y+4, 460, 10, 13)
y = para('◦ Designed and developed an internal production CRM from initial project setup, selecting its technology stack and defining its application architecture. Continued supporting the system through PostgreSQL migration, CI/CD improvements, production deployments, troubleshooting, and ongoing maintenance.', 75.5, y+6, 480)
y = para('<font color="#808080">Private internal system - source code and live access are not publicly available.</font>', 75.5, y+7, 480, 10, 13)
y = para('• <b>Email Warm-Up Automation</b> - Email Deliverability Tool<br/><font color="#808080">( March 2023 - Present )</font>', 75.5, y+26, 480)
y = para('◦ Developed a UI-based, API-driven tool to replace manual email warm-up scripts. Implemented scheduling, mail-class selection, and recipient management to gradually increase volume and strengthen sender reputation.', 75.5, y+4, 480)
y = para('• <b>Splasheo Media Platform</b> - Online Audio and Video Media<br/><font color="#808080">( March 2021 - August 2021 )</font>', 75.5, y+26, 480)
y = para('◦ Developed an API for video thumbnail generation and integrated APIs for publishing videos on social media platforms.', 95.5, y+4, 460)
y = heading('EDUCATION', 75.5, y+26)
y = para('• <b>Christ the King College</b> - BS in Information Technology <font color="#808080">( 2015 - 2020 )</font>', 95.5, y+2, 460)
print(f'Page 2 content ends at {y:.1f} pt')
c.save()
print(OUTPUT)
