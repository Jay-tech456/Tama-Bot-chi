import httpx
from typing import Optional, List, Dict, Any
from config import settings


class SanityService:
    """Sanity CMS service for content management"""
    
    def __init__(self):
        self.project_id = settings.sanity_project_id
        self.dataset = settings.sanity_dataset
        self.api_version = settings.sanity_api_version
        self.token = settings.sanity_token
        self.base_url = f"https://{self.project_id}.api.sanity.io/{self.api_version}"
    
    async def query(self, groq_query: str) -> Optional[Dict[str, Any]]:
        """Execute a GROQ query against Sanity"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/data/query/{self.dataset}",
                    params={"query": groq_query},
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error querying Sanity: {e}")
            return None
    
    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        query = f'*[_id == "{document_id}"][0]'
        result = await self.query(query)
        return result.get("result") if result else None
    
    async def get_documents_by_type(self, doc_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get documents by type"""
        query = f'*[_type == "{doc_type}"][0...{limit}]'
        result = await self.query(query)
        return result.get("result", []) if result else []
    
    async def search_content(self, search_term: str, content_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search content in Sanity"""
        if content_type:
            query = f'*[_type == "{content_type}" && [title, description, content] match "*{search_term}*"][0...{limit}]'
        else:
            query = f'*[[title, description, content] match "*{search_term}*"][0...{limit}]'
        
        result = await self.query(query)
        return result.get("result", []) if result else []
    
    async def create_document(self, document: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new document in Sanity"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/data/mutate/{self.dataset}",
                    json={"mutations": [{"create": document}]},
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error creating document: {e}")
            return None
    
    async def update_document(self, document_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing document"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/data/mutate/{self.dataset}",
                    json={
                        "mutations": [{
                            "patch": {
                                "id": document_id,
                                "set": updates
                            }
                        }]
                    },
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error updating document: {e}")
            return None
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/data/mutate/{self.dataset}",
                    json={"mutations": [{"delete": {"id": document_id}}]},
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False


# Singleton instance
sanity_service = SanityService()
