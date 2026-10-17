# StudyMate AI Architecture

## Main components

1. **Streamlit interface:** collects user input and renders responses.
2. **Gemini generation client:** sends task-specific prompts to the configured Gemini model.
3. **PDF ingestion:** extracts selectable text from PDFs and splits it into overlapping chunks.
4. **Embedding and retrieval:** uses Gemini embeddings and NumPy cosine similarity to retrieve passages relevant to a question.
5. **Task-specific tools:** study-plan and quiz prompt builders structure tasks for the model.
6. **Career workflow:** creates a roadmap from the user's stated interests, skills, goal, and timeline.

## Data flow

The user selects a feature in the Streamlit interface. The application validates required input, constructs a feature-specific prompt, and sends the prompt to Gemini. For PDF questions, the application first retrieves relevant passages and includes them in the prompt. The generated response is displayed in the interface.

## Security considerations

- API keys are read from environment variables or Streamlit secrets.
- `.env` is excluded from Git.
- Uploaded document content is handled in session memory in this version.
- Production deployments should add authentication, rate limits, logging policies, and abuse controls as needed.