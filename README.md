# Workflow / Graph Engine (FastAPI)

This project implements a minimal **workflow / graph execution engine** using Python and FastAPI.  
It supports **nodes**, **edges**, **shared state transitions**, **branching**, and **looping**.  
A sample **text summarization workflow** is included to demonstrate the engine.

---

## 🚀 Features

- **Graph-based execution**
  - Each node is a Python function  
  - Shared state dictionary passed between nodes  
  - Edges define execution flow  

- **Branching**
  - Nodes can override the next step via `state["next_node"]`

- **Looping**
  - Engine continues until no next node is set

- **Execution logs**
  - Tracks the sequence of executed nodes

- **FastAPI endpoints**
  - Create workflow graphs  
  - Run workflow graphs  
  - Retrieve workflow state

---

## 📦 Project Structure
app/
│── main.py               → FastAPI endpoints
│── engine.py             → Core workflow/graph engine
│── models.py             → Request/response models
│── tools.py              → Helper utilities
│── workflows/
│     └── summarization.py → Example summarization workflow
│
README.md
requirements.txt

## 🧪 Running the Project
### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Start FastAPI server
uvicorn app.main:app --reload

### 3️⃣ Open API documentation
http://127.0.0.1:8000



✨ The root path automatically redirects to `/docs`.

---

## 🧠 API Endpoints

| Endpoint | Description |
|---------|-------------|
| `POST /graph/create` | Register a new workflow graph |
| `POST /graph/run` | Run a workflow with an initial state |
| `GET /graph/state/{run_id}` | Retrieve final state and execution log |

---

## 📝 Example Workflow (Summarization)

### Create Workflow

```json
{
  "nodes": {
    "split_chunks": "split text",
    "summarize_chunks": "summarize each chunk",
    "merge": "merge summaries",
    "refine": "refine output"
  },
  "edges": {
    "split_chunks": "summarize_chunks",
    "summarize_chunks": "merge",
    "merge": "refine",
    "refine": null
  },
  "start_node": "split_chunks"
}

```

### Run Workflow

```json
{
  "graph_id": "your_graph_id_here",
  "initial_state": {
    "text": "This is a long article that needs to be summarized...",
    "length_limit": 200,
    "chunk_size": 300
  }
}
```

### Example Output

```json
{
  "final_state": {
    "text": "This is a long article that needs to be summarized...",
    "length_limit": 200,
    "chunk_size": 300,
    "chunks": [
      "This is a long article that needs to be summarized..."
    ],
    "summaries": [
      "This is a long article that needs to be summarized"
    ],
    "merged_summary": "This is a long article that needs to be summarized",
    "final_summary": "This is a long article that needs to be summarized",
    "summary_length": 50
  },
  "log": [
    "START:split_chunks",
    "END:split_chunks",
    "START:summarize_chunks",
    "END:summarize_chunks",
    "START:merge",
    "END:merge",
    "START:refine",
    "END:refine"
  ]
}
```

## 🛠 Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic

## 🧩 Notes

- The summarization workflow included here is a simple rule-based example to demonstrate node execution.
- The workflow engine is generic and can support any custom workflow by defining node functions and edges.
- The root route (`/`) automatically redirects to `/docs` for easier access to the API documentation.
- Graphs and runs are stored in memory for simplicity (suitable for assignment/demo purposes).
