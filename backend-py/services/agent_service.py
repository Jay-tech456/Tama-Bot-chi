from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import List, Dict, Any, Optional
from config import settings
from services.redis_service import redis_service
from services.sanity_service import sanity_service


class AgentService:
    """LangChain and Claude integration service"""
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            anthropic_api_key=settings.anthropic_api_key,
            max_tokens=4096,
            temperature=0.7
        )
    
    def _create_llm_for_agent(self, temperature: float, max_tokens: int) -> ChatAnthropic:
        """Create a custom LLM instance for specific agent settings"""
        return ChatAnthropic(
            model=settings.claude_model,
            anthropic_api_key=settings.anthropic_api_key,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def _build_messages(
        self,
        system_prompt: Optional[str],
        conversation_history: List[Dict[str, Any]],
        user_message: str
    ) -> List:
        """Build message list for Claude"""
        messages = []
        
        # Add system message if provided
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        # Add conversation history
        for msg in conversation_history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        return messages
    
    async def chat(
        self,
        agent_id: str,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
        use_sanity_content: bool = False
    ) -> str:
        """Process a chat message with the agent"""
        
        # Get agent configuration
        agent = redis_service.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Get conversation history
        conversation_history = redis_service.get_conversation_history(agent_id)
        
        # Enhance message with Sanity content if requested
        enhanced_message = user_message
        if use_sanity_content and context and context.get("search_term"):
            sanity_content = await sanity_service.search_content(
                search_term=context["search_term"],
                content_type=context.get("content_type"),
                limit=5
            )
            if sanity_content:
                content_summary = self._format_sanity_content(sanity_content)
                enhanced_message = f"{user_message}\n\nRelevant content from knowledge base:\n{content_summary}"
        
        # Build messages for Claude
        messages = self._build_messages(
            system_prompt=agent.get("system_prompt"),
            conversation_history=conversation_history,
            user_message=enhanced_message
        )
        
        # Create LLM with agent-specific settings
        llm = self._create_llm_for_agent(
            temperature=agent.get("temperature", 0.7),
            max_tokens=agent.get("max_tokens", 4096)
        )
        
        # Get response from Claude
        response = await llm.ainvoke(messages)
        response_text = response.content
        
        # Save conversation to Redis
        redis_service.save_message(agent_id, "user", user_message)
        redis_service.save_message(agent_id, "assistant", response_text)
        
        return response_text
    
    def _format_sanity_content(self, content: List[Dict[str, Any]]) -> str:
        """Format Sanity content for context"""
        formatted = []
        for item in content:
            title = item.get("title", "Untitled")
            description = item.get("description", "")
            formatted.append(f"- {title}: {description}")
        return "\n".join(formatted)
    
    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """Generate a one-off completion without conversation history"""
        llm = self._create_llm_for_agent(temperature, max_tokens)
        messages = [HumanMessage(content=prompt)]
        response = await llm.ainvoke(messages)
        return response.content


# Singleton instance
agent_service = AgentService()
