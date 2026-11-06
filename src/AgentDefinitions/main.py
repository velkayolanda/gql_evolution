import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .Context import AgentContext, create_http_execution_context
from .Toolsets import create_demo_toolset, create_gql_toolset


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run PydanticAI subgraph agent."
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        help="Path to .env file.",
    )
    return parser.parse_args()


def load_configuration():
    args = parse_args()
    if args.env_file:
        print(f"Loading environment variables from {args.env_file}")
        load_dotenv(args.env_file)
    return {
        "AI_MODEL": os.getenv("AI_MODEL"),
        "AI_BASE_URL": os.getenv("AI_BASE_URL"),
        "AI_API_KEY": os.getenv("AI_API_KEY"),
        "GQL_ENDPOINT": os.getenv("GQL_ENDPOINT", "http://localhost:8000/api/gql"),
        "GQL_TOKEN": os.getenv("GQL_TOKEN"),
    }


def create_agent(base_url: str, api_key: str, model_name: str) -> Agent[AgentContext]:
    provider = OpenAIProvider(
        base_url=base_url,
        api_key=api_key,
    )
    model = OpenAIChatModel(
        model_name,
        provider=provider,
    )
    return Agent(
        model,
        deps_type=AgentContext,
        toolsets=[
            create_demo_toolset(),
            create_gql_toolset(),
        ],
        instructions="""
You are an assistant for the gql_personalities GraphQL subgraph.

This subgraph manages personal identity data for users:
- PersonalData: birth date, birth place, citizenship, nationality, personal title (one record per user)
- Education: study history — institution, programme, degree, dates, graduation (multiple records per person)
- Certificates: qualifications — title, issuer, number, issue/expiry dates, level (multiple records per person)

Always use the available tools to retrieve authoritative data from the system.
Never invent or guess identifiers, names or dates — only report what the tools return.
When asked about a person, use the list tools to find their records, then use the
by-id tools to get full details if needed.
""",
    )


def main():
    config = load_configuration()

    if not config["AI_MODEL"]:
        raise RuntimeError("AI_MODEL is not configured.")
    if not config["AI_BASE_URL"]:
        raise RuntimeError("AI_BASE_URL is not configured.")
    if not config["AI_API_KEY"]:
        raise RuntimeError("AI_API_KEY is not configured.")

    model_name = config["AI_MODEL"]
    base_url = config["AI_BASE_URL"]
    api_key = config["AI_API_KEY"]
    gql_endpoint = config["GQL_ENDPOINT"]
    gql_token = config["GQL_TOKEN"]

    executor = create_http_execution_context(gql_endpoint, gql_token)
    deps = AgentContext(
        subgraph_name="gql_personalities",
        executor=executor,
        authorization_token=gql_token,
    )

    agent = create_agent(base_url, api_key, model_name)

    print("PydanticAI subgraph agent — gql_personalities")
    print(f"AI model:     {model_name}")
    print(f"AI endpoint:  {base_url}")
    print(f"GQL endpoint: {gql_endpoint}")
    print()

    agent.to_cli_sync(deps=deps)


if __name__ == "__main__":
    main()