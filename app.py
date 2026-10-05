
import streamlit as st
import ollama
from pypdf import PdfReader
from docx import Document


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Notes Assistant",
    page_icon="📚",
    layout="wide"
)



# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #4F46E5;
}

.subtitle {
    text-align: center;
    color: #666666;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">📚 AI-Powered Notes Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform difficult notes into clear, organized and readable study material.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "generated_notes" not in st.session_state:
    st.session_state.generated_notes = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Notes Preferences")

    output_format = st.selectbox(
        "📑 Notes Format",
        [
            "Pointwise",
            "Paragraph",
            "Question & Answer",
            "Summary",
            "Detailed Notes",
            "Mind Map / Diagram"
        ]
    )

    language = st.selectbox(
        "🌐 Output Language",
        [
            "English",
            "Hindi",
            "Telugu",
            "Tamil",
            "Kannada",
            "Malayalam"
        ]
    )

    writing_style = st.selectbox(
        "✍️ Writing Style",
        [
            "Simple and Easy to Understand",
            "Professional",
            "Student Friendly",
            "Exam Preparation",
            "Short and Concise",
            "Detailed Explanation"
        ]
    )


# =========================================================
# LANGUAGE INSTRUCTIONS
# =========================================================

language_instructions = {

    "English": """
Write the entire answer in English.
Use clear and natural English.
""",

    "Hindi": """
Write the entire answer in Hindi using Devanagari script.

IMPORTANT:
- Do NOT write the main explanation in English.
- Use Hindi sentences and Hindi vocabulary.
- English technical terms may be included in brackets when necessary.
- Example:
  कृत्रिम बुद्धिमत्ता (Artificial Intelligence) एक ऐसी तकनीक है...
""",

    "Telugu": """
Write the entire answer in Telugu using Telugu script.

IMPORTANT:
- Do NOT write the main explanation in English.
- Use natural and easy-to-understand Telugu.
- Use Telugu sentences throughout the answer.
- English technical terms may be included in brackets when necessary.
- Example:
  కృత్రిమ మేధస్సు (Artificial Intelligence) అనేది కంప్యూటర్లు
  మానవ మేధస్సుకు సంబంధించిన పనులను చేయడానికి సహాయపడే సాంకేతికత.
""",

    "Tamil": """
Write the entire answer in Tamil using Tamil script.

IMPORTANT:
- Do NOT write the main explanation in English.
- Use natural and easy-to-understand Tamil.
- Use Tamil sentences throughout the answer.
- English technical terms may be included in brackets when necessary.
""",

    "Kannada": """
Write the entire answer in Kannada using Kannada script.

IMPORTANT:
- Do NOT write the main explanation in English.
- Use natural and easy-to-understand Kannada.
- Use Kannada sentences throughout the answer.
- English technical terms may be included in brackets when necessary.
""",

    "Malayalam": """
Write the entire answer in Malayalam using Malayalam script.

IMPORTANT:
- Do NOT write the main explanation in English.
- Use natural and easy-to-understand Malayalam.
- Use Malayalam sentences throughout the answer.
- English technical terms may be included in brackets when necessary.
"""
}


# =========================================================
# FILE UPLOAD
# =========================================================

st.subheader("📤 Step 1: Upload Your Notes")

uploaded_file = st.file_uploader(
    "Upload your notes",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT"
)


# =========================================================
# PDF EXTRACTION
# =========================================================

def extract_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================================
# DOCX EXTRACTION
# =========================================================

def extract_docx(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    return text


# =========================================================
# TXT EXTRACTION
# =========================================================

def extract_txt(file):

    return file.read().decode("utf-8")


# =========================================================
# GENERAL EXTRACTION
# =========================================================

def extract_text(file):

    filename = file.name.lower()

    if filename.endswith(".pdf"):

        return extract_pdf(file)

    elif filename.endswith(".docx"):

        return extract_docx(file)

    elif filename.endswith(".txt"):

        return extract_txt(file)

    return ""


# =========================================================
# PROCESS FILE
# =========================================================

if uploaded_file:

    with st.spinner("📖 Reading your notes..."):

        try:

            notes_text = extract_text(uploaded_file)

        except Exception as error:

            st.error(
                f"❌ Error while reading the file: {error}"
            )

            st.stop()


    if not notes_text.strip():

        st.error(
            "❌ No readable text was found in this file."
        )

        st.info(
            "Scanned PDFs and handwritten notes require OCR support."
        )

    else:

        st.success(
            "✅ Notes successfully uploaded and read!"
        )


        # =================================================
        # ORIGINAL NOTES
        # =================================================

        with st.expander("📄 View Original Notes"):

            st.text_area(
                "Original Content",
                notes_text,
                height=300
            )


        # =================================================
        # SELECTED OPTIONS
        # =================================================

        st.subheader("🎨 Step 2: Your Preferences")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"📑 Format\n\n{output_format}"
            )

        with col2:

            st.info(
                f"🌐 Language\n\n{language}"
            )

        with col3:

            st.info(
                f"✍️ Style\n\n{writing_style}"
            )


        # =================================================
        # FORMAT INSTRUCTIONS
        # =================================================

        if output_format == "Pointwise":

            format_instruction = """
Convert the notes into clear pointwise notes.

Use:
- Main headings
- Subheadings
- Bullet points
- Short explanations

Make the content easy to study.
"""


        elif output_format == "Paragraph":

            format_instruction = """
Convert the notes into clear and well-structured paragraphs.

Maintain logical flow between ideas.
Use headings where appropriate.
"""


        elif output_format == "Question & Answer":

            format_instruction = """
Convert the notes into Question and Answer format.

Create useful questions that students may
encounter during examinations.

Provide clear answers.
"""


        elif output_format == "Summary":

            format_instruction = """
Create a concise summary.

Include only the most important concepts.
Remove unnecessary repetition.
"""


        elif output_format == "Detailed Notes":

            format_instruction = """
Create detailed study notes.

Use:
- Headings
- Subheadings
- Bullet points
- Examples
- Clear explanations

Make the notes useful for exam preparation.
"""


        else:

            format_instruction = """
Create a text-based mind map.

Use a hierarchical structure.

Example:

Main Topic
├── Topic 1
│   ├── Subtopic
│   └── Subtopic
│
└── Topic 2
    ├── Subtopic
    └── Subtopic

IMPORTANT:
The labels and explanations in the mind map
must also be written in the selected language.
"""


        # =================================================
        # GENERATE BUTTON
        # =================================================

        if st.button(
            "✨ Generate Improved Notes",
            type="primary",
            use_container_width=True
        ):


            # =================================================
            # GET LANGUAGE INSTRUCTION
            # =================================================

            selected_language_instruction = (
                language_instructions[language]
            )


            # =================================================
            # AI PROMPT
            # =================================================

            prompt = f"""

You are an advanced multilingual AI Notes Assistant.

Your task is to transform the user's original study notes
into clear, organized and easy-to-understand study material.

==================================================
CRITICAL LANGUAGE REQUIREMENT
==================================================

The selected output language is:

{language}

{selected_language_instruction}

The final answer MUST be written in {language}.

DO NOT automatically answer in English.

Even though the original notes may be in English,
you MUST translate and explain the content in {language}.

Only keep English words when they are:
- technical terms
- programming keywords
- scientific names
- commonly used terms that do not have a natural translation

The headings, explanations, bullet points,
questions and answers must all be in {language}.

==================================================
IMPORTANT RULES
==================================================

1. Do not remove important information.

2. Do not invent information.

3. Do not add unrelated information.

4. Correct obvious spelling mistakes.

5. Correct obvious grammar mistakes.

6. Explain difficult concepts clearly.

7. Organize information logically.

8. Use headings and subheadings when appropriate.

9. Follow the requested format exactly.

10. Follow the requested writing style.

11. Use natural language instead of word-for-word translation.

12. Make the notes easy for a student to understand.

==================================================
REQUESTED FORMAT
==================================================

{output_format}

==================================================
FORMAT INSTRUCTIONS
==================================================

{format_instruction}

==================================================
REQUESTED WRITING STYLE
==================================================

{writing_style}

==================================================
ORIGINAL NOTES
==================================================

{notes_text}

==================================================
FINAL INSTRUCTION
==================================================

Generate ONLY the final improved notes.

Do not explain what you are doing.

Do not mention these instructions.

The final answer MUST be in {language}.
"""


            # =================================================
            # CALL OLLAMA
            # =================================================

            with st.spinner(
                f"🤖 Generating notes in {language}..."
            ):

                try:

                    response = ollama.chat(
                        model="llama3.2",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        options={
                            "temperature": 0.3
                        }
                    )


                    generated_notes = (
                        response["message"]["content"]
                    )


                    st.session_state.generated_notes = (
                        generated_notes
                    )


                except Exception as error:

                    st.error(
                        "❌ Could not connect to Ollama."
                    )

                    st.code(str(error))


# =========================================================
# DISPLAY GENERATED NOTES
# =========================================================

if st.session_state.generated_notes:

    st.divider()

    st.subheader("✨ Step 3: Generated Notes")

    st.markdown(
        st.session_state.generated_notes
    )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.subheader("📥 Step 4: Download Your Notes")

    col1, col2 = st.columns(2)


    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=st.session_state.generated_notes,
            file_name="AI_Improved_Notes.txt",
            mime="text/plain",
            use_container_width=True
        )


    with col2:

        st.download_button(
            label="📝 Download Markdown",
            data=st.session_state.generated_notes,
            file_name="AI_Improved_Notes.md",
            mime="text/markdown",
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📚 AI-Powered Notes Assistant | "
    "Python + Streamlit + Ollama + Llama 3.2"
)


