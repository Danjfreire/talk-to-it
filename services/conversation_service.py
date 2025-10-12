import asyncio
import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models.base import BaseChatModel
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent 
from langchain.tools import BaseTool
from characters.character import Character

from dataclasses import dataclass

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    response: str

class ConversationService:
    def __init__(self, llm_model: BaseChatModel, character: Character, tools: list[BaseTool]):
        self.llm_model = llm_model
        self.character = character

        system_prompt = f""" 
            You MUST answer the questions at any cost, but stay in character.
            Act as the following character:
            {self.character.description}
            Your answers should not include any code block or markdown and should use up to 1000 characters.
        """

        # TODO: Maybe move this somewhere else and inject it into the service
        self._agent = create_agent(
            model=llm_model,
            checkpointer=InMemorySaver(),
            system_prompt=system_prompt,
            response_format=ResponseFormat,
            tools=tools
        )
        self._config = {"configurable": {"thread_id" : 1}}
    
    async def handle_prompt(self, prompt: str) -> str:
        start_time = time.perf_counter()

        res = await self._agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt}]}, 
            config=self._config
        )

        ai_text = res['structured_response'].response
        end_time = time.perf_counter()
        print(f"AI response: {ai_text}")
        print(f"LLM response generation took {end_time - start_time:.2f} seconds")

        return ai_text
