from pydantic import BaseModel
from .agent import Agent
from .log import logger
from rich.markdown import Markdown
from rich.panel import Panel
from rich.console import Console

console = Console()


class Task(BaseModel):
    description: str
    assignee: Agent

    def execute(self, message: str):
        prev = self.assignee.session_id
        self.assignee.create_session()
        res = self.assignee.message(
            f"<description>{self.description}</description>\n<message>{message}</message>",
            only_show_response=True,
        )
        self.assignee.session_id = prev
        return res


class Workflow(BaseModel):
    name: str = "Unnamed Workflow"
    steps: list[Task]
    _current_index: int = 0

    def add_task(self, task: Task):
        return Workflow(steps=[*self.steps, task])

    @staticmethod
    def build(task: Task):
        return Workflow(steps=[task])

    def execute(self, message: str):
        logger.debug(f"Executing: step={self._current_index}")
        if self._current_index == len(self.steps):
            return message

        res = self.steps[self._current_index].execute(message)
        logger.debug(f"step={self._current_index} Response: {res}"[:150])
        self._current_index += 1
        return self.execute(res)

    def execute_and_print(self, message: str):
        result = self.execute(message)
        user = Markdown(message)
        agent = Markdown(result)

        p = Panel(user, title="User")
        r = Panel(
            agent, title="Workflow:" + " > ".join((x.assignee.name for x in self.steps))
        )
        console.print(p)
        console.print(r)
