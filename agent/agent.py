from __future__ import annotations

from collections.abc import AsyncGenerator

from agent.events import AgentEvent, AgentEventType
from client.llm_client import LLMClient
from client.response import StreamEventType


class Agent:
    def __init__(self):
        self.client: LLMClient | None = LLMClient()

    async def run(self, message: str) -> AsyncGenerator[AgentEvent, None]:
        yield AgentEvent.agent_start(message)
        final_response:str | None = None
 
        async for event in self._agentic_loop(message):
            yield event
            if event.type == AgentEventType.TEXT_COMPLETE:
                final_response = event.data["content"]

        yield AgentEvent.agent_end(final_response)


    async def _agentic_loop(self, message: str) -> AsyncGenerator[AgentEvent, None]:
        if not self.client:
            yield AgentEvent.agent_error("LLM client is not available")
            return

        messages = [{"role": "user", "content": message}]
        response_text = ""

        async for event in self.client.chat_completion(messages, True):
            if event.type ==  StreamEventType.TEXT_DELTA:
                if event.text_delta:
                    content = event.text_delta.content
                    response_text += content
                    yield AgentEvent.text_delta(content)
            elif event.type == StreamEventType.ERROR:
                yield AgentEvent.agent_error(
                    event.error or "Unknown Error"
                )

        if response_text:
            yield AgentEvent.text_complete(response_text)
    
    async def __aenter__(self) -> Agent:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.client:
            await self.client.close()
            self.client = None
        

        

        


        
