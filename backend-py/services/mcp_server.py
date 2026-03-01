from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class MCPServer:
    """Model Context Protocol (MCP) server implementation"""
    
    def __init__(self):
        self.tools = self._register_tools()
        self.resources = self._register_resources()
    
    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register available MCP tools"""
        return {
            "search_content": {
                "name": "search_content",
                "description": "Search for content in the Sanity CMS",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "content_type": {"type": "string", "description": "Optional content type filter"},
                        "limit": {"type": "integer", "description": "Maximum results", "default": 10}
                    },
                    "required": ["query"]
                }
            },
            "get_agent_info": {
                "name": "get_agent_info",
                "description": "Get information about an agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "Agent ID"}
                    },
                    "required": ["agent_id"]
                }
            },
            "get_conversation_history": {
                "name": "get_conversation_history",
                "description": "Retrieve conversation history for an agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string", "description": "Agent ID"},
                        "limit": {"type": "integer", "description": "Number of messages", "default": 50}
                    },
                    "required": ["agent_id"]
                }
            }
        }
    
    def _register_resources(self) -> Dict[str, Dict[str, Any]]:
        """Register available MCP resources"""
        return {
            "agents": {
                "uri": "mcp://agents",
                "name": "Agents",
                "description": "List of all available agents",
                "mimeType": "application/json"
            },
            "content": {
                "uri": "mcp://content",
                "name": "Content",
                "description": "Content from Sanity CMS",
                "mimeType": "application/json"
            }
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return list(self.tools.values())
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources"""
        return list(self.resources.values())
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific tool definition"""
        return self.tools.get(tool_name)
    
    def get_resource(self, resource_uri: str) -> Optional[Dict[str, Any]]:
        """Get a specific resource"""
        for resource in self.resources.values():
            if resource["uri"] == resource_uri:
                return resource
        return None
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool"""
        from services.redis_service import redis_service
        from services.sanity_service import sanity_service
        
        if tool_name == "search_content":
            results = await sanity_service.search_content(
                search_term=parameters["query"],
                content_type=parameters.get("content_type"),
                limit=parameters.get("limit", 10)
            )
            return {"success": True, "data": results}
        
        elif tool_name == "get_agent_info":
            agent = redis_service.get_agent(parameters["agent_id"])
            if agent:
                return {"success": True, "data": agent}
            return {"success": False, "error": "Agent not found"}
        
        elif tool_name == "get_conversation_history":
            history = redis_service.get_conversation_history(
                agent_id=parameters["agent_id"],
                limit=parameters.get("limit", 50)
            )
            return {"success": True, "data": history}
        
        return {"success": False, "error": f"Unknown tool: {tool_name}"}
    
    async def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Read an MCP resource"""
        from services.redis_service import redis_service
        
        if resource_uri == "mcp://agents":
            agents = redis_service.get_all_agents()
            return {"success": True, "data": agents}
        
        elif resource_uri == "mcp://content":
            # This would fetch content from Sanity
            return {"success": True, "data": []}
        
        return {"success": False, "error": f"Unknown resource: {resource_uri}"}


# Singleton instance
mcp_server = MCPServer()
