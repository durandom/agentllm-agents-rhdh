"""Factory for creating ReleaseManager agents."""

from typing import Any, Dict, Optional
from agentllm.agents.registry import AgentFactory
from agentllm_agents_rhdh.release_manager.agent import ReleaseManager


class ReleaseManagerFactory(AgentFactory):
    """
    Factory for creating ReleaseManager agent instances.

    This factory is registered via entry points and used by the AgentRegistry
    to create ReleaseManager instances.
    """

    @staticmethod
    def create_agent(
        shared_db: Any,
        token_storage: Any,
        user_id: str,
        session_id: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> ReleaseManager:
        """
        Create a ReleaseManager instance.

        Args:
            shared_db: Shared database instance (SqliteDb)
            token_storage: Token storage instance (TokenStorage)
            user_id: User ID for this agent instance
            session_id: Optional session ID for conversation history
            temperature: Optional temperature parameter for the model
            max_tokens: Optional max tokens parameter for the model
            **kwargs: Additional keyword arguments

        Returns:
            ReleaseManager instance
        """
        return ReleaseManager(
            shared_db=shared_db,
            token_storage=token_storage,
            user_id=user_id,
            session_id=session_id,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    @staticmethod
    def get_metadata() -> Dict[str, Any]:
        """
        Get metadata for the ReleaseManager agent.

        Returns:
            Dictionary with agent metadata
        """
        return {
            "name": "release-manager",
            "description": "RHDH Release management assistant with Jira and Google Drive integration",
            "mode": "chat",
            "requires_env": [
                "GEMINI_API_KEY",
                "JIRA_SERVER_URL",
                "GDRIVE_CLIENT_ID",
                "GDRIVE_CLIENT_SECRET",
            ],
        }
