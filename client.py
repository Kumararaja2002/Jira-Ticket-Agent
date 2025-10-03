import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from langchain_groq import ChatGroq
from langchain.callbacks import StreamlitCallbackHandler

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()
JIRA_SERVER = os.getenv("JIRA_SERVER")  
JIRA_USER = os.getenv("JIRA_USER") 
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN") 

# ---------------------------
# Jira Ticket Creation Function
# ---------------------------
def create_jira_ticket(summary: str, description: str) -> str:
    """Create a Jira ticket directly via REST API."""
    url = f"{JIRA_SERVER}/rest/api/3/issue"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    auth = (JIRA_USER, JIRA_API_TOKEN)

    json_body = {
        "fields": {
            "project": {"key": "JS"},   # <-- change to your actual project key
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Service Request"}   # <-- change if needed
        }
    }

    try:
        response = requests.post(url, headers=headers, json=json_body, auth=auth)
        response.raise_for_status()
        issue_key = response.json().get("key")
        return f"✅ Jira ticket created successfully: {issue_key}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error creating Jira ticket: {str(e)}"


# ---------------------------
# Safe wrapper to prevent multiple tickets
# ---------------------------
ticket_created = {"done": False}

def safe_create_jira_ticket(summary, description) -> str:
    # Fix: Ensure values are plain strings
    if isinstance(summary, dict):
        summary = summary.get("title") or str(summary)
    if isinstance(description, dict):
        description = description.get("title") or str(description)

    if ticket_created["done"]:
        return "⚠️ Ticket already created in this run. Skipping duplicate."
    ticket_created["done"] = True
    return create_jira_ticket(summary, description)


# ---------------------------
# LangChain Setup
# ---------------------------
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

jira_create_tool = StructuredTool.from_function(
    func=safe_create_jira_ticket,
    name="CreateJiraTicket",
    description="Create a new Jira ticket with summary and description. Only one ticket will be created per run."
)

agent = initialize_agent(
    tools=[jira_create_tool],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Jira Agent", page_icon="🤖")
st.title("🤖 Jira Ticket Agent")

st_callback = StreamlitCallbackHandler(st.container())

user_input = st.text_input(
    "Enter your request (e.g. 'Create a Jira ticket with summary Login Bug and description Users cannot log in.')"
)

if user_input:
    # reset ticket_created for each new user request
    ticket_created["done"] = False
    
    with st.spinner("Processing..."):
        response = agent.run(user_input, callbacks=[st_callback])
        st.success(response)
