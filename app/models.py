from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class GraphCreateRequest(BaseModel):
    # For this assignment we allow user to send a JSON with nodes names only;
    nodes: Dict[str, str]  # name -> description (client-provided)
    edges: Dict[str, Optional[str]]  # name -> next_name
    start_node: Optional[str] = None

class GraphCreateResponse(BaseModel):
    graph_id: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Optional[Dict[str, Any]] = None

class RunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[str]

class RunStateResponse(BaseModel):
    run_id: str
    status: str
    state: Dict[str, Any]
    log: List[str]
