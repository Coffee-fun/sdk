from coffee.agent import Agent
from coffee.models import DEFAULT_MODEL, OpenAI
from coffee.config import config
from coffee.api_client import CoffeeClient
from coffee.log import logger
from logging import DEBUG
from coffee.task import Workflow, Task

logger.setLevel(DEBUG)
API_KEY = "coffee-778121b135a1c247ffc1f3d074a780aa5f0549cb241b258f956c88fbb3c8"

config.api_client = CoffeeClient(
    "http://localhost:3000",
    api_key=API_KEY,
)


search_agent = Agent(
    name="SearchAgent",
    instructions=[
        "You are a helpful assistant that searches the web for latest information and then uses the web_browser tool to scrape the data for further assistance."
    ],
    model=OpenAI(id="gpt-4o-mini"),
    tools=["duckduckgo"],
)

writer = Agent(
    name="Writer",
    instructions=[
        "You will be provided with a topic and a list of top articles on that topic.",
        "Carefully read each article and generate a New York Times worthy blog post on that topic.",
        "Break the blog post into sections and provide key takeaways at the end.",
        "Make sure the title is catchy and engaging.",
        "Always provide sources, do not make up information or sources.",
        "output markdown",
    ],
    model=DEFAULT_MODEL,
    tools=["web_browser"],
)


wikipedia_agent = Agent(
    name="WikiAgent",
    instructions=["You are a researcher agent that uses wikipedia to inform the user"],
    model=DEFAULT_MODEL,
    tools=["wikipedia_tools"],
)

web3_agent = Agent(
    name="web3Agent",
    instructions="Assistant for all things related to web3. #ETH and #SOL",
    tools=["web3_essentials_tools", "solana_tools", "eth_tools"],
)

manager = Agent(
    name="TeamLead",
    instructions=[
        "You are the team leader of this agent troupe. Assign and delegate tasks accordingly"
    ],
    model=DEFAULT_MODEL,
    team=[search_agent, wikipedia_agent, web3_agent],
)


web3_workflow = (
    Workflow.build(
        Task(
            description="Look up information for the following query",
            assignee=search_agent,
        )
    )
    .add_task(
        Task(
            description="Give wikipedia information for the following result",
            assignee=wikipedia_agent,
        )
    )
    .add_task(
        Task(
            description="Give web3 tokens to invest on based on the provided information",
            assignee=web3_agent,
        )
    )
)

# web3_workflow.execute("Deepseek AI blowing up")
blog_workflow = Workflow.build(
    Task(
        description="Given a topic, return a list of the top 5 articles.",
        assignee=search_agent,
    )
).add_task(
    Task(description="Writing blog post based on the following", assignee=writer)
)
