import click
import os
import multiprocessing
from src.dummy_log_generator_file import create_dummy_logs
from src.parser import LogParser
from src.ingestion import KnowledgeBase
from src.agent import TriageAgent

@click.group()
def cli():
    """Agentic RAG Log Triage System CLI Tool."""
    pass

@cli.command()
@click.option('--file', default='data/raw_logs/system_test.log', help='Path to generate the log file.')
@click.option('--size', default=10, help='Target size in MB.')
def generate_logs(file, size):
    """Generate dummy system logs for testing."""
    click.echo(f"Generating {size}MB of logs at {file}...")
    create_dummy_logs(file, size)

@cli.command()
@click.option('--file', required=True, help='Path to the log file to parse.')
@click.option('--severity', help='Filter by severity (e.g., ERROR,FAIL).')
def parse(file, severity):
    """Parse a log file with Intelligence (filtering and trends)."""
    if not os.path.exists(file):
        click.echo(f"Error: File {file} not found.")
        return

    cpu_count = multiprocessing.cpu_count()
    click.echo(f"Parsing log file in parallel ({cpu_count} cores): {file}...")
    parser = LogParser()
    summary = parser.parse_file_parallel(file, filter_severity=severity)
    
    # Sort by count (Failure Density)
    sorted_summary = sorted(summary.items(), key=lambda x: x[1]['count'], reverse=True)

    click.echo(f"\nFound {len(sorted_summary)} Intelligent Patterns (Sorted by Density):\n")
    click.echo(f"{'ID':<5} {'FREQ':<8} {'SEV':<10} {'FIRST LINE (approx)':<20} {'TEMPLATE'}")
    click.echo("-" * 100)
    
    for i, (template, data) in enumerate(sorted_summary, 1):
        loc = f"Chunk {data['chunk_id']}:{data['first_line_in_chunk']}"
        click.echo(f"{i:<5} {data['count']:<8} {data['severity']:<10} {loc:<20} {template}")

@cli.command()
@click.option('--file', required=True, help='Path to the PDF technical manual.')
def ingest(file):
    """Ingest technical manuals into the vector database (FAISS)."""
    if not os.path.exists(file):
        click.echo(f"Error: File {file} not found.")
        return

    click.echo(f"Ingesting manual: {file}...")
    kb = KnowledgeBase()
    num_chunks = kb.ingest_pdf(file)
    click.echo(f"Successfully ingested {num_chunks} chunks into FAISS vector database.")

@cli.command()
@click.option('--file', required=True, help='Path to the log file to analyze.')
@click.option('--output', default='triage_report.md', help='Path to save the Markdown report.')
def analyze(file, output):
    """Run the full Agentic RAG analysis on a log file."""
    if not os.path.exists(file):
        click.echo(f"Error: File {file} not found.")
        return

    click.echo(f"Step 1: Parsing log file in parallel...")
    parser = LogParser()
    # We get the full summary (no initial filter so the agent has full context)
    summary = parser.parse_file_parallel(file)
    
    click.echo(f"Step 2: Synthesizing Intelligent Report via Gemini...")
    agent = TriageAgent()
    report = agent.synthesize_report(summary)
    
    with open(output, 'w') as f:
        f.write(report)
    
    click.echo(f"\n--- Analysis Complete ---")
    click.echo(f"Report saved to: {output}")
    click.echo("\n--- Executive Summary (Preview) ---")
    # Show the first 20 lines of the report as a preview
    click.echo("\n".join(report.split("\n")[:20]))

if __name__ == "__main__":
    cli()
