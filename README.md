# 📄 Research Paper Relevance Checker

Welcome to the **Research Paper Relevance Checker** — a simple and clean tool designed to save you hours of reading through endless research papers!

Instead of manually skimming pages just to figure out if a paper is relevant to your thesis, this tool turns the process into a fast, automated experience.

---

## ✨ How It Works

- Upload a **research paper** (PDF)
- Upload either your **thesis topic** or a **draft document**
- Get instant output:
  - 🔍 **Relevance score** between your topic and the research paper
  - 📖 **Top citations** extracted from the paper (filtered and cleaned)
  - ✍️ **Suggested literature review paragraph** you can use as inspiration
- 📥 Download the full analysis as a **PDF report** for easy safekeeping!

---

## ⚙️ Technologies Used

- **Cosine Similarity**: Calculates the semantic similarity between your thesis and the research paper using their vector embeddings
- **Cohere API**:  
  - Embeds text into semantic vectors
  - Summarizes the research paper
  - Generates the literature review paragraph
- **pdfminer.six**: Extracts text from uploaded PDF files
- **ReportLab**: Dynamically generates the downloadable PDF report
- **Streamlit**: Builds the interactive web app UI

---

## 🚀 Features

- Clean UI for uploading documents
- Fully interactive web app (built with Streamlit)
- Intelligent filtering of citations (removes meaningless year-only citations)
- Ability to download all outputs into a polished PDF
- Warning when a paper may not be relevant (relevance score under 30%)

---

## 📦 Installation

If you want to run it locally:

```bash
pip install streamlit cohere numpy pdfminer.six reportlab
```

Then:

```bash
streamlit run app.py
```

You'll also need a **Cohere API key** — you can get one by signing up at [https://dashboard.cohere.com/](https://dashboard.cohere.com/).

---

## 📜 Disclaimer

This tool is intended for **research support purposes** only. The relevance score and generated paragraphs are suggestions and should be critically evaluated in the context of your academic work.

---

## 👩‍💻 Author

Built by **Sadia Khan** ✨  
Feel free to connect on [LinkedIn](https://www.linkedin.com/in/sadia-khan90/) or view more projects on [GitHub](#)!

---
