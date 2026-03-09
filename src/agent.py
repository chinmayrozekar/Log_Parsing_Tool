import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from src.ingestion import KnowledgeBase

class TriageAgent:
    def __init__(self, model_name="qwen2.5-coder:7b"):
        """
        Initializes the Triage Agent using local Ollama with Qwen2.5-Coder.
        This model is best-in-class for technical reasoning and industrial triage.
        """
        self.kb = KnowledgeBase()
        if not self.kb.load_db():
            print("Warning: Knowledge base not found in data/faiss_db. Please run 'ingest' first.")
        
        # Use local Qwen2.5-Coder model for superior technical analysis
        print(f"Initializing local Agentic layer via Ollama ({model_name})...")
        self.llm = OllamaLLM(model=model_name)
        
    def synthesize_report(self, log_summary):
        """
        Takes a summary of log templates, retrieves documentation, and generates a report locally.
        """
        evidence = []
        critical_patterns = {k: v for k, v in log_summary.items() if v['severity'] in ['ERROR', 'CRITICAL']}
        
        # We can handle more patterns locally without network overhead
        sorted_patterns = sorted(critical_patterns.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
        
        if not sorted_patterns:
            return "# Triage Report\n\nNo critical errors or failures were identified in the log analysis."

        for template, data in sorted_patterns:
            # Retrieve relevant documentation from FAISS
            docs = self.kb.query(template, k=2)
            context = "\n".join([doc.page_content for doc in docs])
            
            evidence.append({
                "template": template,
                "count": data['count'],
                "severity": data['severity'],
                "context": context
            })

        # 2. Construct the prompt
        prompt_text = """
        You are a Senior Systems Debug Engineer. Analyze the failure patterns below and provide a triage report.
        
        Below are failure patterns discovered in the system logs, along with technical manual excerpts.
        
        --- FAILURE EVIDENCE ---
        {evidence_formatted}
        
        --- INSTRUCTIONS ---
        1. Summarize overall system health in an 'Executive Summary'.
        2. For each failure pattern, provide a 'Root Cause' based on the manual context.
        3. Identify if the failure is 'Systematic' or 'Sporadic'.
        4. Provide specific 'Actionable Fix Steps' grounded ONLY in the documentation provided.
        
        Format the output as a professional Markdown report.
        """
        
        evidence_formatted = ""
        for ev in evidence:
            evidence_formatted += f"\nTemplate: {ev['template']}\nFrequency: {ev['count']}\nSeverity: {ev['severity']}\nManual Context: {ev['context']}\n------------------\n"

        prompt = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt | self.llm
        
        print(f"Agent is synthesizing local report via Ollama...")
        response = chain.invoke({"evidence_formatted": evidence_formatted})
        return response

if __name__ == "__main__":
    print("Local Triage Agent Module Ready.")
