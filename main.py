import asyncio
import sys

import click

from agent.agent import Agent
from agent.events import AgentEventType
from ui.renderer import Renderer, get_console

 
class CLI:
    def __init__(self):
        self.agent: Agent | None = None
        self.renderer = Renderer(get_console())

    async def run_single(self, message: str) -> str | None:
        async with Agent() as agent:
            self.agent = agent
            return await self._process_message(message)

    async def _process_message(self, message: str) -> str | None:
        if not self.agent:
            return None

        response_text = ""
        async for event in self.agent.run(message):
            if event.type == AgentEventType.TEXT_DELTA:
                content = event.data.get("content", "")
                response_text += content
                self.renderer.stream_assistant_delta(content)
            elif event.type == AgentEventType.AGENT_ERROR:
                self.renderer.render_error(event.data.get("error", "Unknown error"))
                return None

        self.renderer.finish_stream()
        return response_text



@click.command()
@click.argument("prompt", required=False)
def main(
    prompt: str | None
):
    cli = CLI()
    if prompt:
        result=asyncio.run(cli.run_single(prompt))
        if result is None:
            sys.exit(1)


if __name__ == "__main__":
    main()

