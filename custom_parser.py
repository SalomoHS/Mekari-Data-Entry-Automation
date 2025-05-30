# main.py
import argparse
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import sys

console = Console()

class RichArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        console.print(Panel.fit(f"[bold red]Error:[/] {message}", title="❌ Argument Error",border_style="red"))
        self.print_help()
        exit(2)
    
    def print_help(self):
        help_text = Text()
        help_text.append("🚀 ", style="bold yellow")
        help_text.append("Usage:\n", style="bold underline cyan")
        help_text.append(f"  python {sys.argv[0]} ", style="green")

        # Add usage dynamically
        for action in self._actions:
            if action.option_strings:
                help_text.append("[" + "/".join(action.option_strings) + "] ", style="green")
            else:
                help_text.append(f"{action.dest} ", style="green")
        help_text.append("\n\n")

        help_text.append("📦 Options:\n", style="bold underline cyan")
        for action in self._actions:
            if action.help == argparse.SUPPRESS:
                continue
            opts = ", ".join(action.option_strings) if action.option_strings else action.dest
            help_text.append(f"  {opts:15} ", style="yellow")
            help_text.append(f"{action.help or ''}\n")

        console.print(Panel.fit(help_text, title="🆘 Help", border_style="blue"))


# Use it like the normal parser
def parser():
    parser = RichArgumentParser()

    parser.add_argument('--cardname', type=str, required=True, help="'card name' value")
    parser.add_argument('--number', type=int, required=True, help="number of automation task")
    parser.add_argument('--ib', type=int, required=True, help="'initial balance' value")
    
    args = parser.parse_args()

    return args