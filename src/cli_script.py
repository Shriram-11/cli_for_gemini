import google.generativeai as genai
import json
import os
import time
import sys
import threading
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text

# Initialize the Rich console
console = Console()

# Set the configuration file path
CONFIG_FILE = "config.json"


def load_config():
    """Load configuration from the config file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_config(config):
    """Save configuration to the config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)


def set_api_key():
    """Prompt the user to enter their API key and save it."""
    api_key = Prompt.ask("[bold yellow]Please enter your Gemini API key[/]")
    config = load_config()
    config["api_key"] = api_key
    save_config(config)
    console.print("[bold green]API key saved![/]")


def reset_api_key():
    """Reset the API key by removing it from the config file."""
    config = load_config()
    if "api_key" in config:
        del config["api_key"]
        save_config(config)
        console.print("[bold red]API key reset![/]")
    else:
        console.print("[bold red]No API key found to reset.[/]")


def loading_animation(stop_event):
    """Display a loading animation with colors."""
    with Live(console=console, refresh_per_second=10) as live:
        while not stop_event.is_set():
            for char in "|/-\\":
                live.update(Text(f"{char} Loading...", style="bold magenta"))
                time.sleep(0.1)


def generate_response(prompt):
    """Generate a response using the Gemini API."""
    config = load_config()

    if "api_key" not in config:
        console.print(
            "[bold red]API key not set. Please use the setkey command to set your API key.[/]")
        return

    try:
        # Configure the generative AI with the API key
        genai.configure(api_key=config["api_key"])

        # Create a model instance for interacting with the Gemini API
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Create a threading event to stop the loading animation
        stop_event = threading.Event()

        # Start the loading animation in a separate thread
        loading_thread = threading.Thread(
            target=loading_animation, args=(stop_event,))
        loading_thread.start()

        # Make the API call to generate content
        response = model.generate_content(prompt, stream=True)

        # Stop the loading animation after receiving the response
        stop_event.set()
        loading_thread.join()

        # Slight delay to ensure the animation clears properly
        time.sleep(0.1)

        # Display the response in a formatted way
        if response is not None:
            for chunk in response:
                markdown_text = chunk.text.strip()
                console.print(Markdown(markdown_text))

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/]")


def ask_questions():
    """Start a loop where the user can ask questions to the Gemini API."""
    console.print(
        "[bold blue]Ask your questions (type 'exit' or 'quit' to stop):[/]")

    while True:
        prompt = Prompt.ask("\n[bold cyan]> [/]")
        if prompt.lower() in ["exit", "quit"]:
            console.print("[bold yellow]Exiting...[/]")
            break

        if not prompt.strip():
            console.print("[bold red]Please enter a valid prompt.[/]")
            continue

        # Generate a response from the Gemini API
        generate_response(prompt)


def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: gemini-cli <command>[/]")
        return

    command = sys.argv[1]

    if command == "setkey":
        set_api_key()
    elif command == "ask":
        ask_questions()
    elif command == "resetkey":
        reset_api_key()
    else:
        console.print(
            "[bold red]Unknown command. Available commands: setkey, ask, resetkey[/]")


if __name__ == "__main__":
    main()
