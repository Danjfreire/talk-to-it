import asyncio
import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models.base import BaseChatModel
from characters.character import Character

class ConversationService:
    def __init__(self, llm_model: BaseChatModel, character: Character):
        self.llm_model = llm_model
        self.character = character
    
    async def handle_prompt(self, prompt: str) -> str:
        # TODO: Add conversation history
        start_time = time.perf_counter()
        loop = asyncio.get_event_loop()

        character_desc = f""" 
            Act as the following character:
            {self.character.description}
            You should try to respond the questions, but stay in character.
            Your answers should not include any code block or markdown. Answer with sentences like a human would and use up to 1000 characters.
        """

        messages = [
            SystemMessage(content=character_desc),
            HumanMessage(content=prompt)
        ]

        res = await loop.run_in_executor(
            None,
            lambda: self.llm_model.invoke(messages)
        ) 

        ai_text = res.content
        end_time = time.perf_counter()
        print(f"AI response: {ai_text}")
        print(f"LLM response generation took {end_time - start_time:.2f} seconds")

        return ai_text
