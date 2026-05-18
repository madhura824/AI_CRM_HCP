# AI-CRM-HCP

An AI-first CRM system designed for Healthcare Professional (HCP) interaction management.
The system enables pharmaceutical and life-science field representatives to log interactions with doctors/HCPs using either:

* A structured form interface
* A conversational AI chat interface

The application leverages LLMs, LangGraph workflows, FastAPI backend services, and a React + Redux frontend to create an intelligent CRM experience.

---

# 🎥 Project Demonstration Links

## 🚀 Portal Working Demo
Watch the complete working demonstration of the AI-CRM-HCP platform:

🔗 https://www.loom.com/share/eedd159cf7734d00b3a28360767412a6

---

## 🧠 Code Explanation Demo
Detailed walkthrough of the project architecture, backend workflow, LangGraph implementation, and codebase explanation:

🔗 https://www.loom.com/share/fc5cc359122c42a4b458c7dd81ea5716

---

# Objective

The goal of this project is to conceptualize and build an AI-powered Customer Relationship Management (CRM) module focused on Healthcare Professionals (HCPs).

The system is designed from the perspective of a pharmaceutical/life-science field representative and provides intelligent assistance for:

* Logging HCP interactions
* Updating previous interactions
* Managing samples distributed
* Tracking sentiments and outcomes
* Generating AI-based follow-up suggestions
* Creating downloadable interaction artifacts (PDFs)

---

# Core Features

## Structured Form Logging

Users can manually fill interaction details using a structured form UI.

## Conversational AI Logging

Users can interact naturally using chat prompts such as:

"Dr Raj visited today and discussed fever treatment."

The AI extracts:

* HCP Name
* Interaction Type
* Date
* Topics Discussed
* Samples Distributed
* Sentiment
* Follow-up Actions

and automatically populates the CRM form.

## AI-Powered Followup Suggestions

The system intelligently recommends:

* Next follow-up meetings
* Brochure sharing
* Discussion points
* Future actions

## Artifact Generation

The system generates downloadable PDF reports for:

* Samples distributed
* Structured medicine/sample information

## Intelligent Form Updates

Supports:

* Add
* Update
* Merge
* Append
* Delete
* Replace
* Artifact generation

---

# Tech Stack

## Frontend

* React.js
* Redux Toolkit
* Tailwind CSS
* Google Inter Font

## Backend

* Python
* FastAPI

## AI / LLM Stack

* LangGraph
* Groq API
* gemma2-9b-it
* llama-3.3-70b-versatile
* llama-3.1-8b-instant

## Database

* MySQL / PostgreSQL

## PDF Generation

* Python PDF Generator Service

---

# LLM Configuration

The project uses Groq-hosted LLMs.

Example configuration:

```python
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
```

Primary models:

* gemma2-9b-it
* llama-3.3-70b-versatile
* llama-3.1-8b-instant

---

# Project Architecture

The system follows an AI-agent workflow architecture using LangGraph.

```text
User Input
   ↓
LLM Node
   ↓
Executor Node
   ↓
Followup Node
   ↓
Frontend Response
```

---

# LangGraph Workflow

## Graph Definition

```python
builder.add_node("llm", llm_node)
builder.add_node("execute", executor_node)
builder.add_node("followup", followup_node)

builder.set_entry_point("llm")

builder.add_edge("llm", "execute")
builder.add_edge("execute", "followup")
builder.add_edge("followup", END)
```

---

# LangGraph Nodes / States

The system consists of 3 primary states (nodes).

---

## 1. llm_node (Entry Node)

### Purpose

The entry point of the AI workflow.

### Responsibilities

* Accept user prompt
* Create LLM prompt
* Send request to Groq LLM
* Extract structured interaction information
* Detect user action

### Example

Input:

```text
Dr Raj visited today and discussed fever treatment.
```

LLM Extracted Payload:

```json
{
  "hcp_name": "Dr Raj",
  "interaction_type": "visit",
  "topics_discussed": ["fever treatment"]
}
```

---

## 2. executor_node

### Purpose

Responsible for business logic execution and form population.

### Responsibilities

* Extract information from LLM response
* Normalize fields
* Merge/replace/update values
* Populate frontend form structure
* Generate artifacts
* Apply CRUD operations

### Core Service

```python
apply_action()
```

### Example Responsibilities

* Merge topics discussed
* Replace HCP name
* Append followup actions
* Delete specific values
* Generate PDFs

---

## 3. followup_node

### Purpose

Makes the AI agent behave intelligently rather than returning machine-like responses.

### Responsibilities

* Create follow-up prompt
* Send interaction summary to LLM
* Generate intelligent next-step suggestions

### Example Suggestions

* Schedule next meeting
* Share updated brochure
* Discuss dosage effectiveness

### UI Output

Displayed under:

```text
AI Suggested Followups
```

---

# Actions Supported

The CRM supports multiple intelligent actions.

---

## 1. ADD Action

Adds extracted information into CRM fields.

### Example

```text
Dr Raj discussed diabetes treatment.
```

Result:

```json
{
  "topics_discussed": ["diabetes treatment"]
}
```

---

## 2. UPDATE Action

Used for modifying existing values.

### Supports

### Overwrite

Used for single-value fields.

Example:

```text
Change interaction type to meeting.
```

### Merge

Used for multi-value fields.

Example:

```text
Add fever discussion.
```

### Append

Adds additional list values.

Example:

```text
Add Parafast-500 sample.
```

---

## 3. DELETE Action

Used for:

* Single value deletion
* Complete field deletion
* Group deletion

### Examples

```text
Delete fever topic.
```

```text
Clear materials shared.
```

---

## 4. GENERATE_ARTIFACT Action

Used for generating downloadable PDF reports.

### Purpose

When the user provides:

* Medicine names
* Sample names
* Quantities

The system:

1. Extracts structured sample data
2. Generates PDF content
3. Creates downloadable PDF
4. Attaches artifact to frontend UI

### PDF Service

```python
pdf_generator.py
```

### Features

* Dynamic PDF generation
* Download support
* Artifact updates supported

---

# LangGraph Tools Used

The LangGraph AI agent uses multiple internal tools/services.

## 1. Log Interaction Tool

Captures HCP interaction details using LLM extraction.

## 2. Edit Interaction Tool

Updates/modifies previously logged interaction data.

## 3. Sentiment Analysis Tool

Infers HCP sentiment:

* positive
* neutral
* negative

## 4. Artifact Generation Tool

Creates downloadable PDF reports for samples distributed.

## 5. Followup Recommendation Tool

Generates AI-based next-step suggestions.

---

# Backend Structure

```text
backend/
│
├── app/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │
│   ├── llm/
│   │   ├── prompts.py
│   │   ├── groq_client.py
│   │
│   ├── schemas/
│   │   ├── agent_schema.py
│   │
│   ├── services/
│   │   ├── executor.py
│   │   ├── pdf_generator.py
│   │   ├── sentiment.py
│   │
│   ├── files/
│
├── main.py
```

---

# Frontend Structure

```text
frontend/
│
├── src/
│   ├── components/
│   ├── redux/
│   ├── pages/
│   ├── styles/
│   ├── App.tsx
```

---

# Important Backend Files

## prompts.py

Contains:

* SYSTEM_PROMPT
* FOLLOWUP_PROMPT

Used to instruct the LLM.

---

## executor.py

Contains:

* Business logic
* Field normalization
* Merge/update/delete logic
* Artifact handling

---

## nodes.py

Contains:

* llm_node
* executor_node
* followup_node

Defines LangGraph node behavior.

---

## graph.py

Defines:

* Graph structure
* Node flow
* Execution pipeline

---

## routes.py

Defines FastAPI endpoints.

Main endpoint:

```python
POST /agent
```

Responsible for:

* Receiving frontend requests
* Invoking LangGraph workflow
* Returning AI-generated response

---

# API Flow

```text
Frontend
   ↓
POST /agent
   ↓
LangGraph Workflow
   ↓
LLM Extraction
   ↓
Executor Processing
   ↓
Followup Generation
   ↓
Frontend UI Update
```

---

# Running the Backend

## Step 1: Navigate to Backend

```bash
cd backend
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

## Step 3: Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

## Step 6: Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# Running the Frontend

## Step 1: Navigate to Frontend

```bash
cd frontend
```

## Step 2: Install Dependencies

```bash
npm install
```

## Step 3: Start Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# Example Prompt

```text
Dr Raj visited today for a meeting. He discussed fever and cold treatments. He shared Parafast-500 samples.
```

---

# Example AI Output

```json
{
  "hcp_name": "Dr Raj",
  "interaction_type": "visit",
  "topics_discussed": [
    "fever",
    "cold treatments"
  ]
}
```

---

# Future Enhancements

* Database persistence
* Authentication & RBAC
* Multi-agent workflows
* Voice-based interaction logging
* Analytics dashboard
* HCP recommendation engine
* Email integration
* Calendar scheduling
* Notification system

---

# Conclusion

AI-CRM-HCP demonstrates how modern LLMs, LangGraph workflows, and AI-assisted automation can transform traditional CRM systems into intelligent healthcare engagement platforms.

The project combines:

* Conversational AI
* Structured data extraction
* Workflow orchestration
* Intelligent recommendations
* Artifact generation

to create an AI-first CRM experience for life-science and pharmaceutical field representatives.
