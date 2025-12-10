from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.engine import GraphEngine
from app.models import GraphCreateRequest, GraphCreateResponse, RunRequest, RunResponse, RunStateResponse
from app.workflows.summarization import (build_summarization_graph, node_split_chunks, node_summarize_chunks, node_merge, node_refine,)

app = FastAPI(title="Mini Workflow Engine")

engine = GraphEngine()

# --- Pre-registering a demo summarization graph  ---
demo_graph_id = engine.register_graph(build_summarization_graph())

# node registry: name -> function (for this assignment, only support summarization nodes)
NODE_REGISTRY = {
    "split_chunks": node_split_chunks,
    "summarize_chunks": node_summarize_chunks,
    "merge": node_merge,
    "refine": node_refine,
}


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(req: GraphCreateRequest):
    # Map user-specified node names to actual functions
    try:
        nodes = {name: NODE_REGISTRY[name] for name in req.nodes.keys()}
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown node name '{e.args[0]}'. Allowed: {list(NODE_REGISTRY.keys())}",
        )

    edges = req.edges
    start_node = req.start_node or next(iter(nodes.keys()))

    graph_def = {
        "nodes": nodes,
        "edges": edges,
        "start_node": start_node,
        "max_iterations": 50,
    }

    graph_id = engine.register_graph(graph_def)
    return {"graph_id": graph_id}

@app.post("/graph/run", response_model=RunResponse)
def run_graph(req: RunRequest):
    if not engine.has_graph(req.graph_id):
        raise HTTPException(status_code=404, detail="graph_id not found")
    run_id = engine.start_run(req.graph_id, req.initial_state or {})
    # Run synchronously 
    final_state, log = engine.await_run(run_id)
    return {"run_id": run_id, "final_state": final_state, "log": log}

@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
def get_run_state(run_id: str):
    run = engine.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run_id not found")
    return {
        "run_id": run_id,
        "status": run["status"],
        "state": run["state"],
        "log": run["log"]
    }
