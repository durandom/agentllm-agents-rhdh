"""RHDH toolkit configurations."""

from agentllm_agents_rhdh.toolkit_configs.gdrive_config import GoogleDriveConfig
from agentllm_agents_rhdh.toolkit_configs.jira_config import JiraConfig

__all__ = ["GoogleDriveConfig", "JiraConfig"]

# SystemPromptExtensionConfig is optional and imported conditionally
try:
    from agentllm_agents_rhdh.toolkit_configs.system_prompt_extension_config import (
        SystemPromptExtensionConfig,
    )
    __all__.append("SystemPromptExtensionConfig")
except ImportError:
    pass
