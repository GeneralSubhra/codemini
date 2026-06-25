from rich.console import Console
from rich.theme import Theme
from rich.rule import Rule
from rich.text import Text

AGENT_THEME = Theme(
    {
        "info": "#4FD9FF",         
        "warning": "#FFD866",
        "error": "bold #FF5F56",
        "success": "bold #7FFF3A",   
        "dim": "grey50",
        "muted": "grey62",
        "border": "#1E4D2B",         
        "highlight": "bold #A8FF60", 
        "user": "bold #4FD9FF",
        "assistant": "#F8FAFC",
        "tool": "bold #8A5CFF",     
        "tool.read": "#4FD9FF",
        "tool.write": "#FFD866",
        "tool.shell": "bold #7FFF3A",
        "tool.network": "#4FD9FF",
        "tool.memory": "#5FE35A",
        "tool.mcp": "#80E8FF",
        "code": "#F8FAFC",
    }
)
_console:Console|None=None

def get_console()->Console:
    global _console
    if _console is None:
        _console = Console(theme=AGENT_THEME,highlight=False)
    return _console

class Renderer:
    def __init__(self,console:Console|None=None)->None:
        self.console=console or get_console()
        self._assistant_stream_open = False 
    
    def begin_assistant(self)->None:
        self.console.print()
        self.console.print(Rule(Text("CodeMini",style="assistant")))
        self._assistant_stream_open = True

    def end_assistant(self)->None:
        if self._assistant_stream_open:
            self.console.print()
        self._assistant_stream_open = False
            
    def stream_assistant_delta(self,content:str)->None:
        self.console.print(content,end="",markup=False)  

