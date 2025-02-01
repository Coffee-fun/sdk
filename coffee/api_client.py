import requests

from .config import config
from .types.user import CurrentUser
from .util.time_cache import time_cache
from .log import logger
from requests import Response
from functools import wraps


def response_handler(fn):
    @wraps(fn)
    def _wrapped(*args, **kwargs):
        resp: Response = fn(*args, **kwargs)
        js = text = None
        try:
            js = resp.json()
        except Exception as _:
            text = resp.text()
        try:
            resp.raise_for_status()
            if js and "error" in js:
                raise Exception("_")
        except Exception as _:
            msg = f"JSON={js}" if js else f"TEXT={text}"
            raise Exception(f"request({args=}, {kwargs=}) failed. \n{msg}")
        if js:
            match js:
                case list():
                    return js
                case dict({"data": x}):
                    return x
                case default:
                    return default
        return resp

    return _wrapped


class CoffeeClient:
    def __init__(
        self, base_url: str = "https://coffee-sdk-api.fly.dev", api_key: str = None
    ):
        self.base_url = base_url.rstrip("/")
        config.api_key = api_key or config.api_key
        if not config.api_key:
            raise ValueError(
                "API key must be provided or set in environment variable API_KEY"
            )
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": config.api_key})

    @property
    @time_cache(max_age=300)
    def user_details(self) -> CurrentUser:
        logger.debug("Getting user details")
        gm = self.get_me()["user_data"]
        logger.debug(f"get_me() => {gm}")
        return CurrentUser.model_validate(gm)

    # Agents routes
    @response_handler
    def create_agent(self, agent_data: dict) -> requests.Response:
        url = f"{self.base_url}/agent/-/create?overwrite"
        return self.session.post(url, json=agent_data)

    @response_handler
    def add_agent_knowledge_url(self, agent_id: str, url: str) -> requests.Response:
        url_path = f"{self.base_url}/agent/{agent_id}/add-knowledge"
        return self.session.post(url_path, json={"url": url})

    @response_handler
    def get_all_agents(self) -> requests.Response:
        url = f"{self.base_url}/agent/-/getall"
        return self.session.get(url)

    @response_handler
    def create_agent_session(self, agent_id: str) -> requests.Response:
        url = f"{self.base_url}/agent/{agent_id}/session/create"
        return self.session.get(url)

    @response_handler
    def get_agent_sessions(self, agent_id: str) -> requests.Response:
        url = f"{self.base_url}/agent/{agent_id}/sessions"
        return self.session.get(url)

    @response_handler
    def run_session(
        self, session_id: str, message: str, only_show_response: bool = False
    ) -> str:
        url = f"{self.base_url}/agent/{session_id}/run"
        return self.session.post(
            url,
            json={"message": message},
            params={"only_show_response": ""} if only_show_response else None,
        )

    @response_handler
    def create_team_session(self) -> requests.Response:
        url = f"{self.base_url}/agent/team/session/create"
        return self.session.get(url)

    @response_handler
    def get_team_session_history(self, session_id: str) -> requests.Response:
        url = f"{self.base_url}/agent/team/{session_id}/history"
        return self.session.get(url)

    @response_handler
    def run_team_session(self, session_id: str, message: str) -> requests.Response:
        url = f"{self.base_url}/agent/team/{session_id}/run"
        return self.session.post(url, json={"message": message})

    @response_handler
    def get_public_agents(self) -> requests.Response:
        url = f"{self.base_url}/agent/public/agents"
        return self.session.get(url)

    @response_handler
    def get_agent(self, agent_id: str) -> requests.Response:
        url = f"{self.base_url}/agent/get/{agent_id}"
        return self.session.get(url)

    @response_handler
    def get_session_details(self, session_id: str) -> requests.Response:
        url = f"{self.base_url}/agent/{session_id}/details"
        return self.session.get(url)

    @response_handler
    def upload_knowledge_file(self, agent_id: str, file_path: str) -> requests.Response:
        url = f"{self.base_url}/knowledge/{agent_id}/upload-knowledge"
        with open(file_path, "rb") as f:
            files = {"file": f}
            return self.session.post(url, files=files)

    @response_handler
    def create_plugin(self, plugin_data: dict) -> requests.Response:
        url = f"{self.base_url}/plugins/-/create"
        return self.session.post(url, json=plugin_data)

    @response_handler
    def enable_plugin_for_agent(
        self, plugin_id: str, agent_id: str
    ) -> requests.Response:
        url = f"{self.base_url}/plugins/{plugin_id}/enable-for/{agent_id}"
        return self.session.get(url)

    @response_handler
    def get_user_plugins(self) -> requests.Response:
        url = f"{self.base_url}/plugins/user-plugins"
        return self.session.get(url)

    @response_handler
    def enable_builtin_plugin(
        self, plugin_name: str, agent_id: str
    ) -> requests.Response:
        url = f"{self.base_url}/plugins/builtins/{plugin_name}/enable-for/{agent_id}"
        return self.session.post(url)

    @response_handler
    def enable_marketplace_plugin(
        self, plugin_id: str, agent_id: str
    ) -> requests.Response:
        url = f"{self.base_url}/plugins/marketplace/plugins/{plugin_id}/enable-for/{agent_id}"
        return self.session.post(url)

    @response_handler
    def get_marketplace_plugins(self) -> requests.Response:
        url = f"{self.base_url}/plugins/marketplace/plugins/all"
        return self.session.get(url)

    @response_handler
    def get_marketplace_plugin(self, plugin_id: str) -> requests.Response:
        url = f"{self.base_url}/plugins/marketplace/{plugin_id}/plugin"
        return self.session.get(url)

    @response_handler
    def buy_credits(
        self, amount: int, coffee_credits: int, tx_hash: str, network: str, wallet: str
    ) -> requests.Response:
        url = f"{self.base_url}/transaction/buy-credits"
        data = {
            "amount": amount,
            "coffee_credits": coffee_credits,
            "hash": tx_hash,
            "network": network,
            "wallet": wallet,
        }
        return self.session.post(url, json=data)

    @response_handler
    def buy_agent(self, agent_id: str, amount: int, tx_hash: str) -> requests.Response:
        url = f"{self.base_url}/transaction/{agent_id}/buy-agent"
        data = {"amount": amount, "hash": tx_hash}
        return self.session.post(url, json=data)

    @response_handler
    def buy_plugin(
        self, plugin_id: str, amount: int, tx_hash: str
    ) -> requests.Response:
        url = f"{self.base_url}/transaction/{plugin_id}/buy-plugin"
        data = {"amount": amount, "hash": tx_hash}
        return self.session.post(url, json=data)

    @response_handler
    def upload_user_avatar(self, data: bytes) -> requests.Response:
        url = f"{self.base_url}/uploads/user-avatar"
        return self.session.post(url, data=data)

    def upload_file(self, file_path: str, data: bytes) -> requests.Response:
        url = f"{self.base_url}/uploads/{file_path}"
        return self.session.post(url, data=data)

    @response_handler
    def github_auth(self, code: str) -> requests.Response:
        url = f"{self.base_url}/users/auth/github"
        return self.session.post(url, json={"code": code})

    @response_handler
    def get_me(self) -> dict:
        url = f"{self.base_url}/users/me"
        logger.debug(f"{url=}")
        return self.session.get(url)

    @response_handler
    def get_user_sessions_data(self, user_id: str) -> requests.Response:
        url = f"{self.base_url}/users/{user_id}/sessions-data"
        return self.session.get(url)
