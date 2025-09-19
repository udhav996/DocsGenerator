from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os
from datetime import datetime


def get_next_tc_number():
    counter_file = "tc_counter.txt"
    current_year = datetime.now().year
    prefix = f"TC-{current_year}-"

    # Read last number
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            last_number = int(f.read().strip())
    else:
        last_number = 0

    # Increment and write back
    new_number = last_number + 1
    with open(counter_file, "w") as f:
        f.write(str(new_number))

    return f"{prefix}{new_number:03d}"  # e.g., TC-2025-001


def draw_curved_header(c, width, height):
    """Draw curved header design similar to template"""
    # Main teal header
    c.setFillColor(HexColor("#2d6e7e"))
    c.rect(0, height - 120, width, 120, fill=1)

    # Yellow curved accents using paths
    c.setFillColor(HexColor("#f4c430"))

    # Left curved accent
    path = c.beginPath()
    path.moveTo(0, height - 120)
    path.curveTo(100, height - 80, 150, height - 60, 200, height - 120)
    path.lineTo(0, height - 120)
    c.drawPath(path, fill=1)

    # Right curved accent
    path = c.beginPath()
    path.moveTo(width, height - 120)
    path.curveTo(width - 100, height - 80, width - 150, height - 60, width - 200, height - 120)
    path.lineTo(width, height - 120)
    c.drawPath(path, fill=1)


def draw_bottom_decoration(c, width):
    """Draw bottom decorative element"""
    bottom_y = 70

    # Teal rectangle base
    c.setFillColor(HexColor("#2d6e7e"))
    c.rect(width / 2 - 60, bottom_y - 30, 120, 40, fill=1)

    # Yellow accent triangles using paths
    c.setFillColor(HexColor("#f4c430"))

    # Left triangle
    path = c.beginPath()
    path.moveTo(width / 2 - 80, bottom_y - 10)
    path.lineTo(width / 2 - 60, bottom_y + 10)
    path.lineTo(width / 2 - 60, bottom_y - 30)
    path.lineTo(width / 2 - 80, bottom_y - 10)  # Close the path manually
    c.drawPath(path, fill=1)

    # Right triangle
    path = c.beginPath()
    path.moveTo(width / 2 + 80, bottom_y - 10)
    path.lineTo(width / 2 + 60, bottom_y + 10)
    path.lineTo(width / 2 + 60, bottom_y - 30)
    path.lineTo(width / 2 + 80, bottom_y - 10)  # Close the path manually
    c.drawPath(path, fill=1)


def generate_tc(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = data.get("name", "student").replace(" ", "_")
    filename = f"outputs/{safe_name}_{timestamp}_TC.pdf"

    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # Auto-generate TC number if not provided
    if not data.get("tc_no"):
        data["tc_no"] = get_next_tc_number()

    # Custom PDF size (reduced height to minimize space)
    custom_width = 550  # A4 width
    custom_height = 650  # Significantly reduced from A4 height (842)
    c = canvas.Canvas(filename, pagesize=(custom_width, custom_height))
    width, height = custom_width, custom_height

    # Background
    c.setFillColor(HexColor("#f8f9fa"))
    c.rect(0, 0, width, height, fill=1)

    # Draw curved header
    draw_curved_header(c, width, height)

    # School name and address in header
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Times-Bold", 18)
    c.drawCentredString(width / 2, height - 45, "UDHAV ACADEMY")
    c.setFont("Times-Roman", 11)
    c.drawCentredString(width / 2, height - 65, "Near Durga devi Chowk, Latur - 413512, Maharashtra")

    # Logo (if exists)
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 110, width=80, height=80, mask='auto')

    # Main content area with border
    content_margin = 60
    content_width = width - 2 * content_margin
    content_top = height - 150
    content_bottom = 60  # Reduced to minimize bottom space
    content_height = content_top - content_bottom

    # White content background with border
    c.setFillColor(HexColor("#ffffff"))
    c.setStrokeColor(HexColor("#2d6e7e"))
    c.setLineWidth(2)
    c.rect(content_margin, content_bottom, content_width, content_height, fill=1, stroke=1)

    # Certificate title
    c.setFillColor(HexColor("#2d6e7e"))
    c.setFont("Times-Bold", 20)
    title_y = content_top - 40
    c.drawCentredString(width / 2, title_y, "Transfer Certificate")

    # Decorative line under title
    c.setStrokeColor(HexColor("#f4c430"))
    c.setLineWidth(3)
    c.line(width / 2 - 120, title_y - 12, width / 2 + 120, title_y - 12)

    # TC Number
    c.setFillColor(HexColor("#000000"))
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, title_y - 32, f"T.C. No: {data['tc_no']}")

    # Student details section
    c.setFillColor(HexColor("#000000"))
    details_start_y = title_y - 70
    line_height = 25

    # Field styling
    label_x = content_margin + 30
    colon_x = content_margin + 200
    value_x = content_margin + 220

    fields = [
        ("1. Name of Student", data.get("name", "")),
        ("2. Mother's Name", data.get("mother_name", "")),
        ("3. Religion and Caste", data.get("religion", "")),
        ("4. Date of Birth", data.get("dob", "")),
        ("5. Nationality", data.get("nationality", "")),
        ("6. Date of Leaving", data.get("leaving_date", "")),
        ("7. Reason for Leaving", data.get("reason", "")),
    ]

    current_y = details_start_y

    for i, (label, value) in enumerate(fields):
        # Alternate row background
        if i % 2 == 0:
            c.setFillColor(HexColor("#f8f9fa"))
            c.rect(content_margin + 15, current_y - 5, content_width - 30, line_height - 5, fill=1, stroke=0)

        c.setFillColor(HexColor("#000000"))
        c.setFont("Times-Bold", 11)
        c.drawString(label_x, current_y, label)
        c.drawString(colon_x, current_y, ":")
        c.setFont("Times-Roman", 11)
        c.drawString(value_x, current_y, value)
        current_y -= line_height

    # Certification statement
    cert_y = current_y - 20
    c.setFont("Times-Italic", 11)
    c.drawString(label_x, cert_y, "Certified that the above information is in accordance with the college record.")

    # Signature section with better styling
    sig_section_y = cert_y - 50

    # Signature boxes (smaller)
    sig_box_width = 100
    sig_box_height = 45

    # Left signature box (Clerk)
    clerk_x = content_margin + 40
    c.setStrokeColor(HexColor("#2d6e7e"))
    c.setLineWidth(1)
    c.rect(clerk_x, sig_section_y, sig_box_width, sig_box_height, fill=0, stroke=1)

    # Center signature box (Registrar)
    registrar_x = width / 2 - sig_box_width / 2
    c.rect(registrar_x, sig_section_y, sig_box_width, sig_box_height, fill=0, stroke=1)

    # Right signature box (Principal)
    principal_x = width - content_margin - sig_box_width - 40
    c.rect(principal_x, sig_section_y, sig_box_width, sig_box_height, fill=0, stroke=1)

    # Signature images (perfectly centered in boxes with increased size)
    clerk_sign = "assets/clerk_signature.png"
    principal_sign = "assets/signature.png"

    if os.path.exists(clerk_sign):
        c.drawImage(clerk_sign, clerk_x + 20, sig_section_y + 12,
                    width=sig_box_width - 40, height=28, mask='auto')

    if os.path.exists(principal_sign):
        c.drawImage(principal_sign, principal_x + 20, sig_section_y + 12,
                    width=sig_box_width - 40, height=28, mask='auto')

    # Signature labels
    c.setFont("Times-Bold", 11)
    c.drawCentredString(clerk_x + sig_box_width / 2, sig_section_y - 18, "Clerk")
    c.drawCentredString(registrar_x + sig_box_width / 2, sig_section_y - 18, "Registrar")
    c.drawCentredString(principal_x + sig_box_width / 2, sig_section_y - 18, "Principal")

    # Date (positioned just above the border line)
    date_y = content_bottom + 5
    c.setFont("Times-Roman", 10)
    c.drawString(content_margin + 30, date_y, f"Date: {datetime.now().strftime('%d/%m/%Y')}")

    # Watermark (more visible)
    watermark_path = "assets/logo.png"
    if os.path.exists(watermark_path):
        c.saveState()
        c.translate(width / 2 - 80, height / 2 - 120)
        c.setFillAlpha(0.15)  # Increased from 0.05 to 0.15 for better visibility
        c.drawImage(watermark_path, 0, 0, width=160, height=160, mask='auto')  # Larger size
        c.restoreState()
        c.setFillAlpha(1)

    # Draw bottom decoration
    draw_bottom_decoration(c, width)

    # Final save
    c.showPage()
    c.save()

    # Open PDF after generation
    try:
        os.startfile(os.path.abspath(filename))  # Windows only
    except:
        print(f"✅ TC generated: {filename}")

    return filename