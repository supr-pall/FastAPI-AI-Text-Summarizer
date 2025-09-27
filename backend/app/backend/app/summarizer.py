from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class Summarizer:
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-12-6", device: int = -1):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.pipe = pipeline("summarization", model=self.model, tokenizer=self.tokenizer, device=device)

    def chunk_text(self, text: str, max_tokens: int = 800) -> list:
        words = text.split()
        chunks, current = [], []
        for w in words:
            current.append(w)
            if len(current) >= max_tokens:
                chunks.append(" ".join(current))
                current = []
        if current:
            chunks.append(" ".join(current))
        return chunks

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        text = text.strip()
        if not text:
            return ""
        chunks = self.chunk_text(text, max_tokens=800)
        summaries = []
        for chunk in chunks:
            out = self.pipe(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(out[0]["summary_text"])
        if len(summaries) == 1:
            return summaries[0].strip()
        combined = " ".join(summaries)
        final = self.pipe(combined, max_length=max_length, min_length=min_length, do_sample=False)
        return final[0]["summary_text"].strip()
