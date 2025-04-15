import streamlit as st
import cohere
import numpy as np
import re
from pdfminer.high_level import extract_text
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- CONFIG ---
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
co = cohere.Client(COHERE_API_KEY)

# --- FUNCTIONS ---

def extract_text_from_pdf(uploaded_file):
    return extract_text(uploaded_file)

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def extract_citations(text):
    return re.findall(r'\[\d+\]|\(.*?\d{4}.*?\)', text)

def generate_lit_review_paragraph(summary):
    response = co.generate(
        model="command",
        prompt=f"Based on this research paper summary, write a sample literature review paragraph for an academic thesis:\n\n{summary}",
        max_tokens=200
    )
    return response.generations[0].text

def get_embedding(text, input_type="search_query"):
    return co.embed(texts=[text], model="embed-english-v3.0", input_type=input_type).embeddings[0]

def generate_pdf(score, summary, citations, lit_paragraph):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "Research Paper Relevance Report")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Relevance Score: {score:.2f}")

    if score <= 0.30:
        y -= 20
        c.setFillColorRGB(1, 0, 0)
        c.drawString(40, y, "⚠️ Warning: This paper may not be very relevant to your thesis.")
        c.setFillColorRGB(0, 0, 0)

    def draw_wrapped_text(title, text):
        nonlocal y
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, title)
        y -= 18
        c.setFont("Helvetica", 11)
        for line in text.split('\n'):
            for part in re.findall(r'.{1,95}(?:\s+|$)', line.strip()):
                c.drawString(40, y, part.strip())
                y -= 14
                if y < 60:
                    c.showPage()
                    y = height - 40

    draw_wrapped_text("📌 Summary of the Paper", summary)
    draw_wrapped_text("📖 Suggested Citations", "\n".join(f"{i+1}. {c}" for i, c in enumerate(citations)))
    draw_wrapped_text("✍️ Literature Review Paragraph", lit_paragraph)

    c.save()
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---

st.set_page_config(page_title="Research Paper Relevance Checker", page_icon="📄")
st.title("📄 Research Paper Relevance Checker")

st.markdown("Upload a research paper and enter your thesis topic or upload your thesis draft (optional) to check for relevance.")

uploaded_paper = st.file_uploader("📎 Upload a research paper (PDF)", type="pdf")

col1, col2 = st.columns(2)
with col1:
    thesis_topic = st.text_input("📝 Next, enter your thesis topic manually")
with col2:
    thesis_file = st.file_uploader("📄 Or upload your thesis as a PDF (optional)", type="pdf", key="thesis")

submit = st.button("🔍 Analyze Paper")

if submit and uploaded_paper and (thesis_topic or thesis_file):
    with st.spinner("Analyzing..."):

        try:
            paper_text = extract_text_from_pdf(uploaded_paper)

            # Thesis source
            if thesis_topic:
                thesis_text = thesis_topic
            else:
                thesis_text = extract_text_from_pdf(thesis_file)

            # Embeddings
            thesis_vec = get_embedding(thesis_text, input_type="search_query")
            paper_vec = get_embedding(paper_text[:2000], input_type="search_document")

            score = cosine_similarity(thesis_vec, paper_vec)
            st.markdown(f"### 🔍 Relevance Score: `{score:.2f}`")

            if score <= 0.30:
                st.warning("⚠️ Warning: This paper may not be very relevant to your thesis.")

            # Summary
            st.markdown("### 📌 Summary of the Paper")
            summary = co.summarize(text=paper_text[:5000], length="long", format="bullets")
            st.markdown(summary.summary)

            # Citations
            st.markdown("### 📖 Suggested Citations")
            citations = extract_citations(paper_text)
            cleaned_citations = [
                c for c in citations
                if not re.fullmatch(r'\(?\d{4}(–\d{2,4})?\)?', c)
            ][:10]

            if cleaned_citations:
                for i, cite in enumerate(cleaned_citations, 1):
                    st.markdown(f"{i}. {cite}")
            else:
                st.info("No clear citations found.")

            # Lit review paragraph
            st.markdown("### ✍️ Sample Literature Review Paragraph")
            lit_para = generate_lit_review_paragraph(summary.summary)
            cleaned_para = re.sub(r'^(Certainly!|Sure!|Here.*?:)\s*', '', lit_para.strip(), flags=re.IGNORECASE)
            st.markdown(cleaned_para)

            # PDF Download
            pdf = generate_pdf(score, summary.summary, cleaned_citations, cleaned_para)
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf,
                file_name="research_paper_summary.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
