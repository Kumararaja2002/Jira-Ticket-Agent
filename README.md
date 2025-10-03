# 🤖 Jira Ticket Agent with LangChain & Groq

This project is a Streamlit-based AI assistant that allows users to create Jira tickets using natural language. It uses LangChain's structured agent, Groq's LLaMA3.1-8B model, and Jira's REST API to automate ticket creation securely and efficiently.

## 🚀 Features

- Natural language interface to create Jira tickets
- Uses LangChain's `StructuredTool` and `initialize_agent`
- Powered by Groq's LLaMA3.1-8B model
- Prevents duplicate ticket creation per session
- Streamlit UI with real-time feedback

## 🧠 Technologies Used

- LangChain
- Groq API (LLaMA3.1-8B)
- Jira REST API
- Streamlit
- Python
- dotenv
- requests

## 📁 File Structure

- `client.py`: Main Streamlit application
- `.env`: Stores Jira credentials and server URL

## 🔐 Environment Variables

Create a `.env` file with the following keys:

JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USER=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token

## 🛠️ How to Run

1. Clone the repository:
```
git clone https://github.com/yourusername/jira-agent-chatbot.gitcd jira-agent-chatbot
```
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Add your .env file with Jira credentials.


4. Run the Streamlit app:
```
streamlit run app.py
```
