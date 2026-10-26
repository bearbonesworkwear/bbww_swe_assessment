"""Offline stand-in for an LLM provider. No API key, network access, or real customer data.

Treat this output as untrusted suggestions, NOT catalog data or authoritative stock.
"""
import json
from pathlib import Path

class MockLLMProvider:
    def __init__(self, data_dir: Path):
        self.responses = json.loads((Path(data_dir)/'mock_llm_responses.json').read_text())

    def suggest_skus(self, message: str) -> dict:
        text = message.lower()
        key = ('boots' if any(t in text for t in ('boot','steel toe','safety toe','waterproof'))
            else 'hi-vis' if any(t in text for t in ('vest','high visibility','high-vis','hi-vis','roadway'))
            else 'uniforms' if any(t in text for t in ('uniform','mechanic','shirt'))
            else 'default')
        return dict(self.responses[key])
