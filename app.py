import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from modules.ai_core import generate_text, embed_texts, retrieve_relevant_chunks
from modules.document_loader import extract_pdf_chunks
from modules.tools import build_study_plan, route_agent_task, make_quiz_prompt

load_dotenv()

st.set_page_config(
    page_title="StudyMate AI | Study & Career Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main .block-container {padding-top: 1.8rem; max-width: 1200px;}
    .hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#172554,#2563eb); color: white; margin-bottom: 1rem;}
    .hero h1 {color: white; margin-bottom: .35rem;}
    .hero p {color: #e0e7ff; margin-bottom: 0;}
    div[data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.25); padding: 12px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🎓 StudyMate AI</h1>
<p>Your AI companion for learning, document research, revision, and career planning.</p>
</div>
""", unsafe_allow_html=True)

load_dotenv()

# Read the API key from Streamlit Secrets first,
# then fall back to the local .env environment.
try:
    default_api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    default_api_key = ""

default_api_key = default_api_key or os.getenv("GEMINI_API_KEY", "")

api_key = st.sidebar.text_input(
    "Gemini API key",
    value=default_api_key,
    type="password",
    help="Your key is used only for API requests. Never commit it to GitHub.",
)

model_name = st.sidebar.selectbox(
    "Gemini model",
    ["gemini-3.8-flash", "gemini-3.6-flash"],
    index=0,
)

st.sidebar.caption(
    "Configure GEMINI_API_KEY in Streamlit Secrets or your local .env file."
)

model_name = st.sidebar.selectbox(
    "Gemini model",
    ["gemini-3.8-flash", "gemini-3.6-flash"],
    index=0,
    key="gemini_model_selectbox",
)

st.sidebar.caption("Tip: Add GEMINI_API_KEY to your local .env file or deployment secrets.")
if not api_key:
    st.info("Add your Gemini API key in the sidebar to enable AI features. You can create one in Google AI Studio.")
    st.link_button("Get a Gemini API key", "https://aistudio.google.com/apikey")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = []
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""
if "doc_embeddings" not in st.session_state:
    st.session_state.doc_embeddings = None

client = genai.Client(api_key=api_key) if api_key else None

with st.sidebar:
    st.divider()
    st.subheader("Quick actions")
    if st.button("Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("Clear uploaded document", use_container_width=True):
        st.session_state.doc_chunks = []
        st.session_state.doc_embeddings = None
        st.session_state.doc_name = ""
        st.rerun()
    st.divider()
    st.caption("Privacy: uploaded document text is processed in your current app session and sent to the selected AI API only when needed for embedding or answering questions.")

tab_chat, tab_docs, tab_plan, tab_quiz, tab_career = st.tabs(
    ["💬 AI Chat", "📄 Chat with PDF", "🗓️ Study Planner", "🧠 Quiz Generator", "🚀 Career Assistant"]
)

def require_client():
    if client is None:
        st.warning("Add your Gemini API key in the sidebar first.")
        return False
    return True

with tab_chat:
    st.subheader("Ask StudyMate")
    st.write("Ask for explanations, examples, summaries, programming help, or revision notes.")
    examples = st.columns(3)
    example_prompts = [
        "Explain gradient descent in simple terms.",
        "Give me a Python example of a stack.",
        "Create a 5-point revision summary of DBMS normalization.",
    ]
    for col, prompt in zip(examples, example_prompts):
        with col:
            if st.button(prompt, use_container_width=True, key="example_" + str(example_prompts.index(prompt))):
                st.session_state.chat_prompt = prompt

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("What would you like to learn today?")
    if "chat_prompt" in st.session_state:
        user_prompt = st.session_state.pop("chat_prompt")
    if user_prompt:
        if require_client():
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
            history = st.session_state.messages[-10:]
            prompt = (
                "You are StudyMate, a patient and accurate study and career assistant. "
                "Explain concepts clearly, use examples where useful, and distinguish facts from uncertainty. "
                "For educational questions, prefer structured answers.\n\n"
                f"Recent conversation:\n{history}\n\nLatest user request: {user_prompt}"
            )
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = generate_text(client, model_name, prompt)
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as exc:
                        st.error(f"Gemini request failed: {exc}")
                        st.caption("Check your API key, internet connection, model availability, and API quota.")

with tab_docs:
    st.subheader("Ask questions about your PDF")
    st.write("Upload lecture notes or a study PDF. StudyMate will retrieve relevant text passages and use them as context for its answer.")
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_upload")
    if pdf is not None and require_client():
        if st.button("Process PDF", type="primary"):
            with st.spinner("Extracting text and creating embeddings..."):
                try:
                    chunks = extract_pdf_chunks(pdf)
                    if not chunks:
                        st.error("No readable text was found. This may be a scanned PDF that needs OCR.")
                    else:
                        vectors = []
                        for start in range(0, len(chunks), 50):
                            batch = chunks[start:start + 50]
                            vectors.extend(embed_texts(client, batch))
                        st.session_state.doc_chunks = chunks
                        st.session_state.doc_embeddings = vectors
                        st.session_state.doc_name = pdf.name
                        st.success(f"Processed {len(chunks)} text chunks from {pdf.name}.")
                except Exception as exc:
                    st.error(f"PDF processing failed: {exc}")

    if st.session_state.doc_chunks:
        st.success(f"Active document: {st.session_state.doc_name} · {len(st.session_state.doc_chunks)} chunks")
        question = st.text_input("Your question", placeholder="What are the key concepts in this document?")
        if st.button("Ask about this PDF", type="primary") and question:
            if require_client():
                with st.spinner("Searching document and generating answer..."):
                    try:
                        retrieved = retrieve_relevant_chunks(
                            client,
                            question,
                            st.session_state.doc_chunks,
                            st.session_state.doc_embeddings,
                            top_k=4,
                        )
                        context = "\n\n".join(
                            [f"[Passage {i+1}]\n{item['text']}" for i, item in enumerate(retrieved)]
                        )
                        prompt = (
                            "You are a document-grounded study assistant. Answer using the supplied passages. "
                            "If the answer is not supported by the passages, say so and then clearly label any general explanation. "
                            "Do not invent citations. Refer to passage numbers when helpful.\n\n"
                            f"Document: {st.session_state.doc_name}\n"
                            f"Retrieved passages:\n{context}\n\nQuestion: {question}"
                        )
                        answer = generate_text(client, model_name, prompt)
                        st.markdown("### Answer")
                        st.markdown(answer)
                        with st.expander("View retrieved passages"):
                            for i, item in enumerate(retrieved):
                                st.markdown(f"**Passage {i+1}**")
                                st.write(item["text"])
                    except Exception as exc:
                        st.error(f"Document question failed: {exc}")
    else:
        st.caption("No PDF has been processed in this session yet.")

with tab_plan:
    st.subheader("Build a realistic study plan")
    with st.form("study_plan_form"):
        subjects = st.text_input("Subjects or topics", placeholder="DBMS, Machine Learning, Numerical Methods")
        days_left = st.number_input("Days until deadline or exam", min_value=1, max_value=180, value=7)
        hours_per_day = st.slider("Hours available per day", min_value=1, max_value=12, value=3)
        level = st.selectbox("Current preparation level", ["Beginner", "Some understanding", "Revision"])
        plan_submit = st.form_submit_button("Generate study plan", type="primary")
    if plan_submit:
        if require_client():
            if not subjects.strip():
                st.warning("Enter at least one subject or topic.")
            else:
                prompt = build_study_plan(subjects, int(days_left), int(hours_per_day), level)
                with st.spinner("Preparing your schedule..."):
                    try:
                        st.markdown(generate_text(client, model_name, prompt))
                    except Exception as exc:
                        st.error(f"Could not generate a plan: {exc}")

with tab_quiz:
    st.subheader("Generate a practice quiz")
    with st.form("quiz_form"):
        quiz_topic = st.text_input("Topic", placeholder="Linear regression")
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")
        question_count = st.slider("Number of questions", min_value=3, max_value=15, value=5)
        quiz_type = st.selectbox("Question style", ["Multiple choice", "Short answer", "Mixed"])
        quiz_submit = st.form_submit_button("Generate quiz", type="primary")
    if quiz_submit:
        if require_client():
            if not quiz_topic.strip():
                st.warning("Enter a topic first.")
            else:
                with st.spinner("Creating your quiz..."):
                    try:
                        result = generate_text(client, model_name, make_quiz_prompt(quiz_topic, difficulty, question_count, quiz_type))
                        st.markdown(result)
                    except Exception as exc:
                        st.error(f"Quiz generation failed: {exc}")

with tab_career:
    st.subheader("Career and skills guidance")
    with st.form("career_form"):
        interest = st.text_input("Career area or role", placeholder="Data analyst, AI engineer, cybersecurity")
        current_skills = st.text_area("Current skills", placeholder="Python, SQL, Excel, machine learning...")
        goal = st.selectbox("Main goal", ["Get an internship", "Prepare for a job", "Choose a career path", "Build a portfolio"])
        timeline = st.selectbox("Timeline", ["1 month", "3 months", "6 months", "12 months"])
        career_submit = st.form_submit_button("Create my roadmap", type="primary")
    if career_submit:
        if require_client():
            if not interest.strip():
                st.warning("Enter a career area or role.")
            else:
                prompt = (
                    "You are a practical career mentor for a student. Give realistic guidance and do not guarantee jobs, salaries, or outcomes. "
                    "Make the response specific to the user's skills, goal, and timeline. Include: role overview, skill gaps, a week-by-week roadmap, "
                    "two portfolio project ideas, interview preparation, and ways to measure progress.\n\n"
                    f"Career area: {interest}\nCurrent skills: {current_skills or 'Not specified'}\nGoal: {goal}\nTimeline: {timeline}"
                )
                with st.spinner("Building your roadmap..."):
                    try:
                        st.markdown(generate_text(client, model_name, prompt))
                    except Exception as exc:
                        st.error(f"Career guidance failed: {exc}")

st.divider()
st.caption("StudyMate AI is an educational prototype. Verify important information and do not enter confidential personal data.")
