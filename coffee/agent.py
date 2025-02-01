from .config import config
from .types.agent import AgentIn as _AgentIn
from .util.hash import generate_deterministic_hash
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from .log import logger

console = Console()


class Agent(_AgentIn):
    team: list["Agent"] = []
    _is_registered: bool = False

    def _register_if_not_exists(self):
        if self._is_registered:
            return
        if not self.agent_id:
            self.agent_id = generate_deterministic_hash(
                f"{config.api_client.user_details.id_}/{self.name}",
                "sha256",
            )
            logger.debug(f"Generated following agent id: {self.agent_id}")

        for k in self.team:
            logger.debug("Registering teams that might need to be registered")
            k._register_if_not_exists()

        for tool in self.tools:
            if isinstance(tool, str):
                continue
            tool.register_tool()

        logger.debug(f"Registering agent {self.name}")
        logger.debug(
            f"Register result: {config.api_client.create_agent(self.model_dump(mode='json'))}",
        )
        self._is_registered = True

    def create_session(self):
        self._register_if_not_exists()
        sess = config.api_client.create_agent_session(self.agent_id)
        self.session_id = sess["id_"]

    def message(self, msg: str, only_show_response: bool = True):
        self._register_if_not_exists()
        self.create_session()
        return config.api_client.run_session(self.session_id, msg, only_show_response)

    def print_message(self, msg: str):
        resp = self.message(msg, True)

        user = Markdown(msg)
        agent = Markdown(resp)

        p = Panel(user, title="User")
        r = Panel(agent, title=self.name)
        console.print(p)
        console.print(r)
