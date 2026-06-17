from rich.console import Console


def get_console() -> Console:
    return Console()


class Renderer:
    def __init__(self, console: Console) -> None:
        self.console = console

    def stream_assistant_delta(self, content: str) -> None:
        self.console.print(content, end="")

    def finish_stream(self) -> None:
        self.console.print()

    def render_error(self, message: str) -> None:
        self.console.print(f"[red]Error:[/red] {message}")
