import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# --- Streamlit App: PDF & Image Generator ---
st.title("📄 PDF & Image Generator")

# Input Forms
st.header("Enter Your Content")
doc_title = st.text_input("Document Title", value="Proof of Shipping Delays Due to U.S. Tariffs")
summary = st.text_area("Summary", height=100)
timeline = st.text_area("Shipping Timeline Comparison", height=100)
complaints = st.text_area("Customer Complaints (one per line)", height=100)
final_note = st.text_area("Final Note", height=100)

# Output format selection
output_format = st.radio("Choose Output Format", ["PDF", "Image (PNG)"])

# --- Live Preview as Image ---
st.subheader("Live Preview")

def generate_preview_image(title, summary, timeline, complaints, final_note):
    width, height = 800, 1000
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font_path = "DejaVuSans.ttf"
    title_font = ImageFont.truetype(font_path, 30)
    sub_font = ImageFont.truetype(font_path, 24)
    body_font = ImageFont.truetype(font_path, 18)
    italic_font = ImageFont.truetype(font_path, 18)
    x, y = 20, 20

    # Title
    for line in textwrap.wrap(title, width=30):
        draw.text((x, y), line, font=title_font, fill="black")
        y += 36
    y += 10

    # Summary
    for line in textwrap.wrap(summary, width=60):
        draw.text((x, y), line, font=body_font, fill="black")
        y += 28
    y += 10

    # Timeline
    draw.text((x, y), "Shipping Timeline Comparison", font=sub_font, fill="black")
    y += 32
    for line in textwrap.wrap(timeline, width=60):
        draw.text((x, y), line, font=body_font, fill="black")
        y += 28
    y += 10

    # Complaints
    draw.text((x, y), "Customer Complaint Examples", font=sub_font, fill="black")
    y += 32
    for cmt in complaints.splitlines():
        for line in textwrap.wrap(f"• {cmt}", width=60):
            draw.text((x, y), line, font=body_font, fill="black")
            y += 28
    y += 10

    # Final Note
    draw.text((x, y), "Final Note", font=sub_font, fill="black")
    y += 32
    for line in textwrap.wrap(final_note, width=60):
        draw.text((x, y), line, font=italic_font, fill="black")
        y += 28

    return img

# Generate and display preview every run
preview_img = generate_preview_image(doc_title, summary, timeline, complaints, final_note)
st.image(preview_img, use_container_width=True)

# --- Generate & Download ---
if st.button("Generate & Download"):
    if output_format == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        

        # PDF Title
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, doc_title, ln=True)
        pdf.ln(5)

        # Summary
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 6, summary)
        pdf.ln(5)

        # Timeline
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, "Shipping Timeline Comparison", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 6, timeline)
        pdf.ln(5)

        # Complaints
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, "Customer Complaint Examples", ln=True)
        pdf.set_font("DejaVu", "", 12)
        for cmt in complaints.splitlines():
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"• {cmt}")
        pdf.ln(5)

        # Final Note
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 6, final_note)

        pdf_bytes = pdf.output(dest='S')
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="shipping_report.pdf",
            mime="application/pdf"
        )

    else:
        buf = io.BytesIO()
        preview_img.save(buf, format="PNG")
        buf.seek(0)
        st.download_button(
            label="Download Image",
            data=buf,
            file_name="shipping_report.png",
            mime="image/png"
        )
