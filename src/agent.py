import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.ingestion import KnowledgeBase

load_dotenv()

class TriageAgent:
    def __init__(self, model_name="gemini-flash-latest"):
        """
        Initializes the Triage Agent using the raw Google GenAI SDK with high-reliability retries.
        """
        self.kb = KnowledgeBase()
        if not self.kb.load_db():
            print("Warning: Knowledge base not found in data/faiss_db. Please run 'ingest' first.")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment or .env file")

        # Initialize the raw client
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
    def synthesize_report(self, log_summary):
        """
        Takes a summary of log templates, retrieves documentation, and generates a report with retries.
        """
        evidence = []
        critical_patterns = {k: v for k, v in log_summary.items() if v['severity'] in ['ERROR', 'CRITICAL']}
        # Take top 5 to keep prompt size manageable for free tier
        sorted_patterns = sorted(critical_patterns.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
        
        if not sorted_patterns:
            return "# Triage Report\n\nNo critical errors or failures were identified."

        for template, data in sorted_patterns:
            docs = self.kb.query(template, k=1)
            context = "\n".join([doc.page_content for doc in docs])
            
            evidence.append(
                f"Template: {template}\nFrequency: {data['count']}\nSeverity: {data['severity']}\nManual Context: {context}\n"
            )

        evidence_formatted = "\n------------------\n".join(evidence)

        prompt_text = f"""
        You are a Senior Systems Debug Engineer. Analyze these failure patterns and excerpts from the manual.
        
        --- FAILURE EVIDENCE ---
        {evidence_formatted}
        
        --- INSTRUCTIONS ---
        1. Summarize the overall system health.
        2. Provide 'Root Cause' and 'Actionable Fix Steps' grounded ONLY in the documentation provided.
        3. If documentation is missing, state 'Further verification required'.
        
        Format as a professional Markdown report.
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Agent is synthesizing report via Gemini ({self.model_name}) - Attempt {attempt+1}...")
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt_text
                )
                return response.text
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 30
                    print(f"Rate limit hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return f"Error: Synthesis failed. Details: {str(e)}"

if __name__ == "__main__":
    print("Triage Agent Module (Reliable) Ready.")
