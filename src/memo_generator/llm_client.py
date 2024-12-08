from typing import List, Dict, Any
import anthropic
from .config import LLMConfig

class ClaudeClient:
    """Client for interacting with Claude API."""
    
    def __init__(self, config: LLMConfig):
        self.client = anthropic.Client(api_key=config.api_key)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Generate text using Claude API."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"Error generating text with Claude: {str(e)}")

    async def analyze_documents(self, documents: List[str], query: str) -> str:
        """Analyze documents with a specific query."""
        combined_docs = "\n\n".join(documents)
        prompt = f"Based on these documents:\n\n{combined_docs}\n\nQuery: {query}"
        
        return await self.generate_text(prompt)

    async def generate_memo_section(self, 
                                  section_name: str, 
                                  context: Dict[str, Any],
                                  language: str = "en") -> str:
        """Generate a specific section of the investment memo."""
        system_prompts = {
            "en": "You are a professional investment analyst writing investment memorandums.",
            "nl": "Je bent een professionele investeringsanalist die investeringsmemoranda schrijft."
        }
        
        system_prompt = system_prompts.get(language, system_prompts["en"])
        
        prompt = f"""Generate the {section_name} section based on this context:
        
        {context}
        
        Requirements:
        1. Use professional financial terminology
        2. Be concise but comprehensive
        3. Include specific data points where available
        4. Maintain a formal tone
        """
        
        return await self.generate_text(prompt, system_prompt)