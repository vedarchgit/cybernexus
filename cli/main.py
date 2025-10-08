import typer
import requests
import json
from typing_extensions import Annotated

app = typer.Typer(
    help="CyberNexus CLI - A command-line interface for the CyberNexus Threat Intelligence Platform."
)

API_URL = "http://localhost:8000"

@app.command(
    help="Search for threats. You can filter by indicator, type, or source."
)
def search(
    indicator: Annotated[str, typer.Option(help="Indicator to search for (e.g., an IP or domain).")] = None,
    type: Annotated[str, typer.Option(help="Type of threat to search for (e.g., phishing).")] = None,
    source: Annotated[str, typer.Option(help="Source of the threat intelligence.")] = None,
):
    """Search for threats in the CyberNexus database."""
    params = {}
    if indicator:
        params["indicator"] = indicator
    if type:
        params["type"] = type
    if source:
        params["source"] = source

    try:
        response = requests.get(f"{API_URL}/threats/", params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        if not data:
            typer.echo("No threats found matching the criteria.")
            return

        # Pretty-print the JSON output
        typer.echo(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error connecting to the CyberNexus API: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command(
    help="Submit a new threat to the database."
)
def submit(
    indicator: Annotated[str, typer.Argument(help="The threat indicator (e.g., IP, URL, hash).")],
    type: Annotated[str, typer.Argument(help="The type of threat (e.g., phishing, malware).")],
    source: Annotated[str, typer.Argument(help="The source of this threat intelligence.")],
):
    """Submit a new threat to the CyberNexus database."""
    threat_data = {"indicator": indicator, "type": type, "source": source}
    try:
        response = requests.post(f"{API_URL}/threats/", json=threat_data)
        response.raise_for_status()
        
        data = response.json()
        typer.secho(f"Successfully submitted threat: {data['id']}", fg=typer.colors.GREEN)
        typer.echo(json.dumps(data, indent=2))

    except requests.exceptions.RequestException as e:
        typer.secho(f"Error connecting to the CyberNexus API: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
