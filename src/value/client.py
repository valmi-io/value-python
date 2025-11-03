"""SDK client implementations."""

from typing import Optional
from opentelemetry import trace

from .tracing import initialize_tracing
from .actions import ActionEmitter
from ._api import ValueControlPlaneAPI, SyncValueControlPlaneAPI
from .config import load_config_from_env


class AsyncValueSDK:
    """Asynchronous client for the Value Control SDK."""

    def __init__(
        self,
        service_name: str = "value-control-agent",
    ):
        config = load_config_from_env()
        if not config.secret:
            raise ValueError("Agent secret must be provided.")

        self.secret = config.secret
        self._otel_endpoint = config.otel_endpoint
        self._service_name = service_name
        self._backend_url = config.backend_url
        self._enable_console_export = config.enable_console_export

        # Setup internal API client
        self._api_client = ValueControlPlaneAPI(secret=self.secret, base_url=self._backend_url)

        # Agent context attributes
        self.organization_id = None
        self.workspace_id = None
        self.agent_name = None

        # Tracer and actions will be initialized in initialize()
        self._tracer = None
        self.actions = None

    @property
    def api_client(self) -> ValueControlPlaneAPI:
        return self._api_client

    @property
    def tracer(self) -> Optional[trace.Tracer]:
        return self._tracer

    async def initialize(self):
        """
        Initialize tracer, actions, and fetch agent context (organization, workspace, agent name) from backend.
        """
        agent_info = await self._api_client.get_agent_info()
        self.organization_id = agent_info.get("organization_id", "unknown")
        self.workspace_id = agent_info.get("workspace_id", "unknown")
        self.agent_name = agent_info.get("name", "unknown")

        self._tracer = initialize_tracing(
            endpoint=self._otel_endpoint,
            service_name=self._service_name,
            console_export=self._enable_console_export,
            workspace_id=self.workspace_id,
            organization_id=self.organization_id,
            agent_name=self.agent_name,
        )
        self.actions = ActionEmitter(tracer=self._tracer)


class ValueSDK:
    """Synchronous client for the Value Control SDK."""

    def __init__(
        self,
        service_name: str = "value-control-agent",
    ):
        config = load_config_from_env()
        if not config.secret:
            raise ValueError("Agent secret must be provided.")

        self.secret = config.secret
        self._otel_endpoint = config.otel_endpoint
        self._service_name = service_name
        self._backend_url = config.backend_url
        self._enable_console_export = config.enable_console_export

        # Setup internal API client (sync version)
        self._api_client = SyncValueControlPlaneAPI(secret=self.secret, base_url=self._backend_url)

        # Agent context attributes
        self.organization_id = None
        self.workspace_id = None
        self.agent_name = None

        # Tracer and actions will be initialized in initialize()
        self._tracer = None
        self.actions = None

    @property
    def api_client(self) -> SyncValueControlPlaneAPI:
        return self._api_client

    @property
    def tracer(self) -> Optional[trace.Tracer]:
        return self._tracer

    def initialize(self):
        """
        Initialize tracer, actions, and fetch agent context (organization, workspace, agent name) from backend.
        """
        agent_info = self._api_client.get_agent_info()
        self.organization_id = agent_info.get("organization_id", "unknown")
        self.workspace_id = agent_info.get("workspace_id", "unknown")
        self.agent_name = agent_info.get("name", "unknown")

        self._tracer = initialize_tracing(
            endpoint=self._otel_endpoint,
            service_name=self._service_name,
            console_export=self._enable_console_export,
            organization_id=self.organization_id,
            workspace_id=self.workspace_id,
            agent_name=self.agent_name,
        )
        self.actions = ActionEmitter(tracer=self._tracer)


def initialize_sdk_sync(service_name: str = "value-control-agent") -> ValueSDK:
    """
    Initialize and return a configured synchronous ValueSDK instance.
    Reads configuration from environment variables.
    """
    sdk = ValueSDK(service_name=service_name)
    sdk.initialize()
    return sdk


async def initialize_sdk_async(service_name: str = "value-control-agent") -> AsyncValueSDK:
    """
    Initialize and return a configured asynchronous AsyncValueSDK instance.
    Reads configuration from environment variables.
    """
    sdk = AsyncValueSDK(service_name=service_name)
    await sdk.initialize()
    return sdk
