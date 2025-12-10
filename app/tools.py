# Simple tool registry. Nodes can import and call tools from here.
def simple_chunk(text: str, chunk_size: int = 200):
    # naive split by characters 
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def naive_summarize(chunk: str, max_words: int = 30):
    # extremely simple summarizer
    if "." in chunk:
        sentence = chunk.split(".")[0].strip()
        if sentence:
            words = sentence.split()
            return " ".join(words[:max_words])
    words = chunk.split()
    return " ".join(words[:max_words])

def merge_summaries(summaries):
    text = " ".join(summaries)
    return " ".join(text.split())
