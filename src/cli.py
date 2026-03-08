import click
import os
from src.dummy_log_generator_file import create_dummy_logs
from src.parser import LogParser

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
    parser.parse_file(file)
    
    summary = parser.get_summary()
    click.echo(f"\nDiscovered {len(summary)} Unique Log Templates:\n")
    for s in summary:
        click.echo(f"ID {s['id']} (Count: {s['count']}): {s['template']}")

@cli.command()
def ingest():
    """[Placeholder] Ingest technical manuals into the vector database."""
    click.echo("Ingestion module coming soon (PDF manuals required).")

@cli.command()
def analyze():
    """[Placeholder] Run the full Agentic RAG analysis on a log file."""
    click.echo("Synthesis module coming soon.")

if __name__ == "__main__":
    cli()
