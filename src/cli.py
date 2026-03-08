import click
import os
from src.dummy_log_generator_file import create_dummy_logs
from src.parser import LogParser
from src.ingestion import KnowledgeBase

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
def parse(file):
    """Parse a log file using Drain3 to extract templates."""
    if not os.path.exists(file):
        click.echo(f"Error: File {file} not found.")
        return

    click.echo(f"Parsing log file: {file}...")
    parser = LogParser()
    # Handle the generator output
    for result in parser.parse_file(file):
        pass # We just want the summary for now
    
    summary = parser.get_summary()
    click.echo(f"\nDiscovered {len(summary)} Unique Log Templates:\n")
    for s in summary:
        click.echo(f"ID {s['id']} (Count: {s['count']}): {s['template']}")

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
def analyze():
    """[Placeholder] Run the full Agentic RAG analysis on a log file."""
    click.echo("Synthesis module coming soon.")

if __name__ == "__main__":
    cli()
