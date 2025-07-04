import httpx
from typing import AsyncGenerator, Dict, Any, List
from contextlib import asynccontextmanager
from app.config import settings

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"Bearer {settings.GITHUB_TOKEN}"}
        self.timeout = 30.0
        self._client = None

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        Advanced async context manager for HTTP client management.
        
        This ensures proper connection pooling and resource cleanup.
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.headers,
                limits=httpx.Limits(
                    max_keepalive_connections=10,
                    max_connections=100,
                    keepalive_expiry=30.0
                )
            )
        
        try:
            yield self._client
        finally:
            # Don't close the client here as it's reused
            pass

    async def close(self):
        """Close the HTTP client properly."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_repo(self, owner: str, repo: str):
        url = f"{self.base_url}/repos/{owner}/{repo}"
        async with self.get_client() as client:
            response = await client.get(url)
            response.raise_for_status()
            return await response.json()

    async def get_issues(self, owner: str, repo: str, istask=False):
        """
        Get issues using traditional approach for backward compatibility.
        """
        issues = []
        async for issue in self.stream_issues(owner, repo, istask):
            issues.append(issue)
        return issues

    async def stream_issues(self, owner: str, repo: str, istask=False) -> AsyncGenerator[Dict[Any, Any], None]:
        """
        Advanced async generator for streaming GitHub issues.
        
        This provides memory-efficient iteration over large datasets
        and demonstrates advanced async patterns with generators.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": "all", "per_page": 100}  # Optimize pagination
        
        async with self.get_client() as client:
            while url:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                issues_batch = await response.json()
                
                for issue in issues_batch:
                    if istask:
                        yield issue
                    else:
                        yield {"number": issue["number"], "title": issue["title"]}

                # Handle pagination
                if "next" in response.links:
                    url = response.links["next"]["url"]
                    params = None  # URL already contains params
                else:
                    url = None

    async def get_issues_batch(self, owner: str, repo: str, batch_size: int = 50, istask=False) -> AsyncGenerator[List[Dict[Any, Any]], None]:
        """
        Advanced async generator that yields batches of issues.
        
        This demonstrates sophisticated async patterns for processing
        large datasets in configurable chunks.
        """
        batch = []
        
        async for issue in self.stream_issues(owner, repo, istask):
            batch.append(issue)
            
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        # Yield remaining items if any
        if batch:
            yield batch

    async def get_issue(self, owner: str, repo: str, issue_number: int):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}"
        async with self.get_client() as client:
            response = await client.get(url)
            response.raise_for_status()
            return await response.json()
    
    async def __aenter__(self):
        """Support async context manager protocol."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Support async context manager protocol."""
        await self.close()