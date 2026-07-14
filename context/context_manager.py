import os
from dotenv import load_dotenv
from prompts.system import get_system_prompt
from typing import List, TypedDict,Any
from dataclasses import dataclass

load_dotenv()


@dataclass
class MessageItem():
    role: str
    content: str
    token_count:int | None =None

    def to_dict(self)->dict[str,Any]:
        result: dict[str,Any] = {"role": self.role}
        if self.content:
            result["content"] = self.content
        return result

@dataclass
class ContextManager:
    def __init__(self)-> None: 
        self._system_prompt:str= get_system_prompt()
        self._messages: List[MessageItem] = []
        self._model_name = os.getenv("MODEL_NAME")


        
    def add_user_message(self,content:str)->None:
        item = MessageItem(
            role="user", 
            content=content,
            token_count=count_tokens(
                content,
                self._model_name,
                ),
            )

        self._messages.append(item)


    def add_assistant_message(self,content:str)->None:
        item = MessageItem(
            role="assistant", 
            content=content or "",
            token_count=count_tokens(
                content,
                self._model_name,
                ),
            )

        self._messages.append(item)

    def get_messages(Self)-> list[dict[str,Any]]:
        messages=[]
        if self._messages:
            messages.append(
                {
                    "role":"system", 
                    "content":self._system_prompt,
                }
            )
        for item in self._messages:
            messages.append(item.to_dict())
            
        return messages

