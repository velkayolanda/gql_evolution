from dataclasses import dataclass
from typing import Any, Awaitable, Callable


GraphQLExecutor = Callable[
    [str, dict[str, Any] | None],
    Awaitable[Any],
]


def create_execution_context(schema):
    """In-process executor — wraps a Strawberry schema for testing without a running server."""
    async def execute_gql(query: str, variables: dict = None):
        result = await schema.execute(query, variable_values=variables)
        return {"data": result.data, "errors": result.errors}
    return execute_gql


def create_http_execution_context(endpoint_url: str, authorization_token: str = None) -> GraphQLExecutor:
    """HTTP executor — sends queries to a running GraphQL server via POST."""
    async def execute_gql(query: str, variables: dict = None) -> dict:
        import aiohttp
        headers = {"Content-Type": "application/json"}
        if authorization_token:
            headers["Authorization"] = f"Bearer {authorization_token}"
        payload: dict = {"query": query}
        if variables:
            payload["variables"] = variables
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint_url, json=payload, headers=headers) as response:
                return await response.json()
    return execute_gql


@dataclass
class AgentContext:
    """Runtime dependencies available to agent tools."""

    subgraph_name: str = "demo"
    executor: GraphQLExecutor = None
    user_id: str = None
    authorization_token: str = None