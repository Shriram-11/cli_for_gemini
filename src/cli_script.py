import json
import time
import sys
import threading
from google import genai
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
    """Generate a response using the NEW Google GenAI SDK syntax."""
    config = load_config()

    if "api_key" not in config:
        console.print(
            "[bold red]Error: API key not set. Use 'setkey' first.[/]")
        return

    try:
        # Initialize Client
        client = genai.Client(api_key=config["api_key"])

        stop_event = threading.Event()
        loading_thread = threading.Thread(
            target=loading_animation, args=(stop_event,))
        loading_thread.start()

        # FIX 1: Use generate_content_stream() instead of generate_content(stream=True)
        response = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt
        )

        stop_event.set()
        loading_thread.join()

        full_response = ""
        console.print("\n[bold green]Gemini:[/]")

        with Live(console=console, vertical_overflow="visible") as live:
            for chunk in response:
                # FIX 2: Handle the tuple wrapper if the SDK yields one
                # This fixes the "'tuple' object has no attribute 'text'" error
                item = chunk[0] if isinstance(chunk, tuple) else chunk

                if hasattr(item, 'text') and item.text:
                    full_response += item.text
                    live.update(Markdown(full_response))

    except Exception as e:
        if 'stop_event' in locals():
            stop_event.set()
        console.print(f"[bold red]Error: {e}[/]")


def ask_questions():
    """Interactive loop for asking questions."""
    console.print("[bold blue]Ask your questions (type 'exit' to leave):[/]")
    while True:
        prompt = Prompt.ask("\n[bold cyan]> [/]")
        if prompt.lower() == "exit":
            break
        if not prompt.strip():
            continue
        generate_response(prompt)


def show_help():
    """Display help information."""
    help_text = """[green]
    Gemini CLI - 2026 Edition (v2.1)
    Commands: setkey, ask, resetkey, help, quit
    [/]"""
    console.print(help_text)


def interactive_mode():
    """Main interactive menu."""
    console.print(
        "[bold green]Gemini CLI Active. Type 'help' for commands.[/]")
    while True:
        cmd = input('\n> ').strip().lower()
        if cmd in ["quit", "exit"]:
            break
        elif cmd == "setkey":
            set_api_key()
        elif cmd == "ask":
            ask_questions()
        elif cmd == "resetkey":
            reset_api_key()
        elif cmd == "help":
            show_help()
        elif not cmd:
            continue
        else:
            console.print("[bold red]Unknown command.[/]")


def main():
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        command = sys.argv[1].lower()
        if command == "setkey":
            set_api_key()
        elif command == "ask":
            ask_questions()
        elif command == "resetkey":
            reset_api_key()
        elif command == "help":
            show_help()
        else:
            console.print("[bold red]Unknown command.[/]")


if __name__ == "__main__":
    main()
