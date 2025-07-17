"""
Tests for async improvements to demonstrate advanced async concepts.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.core.github_client import GitHubClient
from worker.async_task import gather_with_concurrency


@pytest.mark.asyncio
async def test_github_client_async_context_manager():
    """Test that GitHubClient properly supports async context manager."""
    async with GitHubClient() as client:
        assert client is not None
        assert hasattr(client, 'get_client')
        assert hasattr(client, 'stream_issues')


@pytest.mark.asyncio
async def test_github_client_stream_issues():
    """Test async generator for streaming issues."""
    client = GitHubClient()
    
    # Mock the HTTP client
    with patch.object(client, 'get_client') as mock_get_client:
        mock_http_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[
            {"number": 1, "title": "Issue 1", "updated_at": "2023-01-01T00:00:00Z"},
            {"number": 2, "title": "Issue 2", "updated_at": "2023-01-02T00:00:00Z"}
        ])
        mock_response.links = {}  # No pagination
        mock_http_client.get = AsyncMock(return_value=mock_response)
        
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Test streaming
        issues = []
        async for issue in client.stream_issues("owner", "repo", False):
            issues.append(issue)
        
        assert len(issues) == 2
        assert issues[0]["number"] == 1
        assert issues[1]["number"] == 2


@pytest.mark.asyncio
async def test_github_client_batch_issues():
    """Test async batch processing."""
    client = GitHubClient()
    
    with patch.object(client, 'stream_issues') as mock_stream:
        # Mock async generator
        async def mock_generator():
            for i in range(5):
                yield {"number": i, "title": f"Issue {i}"}
        
        mock_stream.return_value = mock_generator()
        
        batches = []
        async for batch in client.get_issues_batch("owner", "repo", batch_size=2):
            batches.append(batch)
        
        assert len(batches) == 3  # 2 + 2 + 1
        assert len(batches[0]) == 2
        assert len(batches[1]) == 2
        assert len(batches[2]) == 1


@pytest.mark.asyncio
async def test_gather_with_concurrency():
    """Test advanced concurrency control."""
    call_count = 0
    
    async def mock_task():
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.01)  # Simulate async work
        return call_count
    
    tasks = [mock_task() for _ in range(5)]
    results = await gather_with_concurrency(3, *tasks)
    
    assert len(results) == 5
    assert all(isinstance(r, int) for r in results)


@pytest.mark.asyncio
async def test_async_middleware_concepts():
    """Test async middleware patterns (conceptual)."""
    
    async def mock_middleware(request, call_next):
        """Example of async middleware pattern."""
        import time
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        # In real implementation, this would set headers
        assert process_time >= 0
        
        return response
    
    # Mock request and call_next
    request = {}
    
    async def call_next(req):
        await asyncio.sleep(0.01)  # Simulate processing
        return {"status": "ok"}
    
    result = await mock_middleware(request, call_next)
    assert result["status"] == "ok"


def test_async_task_decorator_concepts():
    """Test async task decorator concepts."""
    from worker.async_task import async_task
    from unittest.mock import Mock
    
    # Mock Celery app
    mock_app = Mock()
    mock_app.task.return_value = lambda func: func
    
    @async_task(mock_app)
    async def sample_async_task():
        await asyncio.sleep(0.01)
        return "completed"
    
    # The decorator should have been applied
    assert callable(sample_async_task)
    # In real usage, this would be executed by Celery