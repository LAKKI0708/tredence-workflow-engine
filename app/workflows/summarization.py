from typing import Dict, Any, List
from app.tools import simple_chunk, naive_summarize, merge_summaries


def node_split_chunks(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("text", "")
    chunk_size = state.get("chunk_size", 300)
    chunks = simple_chunk(text, chunk_size)
    state["chunks"] = chunks
    return state


def node_summarize_chunks(state: Dict[str, Any]) -> Dict[str, Any]:
    chunks: List[str] = state.get("chunks", [])
    summaries: List[str] = []

    for ch in chunks:
        s = naive_summarize(ch, max_words=40)
        summaries.append(s)

    state["summaries"] = summaries
    return state


def node_merge(state: Dict[str, Any]) -> Dict[str, Any]:
    summaries = state.get("summaries", [])
    merged = merge_summaries(summaries)
    state["merged_summary"] = merged
    return state


def node_refine(state: Dict[str, Any]) -> Dict[str, Any]:
    merged = state.get("merged_summary", "")
    limit = state.get("length_limit", 200)  # char limit

    if len(merged) <= limit:
        state["final_summary"] = merged
    else:
        trimmed = merged[:limit]
        if " " in trimmed:
            trimmed = trimmed.rsplit(" ", 1)[0]
        state["final_summary"] = trimmed + "..."

    state["summary_length"] = len(state["final_summary"])

    # Simple loop/branch: if still too long, loop back to summarize_chunks
    if state["summary_length"] <= state.get("length_limit", 200):
        state["next_node"] = None  
    else:
        state["next_node"] = "summarize_chunks"
        state["chunk_size"] = max(100, int(state.get("chunk_size", 300) * 0.7))

    return state


def build_summarization_graph():
    nodes = {
        "split_chunks": node_split_chunks,
        "summarize_chunks": node_summarize_chunks,
        "merge": node_merge,
        "refine": node_refine,
    }

    edges = {
        "split_chunks": "summarize_chunks",
        "summarize_chunks": "merge",
        "merge": "refine",
        "refine": None,  # engine stops here unless state["next_node"] overrides it
    }

    return {
        "nodes": nodes,
        "edges": edges,
        "start_node": "split_chunks",
        "max_iterations": 50,
    }
