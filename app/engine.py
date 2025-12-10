import uuid
from typing import Dict, Any, Optional


class GraphEngine:
    def __init__(self):
        # graphs: graph_id -> graph_def
        # graph_def: {"nodes": {name: callable}, "edges": {name: next_name_or_none}, "start_node": str}
        self.graphs: Dict[str, Dict] = {}
        # runs: run_id -> {"graph_id", "state", "status", "log"}
        self.runs: Dict[str, Dict] = {}

    def register_graph(self, graph_def: Dict) -> str:
        """
        Register a graph definition.
        graph_def must contain:
          - "nodes": dict[name -> callable]
          - "edges": dict[name -> next_name or None]
          - "start_node": str (optional; defaults to first node)
        """
        if "nodes" not in graph_def or "edges" not in graph_def:
            raise ValueError("graph_def must contain 'nodes' and 'edges'")

        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = graph_def
        return graph_id

    def has_graph(self, graph_id: str) -> bool:
        return graph_id in self.graphs

    def _execute_graph(self, graph_id: str, initial_state: Dict[str, Any]):
        """
        Synchronous execution of a graph. No asyncio, no tasks.
        Returns: (final_state, log, status)
        """
        graph = self.graphs[graph_id]
        nodes = graph["nodes"]
        edges = graph["edges"]
        start = graph.get("start_node") or (list(nodes.keys())[0] if nodes else None)
        max_iterations = graph.get("max_iterations", 1000)

        state = initial_state.copy()
        log = []
        status = "running"

        current = start
        iterations = 0

        try:
            while current:
                iterations += 1
                if iterations > max_iterations:
                    status = "failed"
                    log.append("Max iterations exceeded -> possible infinite loop")
                    break

                if current not in nodes:
                    status = "failed"
                    log.append(f"Node '{current}' not found")
                    break

                node_fn = nodes[current]
                log.append(f"START:{current}")
                # Node is a normal sync function
                state = node_fn(state)
                log.append(f"END:{current}")

                # Determine next node
                next_node = state.pop("next_node", None)
                if not next_node:
                    next_node = edges.get(current)

                if callable(next_node):
                    next_node = next_node(state)

                if not next_node:
                    current = None
                else:
                    current = next_node

            if status == "running":
                status = "completed"
        except Exception as e:
            status = "failed"
            log.append(f"Exception: {repr(e)}")

        return state, log, status

    def start_run(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        """
        For simplicity, this executes the graph synchronously
        and stores the result in self.runs.
        """
        run_id = str(uuid.uuid4())
        final_state, log, status = self._execute_graph(graph_id, initial_state)

        self.runs[run_id] = {
            "graph_id": graph_id,
            "state": final_state,
            "status": status,
            "log": log,
        }

        return run_id

    def await_run(self, run_id: str, timeout: Optional[float] = None):
        """
        Kept for API compatibility; since we run synchronously,
        this just returns the stored result.
        """
        run = self.runs.get(run_id)
        if not run:
            raise KeyError("run_id not found")
        return run["state"], run["log"]

    def get_run(self, run_id: str) -> Optional[Dict]:
        return self.runs.get(run_id)
