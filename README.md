# Coffee Agent Framework

A Python framework for building and managing AI agent workflows with support for tools, teams, and complex interactions.

## Installation
from PyPi
```sh
pip install coffee-agent-kit
```
OR 
```sh
pip install install git+ssh://git@github.com/Ghost-Teams/coffee-lib.git
```

# Examples

See [./example.py](example.py)

## Interacting with the Coffee API

```python
from coffee.api_client import CoffeeClient
from coffee.config import config
config.api_client = CoffeeClient(
    api_key=YOUR_API_KEY,
)
```

![image](https://github.com/user-attachments/assets/9f825237-3805-4ab1-93af-76b1566c1cfc)

![image](https://github.com/user-attachments/assets/3adf7e12-fbea-40f4-8704-a9b24012220b)

## Quickstart

```python
from coffee import Agent, CoffeeClient, config
from coffee.models import DEFAULT_MODEL

# Configure API client
config.api_client = CoffeeClient(
    api_key="your_api_key_here", base_url="https://coffee-sdk-api.fly.dev"
)
# Create a basic agent
research_agent = Agent(
    name="ResearchAgent",
    instructions=[
        "You are a research assistant specialized in web information gathering"
    ],
    tools=["duckduckgo", "web_browser"],
    model=DEFAULT_MODEL,
)
# Simple interaction
research_agent.print_message("What's the latest news about AI advancements?")

```

## Core Concepts

### Agents

Agents are autonomous units with specific capabilities:

```python
class Agent:
    def message(self, msg: str, only_show_response: bool = True):
        ...

    def print_message(self, msg: str):
        ...
```

### Tools

Built-in tools provide specialized capabilities:

```python
BuiltinTools = Literal[
    "web3_essentials_tools",
    "solana_tools",
    "duckduckgo",
    "web_browser",
    "wikipedia_tools",
    # and lots more
]
```

### Workflows

Chain multiple agents into complex workflows:

```python
web3_workflow = (
    Workflow.build(
        Task(description="Web search", assignee=search_agent)
    )
    .add_task(Task(description="Wiki research", assignee=wiki_agent))
    .add_task(Task(description="Web3 analysis", assignee=web3_agent))
)

web3_workflow.execute_and_print("Latest blockchain trends")
```

## Key Features

### Multi-Agent Collaboration

```python
team = Agent(
    name="TeamLead",
    instructions=["Coordinate team activities"],
    team=[research_agent, writer_agent, analysis_agent]
)
```

### Custom Tools

Register or Purchase custom tools on the Coffee Website and use them in your agents.

```python
class RemoteTool(BaseModel):
    name: str
    url: str
    args: dict[str, PluginArgType]
    instructions: str

    def register_tool(self):
        # Registration logic
        pass
```

### Model Support

```python
class OpenAI(Model):
    id: str = "gpt-4o"
    name: str = "OpenAIChat"
    provider: str = "OpenAI"

class Claude(Model):
    id: str = "claude-3-5-sonnet-20241022"
    provider: str = "Anthropic"
```

## Advanced Configuration

### Environment Setup

```python
# Configure logging
from coffee.log import logger
logger.setLevel(logging.DEBUG)

# Custom client configuration
config.api_client = CoffeeClient(
    api_key="your_key"
)
```

## Examples

### Blog Writing Workflow

```python
blog_workflow = Workflow.build(
    Task(description="Gather research", assignee=research_agent)
).add_task(
    Task(description="Write article", assignee=writer_agent)
)

blog_workflow.execute_and_print("Generative AI in healthcare")
```
