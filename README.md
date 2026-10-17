# 🎓 StudyMate AI: AI Study & Career Assistant

An AI-powered study and career assistant built with Python, Streamlit, and Google's Gemini 3.6 Gemini 3.8 & Flash model. StudyMate AI helps students understand complex concepts, interact with PDF study materials, generate personalised study plans, practise through AI-generated quizzes, and explore career opportunities through an interactive web application.

The project demonstrates practical implementation of Generative AI, Large Language Model (LLM) integration, prompt engineering, Retrieval-Augmented Generation (RAG), embeddings, vector similarity search, and AI-powered application development.

---

## 📌 Project Overview

StudyMate AI is designed to make studying, revision, document research, and career preparation more accessible through a single AI-powered platform.

Instead of switching between different tools for studying, summarising notes, preparing quizzes, and exploring career paths, users can access these capabilities through one interface.

The application uses Google's Gemini API to generate responses, while its document question-answering workflow uses embeddings and similarity-based retrieval to find relevant passages from uploaded PDF files.

## ✨ Key Features

### 💬 1. AI Chat Assistant

Interact with an AI assistant for academic learning, programming assistance, and general educational questions.

Features include:
- Explain difficult concepts in simple language.
- Generate structured study notes and summaries.
- Provide programming explanations and examples.
- Answer follow-up questions using recent conversation history.
- Offer revision guidance and learning suggestions.
- Provide quick prompts for common educational tasks.

### 📄 2. Chat With Your PDFs

Upload PDF study materials and ask questions about their contents using a Retrieval-Augmented Generation (RAG) workflow.

Features include:
- Upload PDF files through the web interface.
- Extract readable text from PDF pages.
- Split extracted text into overlapping chunks.
- Generate embeddings for document chunks.
- Convert questions into embeddings.
- Retrieve relevant passages using cosine similarity.
- Generate answers using retrieved passages as context.
- Display retrieved passages for reference.

This feature is particularly useful for lecture notes, textbooks, revision material, and other text-based educational documents.

**Current limitation:** Scanned PDFs containing images rather than selectable text may require OCR, which is not included in the current version.

### 🗓️ 3. AI Study Planner

Generate a structured study schedule based on your preparation needs and available time.

Users can specify:
- Subjects or topics to study.
- Number of days remaining before an examination or deadline.
- Available study hours per day.
- Current preparation level.

The AI generates a practical schedule with topic prioritisation, revision sessions, practice activities, active recall, and final self-assessment suggestions.

### 🧠 4. AI Quiz Generator

Generate practice questions to support revision and self-assessment.

Features include:
- Select a topic.
- Choose Easy, Medium, or Hard difficulty.
- Generate between 3 and 15 questions.
- Choose multiple-choice, short-answer, or mixed question formats.
- Receive an answer key with concise explanations.

This feature can help students practise concepts and identify topics that need further revision.

### 🚀 5. AI Career Assistant

Explore career paths and create structured learning roadmaps.

Users can provide their career interests, current skills, goals, and preparation timeline.

The AI can generate:
- Career and role overviews.
- Skill-gap assessments.
- Week-by-week learning roadmaps.
- Portfolio project suggestions.
- Interview preparation recommendations.
- Practical milestones for tracking progress.

The assistant provides guidance rather than guaranteeing employment, salary outcomes, or internship selection.

### 🛠️ 6. AI Tools and Task Routing

The application includes dedicated prompt-building functions for study planning and quiz generation, along with a deterministic task-routing helper.

The router categorises requests into workflows such as general chat, study planning, quiz generation, career guidance, and document question answering.

The current implementation uses predefined routing rules rather than autonomous, model-driven agent selection. This provides a foundation for future integration of tool calling and more advanced agent workflows.

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Google Gemini 3.6 Flash | Additional AI model used during development and experimentation |
| Google Gemini 3.8 Flash | Working AI text-generation model |
| Google GenAI Python SDK | Gemini API integration |
| Gemini Embeddings | Document and query vector generation |
| NumPy | Vector operations and cosine similarity |
| pypdf | PDF text extraction |
| python-dotenv | Local environment configuration |
| Git and GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

---

## 🏗️ Project Architecture

The application follows a modular structure to separate the user interface, AI functionality, document processing, and task-specific workflows.

```text
StudyMate-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── ai_core.py
│   ├── document_loader.py
│   └── tools.py
│
├── docs/
│   └── architecture.md
│
├── tests/
│   └── test_tools.py
│
└── .streamlit/
    └── config.toml
```

### File Descriptions

- `app.py`: Main Streamlit application, interface, navigation, and feature workflows.
- `modules/ai_core.py`: Gemini text generation, embedding generation, and similarity-based retrieval.
- `modules/document_loader.py`: PDF text extraction and text chunking.
- `modules/tools.py`: Study-plan and quiz prompt builders and deterministic task routing.
- `requirements.txt`: Python dependency list.
- `.env`: Local environment variables and API key. This file must not be committed to GitHub.
- `.env.example`: Example environment configuration without a real API key.
- `.gitignore`: Excludes sensitive files and local development artefacts.
- `docs/architecture.md`: Additional technical architecture documentation.
- `tests/test_tools.py`: Automated tests for task routing and prompt-building functions.
- `.streamlit/config.toml`: Streamlit theme configuration.

---

## 🔄 How the Application Works

### AI Chat Workflow

1. The user enters a question in the Streamlit interface.
2. The application constructs a prompt containing the assistant's instructions and recent conversation context.
3. The prompt is sent to Gemini through the Google GenAI SDK.
4. Gemini generates a response.
5. The response is displayed in the chat interface.
6. The conversation is retained in the current Streamlit session.

### PDF RAG Workflow

The document question-answering feature follows these steps:

1. **Document upload:** The user uploads a PDF.
2. **Text extraction:** pypdf extracts selectable text from PDF pages.
3. **Text chunking:** The extracted text is divided into overlapping chunks.
4. **Embedding generation:** Gemini generates vector embeddings for the chunks.
5. **Question embedding:** The user's question is converted into a vector.
6. **Similarity search:** NumPy calculates cosine similarity between the question vector and document vectors.
7. **Context retrieval:** The highest-ranked passages are selected.
8. **Prompt construction:** The question and retrieved passages are combined into a prompt.
9. **AI response:** Gemini generates an answer using the supplied context.
10. **Result display:** The application displays the answer and retrieved passages.

### Study Planning Workflow

1. The user enters subjects, days remaining, daily study hours, and preparation level.
2. The application constructs a study-planning prompt.
3. Gemini generates a structured schedule.
4. The resulting plan is displayed in the application.

### Quiz Generation Workflow

1. The user selects a topic, difficulty, question count, and question format.
2. The application constructs a quiz-specific prompt.
3. Gemini generates questions and an answer key.
4. The quiz is displayed for practice and revision.

### Career Guidance Workflow

1. The user specifies a career area, current skills, primary goal, and timeline.
2. The application constructs a career-planning prompt.
3. Gemini identifies potential skill gaps and learning priorities.
4. The assistant generates a roadmap and portfolio suggestions.

---

## ⚙️ Installation and Setup

### Prerequisites

Before running StudyMate AI, ensure that you have:

- Python 3.10 or newer.
- Visual Studio Code or another Python-compatible editor.
- Git installed on your system.
- An internet connection.
- A Google Gemini API key.

### Step 1: Download or Clone the Repository

Clone the repository after uploading the project to GitHub:

```bash
git clone https://github.com/rahulg2004/GenAI-Capstone-Project.git
```

Navigate into the project directory:

```bash
cd GenAI-Capstone-Project
```

If your repository has a different name, replace the URL and directory name accordingly.

### Step 2: Create a Virtual Environment

On Windows, run:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the required libraries:

```powershell
pip install -r requirements.txt
```

### Step 4: Obtain a Gemini API Key

Create an API key through Google AI Studio:

https://aistudio.google.com/apikey

Follow Google's account, API availability, and usage requirements.

### Step 5: Configure Environment Variables

Create a `.env` file in the project root, alongside `app.py`.

Add:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace the placeholder with your own API key.

**Security warning:** Never publish your API key, share it in screenshots, or commit your `.env` file to GitHub.

The application also allows an API key to be entered through the sidebar for local testing.

### Step 6: Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal. The default address is:

http://localhost:8501

The StudyMate AI interface should now be available in your browser.

---

## 🤖 Google Gemini Model Integration

StudyMate AI integrates Google's Gemini Flash models to power its AI-assisted learning, document research, quiz generation, study planning, and career guidance features.

The project uses two models:

- **Gemini 3.6 Flash:** Used for AI text generation and assistant workflows.
- **Gemini 3.8 Flash:** Used for AI text generation and assistant workflows, following the model configuration update during development.

Using these models provides an opportunity to work with Generative AI APIs, structured prompts, conversational responses, and task-specific AI workflows.

### API Integration

The application uses the Google GenAI Python SDK to communicate with Gemini models.

The text-generation function in `modules/ai_core.py` uses the Interactions API:

```python
def generate_text(client, model_name, prompt):
    response = client.interactions.create(
        model=model_name,
        input=prompt,
    )

    text = getattr(response, "output_text", None)

    if not text:
        raise RuntimeError("The model returned an empty response.")

    return text.strip()
```

The model identifier is supplied to this function through the application configuration.

### Model Configuration

The model selector in `app.py` can be configured to expose both models:

```python
model_name = st.sidebar.selectbox(
    "Gemini model",
    [
        "gemini-3.6-flash",
        "gemini-3.8-flash",
    ],
    index=1,
)
```

**Important:** This configuration assumes that both identifiers are supported by your API account. Confirm the exact model IDs in Google AI Studio before enabling both options. If only Gemini 3.8 Flash is available, retain that model as the sole option until the other identifier is verified.

### Embedding Integration

The PDF question-answering feature uses a separate embedding model and API workflow. Embeddings convert document chunks and user questions into numerical vectors, allowing the application to retrieve relevant passages using cosine similarity.

Text generation and embedding generation are separate operations and should be tested independently.

### Official References

- Gemini API documentation: https://ai.google.dev/gemini-api/docs/get-started
- Google GenAI Python SDK: https://github.com/googleapis/python-genai
- Google AI Studio: https://aistudio.google.com/

Model availability and API behaviour may change over time.

---

## 🧪 Testing and Validation

After installation, test each feature independently.

### AI Chat

- Ask a basic educational question.
- Request a code example.
- Ask a follow-up question.
- Confirm that responses are displayed correctly.

### Study Planner

- Enter multiple subjects.
- Select a deadline and available hours.
- Generate a schedule.
- Verify that the suggested workload is realistic.

### Quiz Generator

- Generate a quiz with five questions.
- Try different difficulty levels.
- Test multiple-choice and short-answer formats.
- Verify that the answer key is included.

### Career Assistant

- Enter a career interest.
- Provide current skills.
- Choose a goal and timeline.
- Check that the roadmap reflects the submitted information.

### PDF Question Answering

- Upload a text-based PDF.
- Process the document.
- Ask a question that can be answered from its content.
- Review the retrieved passages.
- Ask a question that is not covered by the PDF and check whether the assistant acknowledges the limitation.

### Automated Tests

Run the included unit tests:

```powershell
python -m unittest discover -s tests -v
```

These tests validate the deterministic task router and prompt-building helpers. They do not replace integration testing of the Gemini API, embeddings, or Streamlit deployment.

### Final Validation Checklist

- [ ] Application starts successfully.
- [ ] Gemini 3.8 Flash generates responses.
- [ ] Study planner works.
- [ ] Quiz generator works.
- [ ] Career assistant works.
- [ ] PDF text extraction works.
- [ ] Embedding generation and retrieval work.
- [ ] Invalid inputs and API failures are handled.
- [ ] API keys are excluded from source control.
- [ ] Application works from its deployed URL.

---

## 🚀 Deployment on Streamlit Community Cloud

StudyMate AI can be deployed through Streamlit Community Cloud.

### Step 1: Push the Code to GitHub

Ensure that the source files, `requirements.txt`, README, tests, and documentation are committed.

Verify that `.env` and `.venv/` are excluded.

### Step 2: Open Streamlit Community Cloud

Visit:

https://share.streamlit.io/

Sign in with your GitHub account.

### Step 3: Create the Application

Create a new app and select:

- Repository: Your StudyMate AI GitHub repository.
- Branch: `main`.
- Main file path: `app.py`.

### Step 4: Configure Deployment Secrets

Open the app's deployment settings and add your API key through the Secrets configuration.

Use TOML syntax:

```toml
GEMINI_API_KEY = "your_actual_api_key"
```

Do not place the actual key in your README, Python source files, or public repository.

### Step 5: Deploy

Start the deployment and wait for the build to finish.

Open the generated application URL and test AI chat, study planning, quiz generation, career guidance, and PDF processing.

Official deployment guide:

https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

---

## 🔐 Security and Privacy

The application is a learning and demonstration project. Security and privacy should be considered when using or deploying it.

- Keep API credentials in environment variables or deployment secrets.
- Never commit `.env` or secret configuration files.
- Avoid entering passwords, confidential records, or sensitive personal information.
- Remember that prompts and document passages submitted to the AI API are sent to the configured provider for processing.
- Uploaded PDF chunks are retained in the current Streamlit session rather than a permanent document database.
- Public deployment may expose the application to unexpected traffic and API usage.
- API quotas, usage restrictions, and potential charges depend on the provider and account configuration.
- Consider authentication, rate limiting, usage monitoring, and additional access controls before making the application publicly available for production use.

---

## ⚠️ Current Limitations

- AI-generated responses may contain inaccurate information and should be verified.
- PDF retrieval quality depends on text extraction, chunking, embeddings, and semantic similarity.
- Scanned PDFs require OCR support, which is not included.
- Document chunks and chat history are not stored in a persistent database.
- The current task router uses predefined rules and is not a fully autonomous AI agent.
- The application does not guarantee the correctness of career, academic, or technical advice.
- Model availability and API limits depend on Google's current service configuration.

---

## 🔮 Future Enhancements

Possible improvements for future versions include:

- Persistent conversation history and user accounts.
- Page-number citations for document answers.
- OCR for scanned PDFs.
- Improved vector search using a dedicated vector database.
- Model-driven function calling and agent-based workflows.
- Exportable study plans and quizzes.
- Interactive quiz scoring and progress tracking.
- Resume analysis and interview practice.
- Automated evaluation of retrieval quality and answer accuracy.
- Better API usage controls and monitoring.
- Enhanced mobile responsiveness and interface personalisation.

---

## 🎯 Learning Outcomes

Developing StudyMate AI provides practical experience with:

- Generative AI application development.
- LLM API integration using Python.
- Prompt engineering and task-specific prompting.
- Retrieval-Augmented Generation (RAG).
- Text extraction, chunking, embeddings, and vector similarity.
- AI-powered study and career workflows.
- Streamlit interface development.
- Modular Python programming.
- Environment variable management and API key security.
- Unit testing and application troubleshooting.
- Git and GitHub version control.
- Web application deployment and documentation.

---

## 📂 Project Information

**Project Name:** StudyMate AI: AI Study & Career Assistant

**Project Type:** Generative AI Web Application

**Primary Language:** Python

**Interface:** Streamlit

**AI Models:** Google Gemini 3.6 Flash and Gemini 3.8 Flash

**Core Concepts:** LLM APIs, Prompt Engineering, RAG, Embeddings, Vector Similarity, AI Workflows

**Project Context:** GenAI Capstone Project

**Development Environment:** Visual Studio Code

---

## 🔗 Project Links

**GitHub Repository:** [Add your repository link]

**Live Website:** [Add your deployed application link]

**LinkedIn Project Post:** [Add your LinkedIn post link]

---

## 👨‍💻 Author

Rahul Gupta

B.Sc. (Hons) Computer Science | University of Delhi

GitHub: https://github.com/rahulg2004

LinkedIn: https://linkedin.com/in/rg-rr2004

---

## 📜 Disclaimer

StudyMate AI is an educational project developed to demonstrate Generative AI application development and integration. It is intended for learning, experimentation, and demonstration purposes. AI-generated content should be independently verified before being relied upon for important academic, professional, or career decisions.

---

⭐ If you find this project useful, consider starring the repository on GitHub.