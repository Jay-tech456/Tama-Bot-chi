"""
Smart permissions system that learns user preferences
"""
from typing import Dict, Optional
from enum import Enum


class ActionType(Enum):
    """Types of actions the agent can take"""
    SEND_MESSAGE = "send_message"
    SCHEDULE_MEETING = "schedule_meeting"
    SEND_EMAIL = "send_email"
    SHARE_PROFILE = "share_profile"
    REQUEST_CONNECTION = "request_connection"


class PermissionLevel(Enum):
    """Permission levels for different actions"""
    ALWAYS_ASK = "always_ask"
    AUTO_HIGH_MATCH = "auto_high_match"  # Auto for high-match people
    ALWAYS_AUTO = "always_auto"
    NEVER = "never"


class PermissionsManager:
    """Manages user permissions and learns preferences"""

    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.default_permissions = {
            ActionType.SEND_MESSAGE: PermissionLevel.AUTO_HIGH_MATCH,
            ActionType.SCHEDULE_MEETING: PermissionLevel.ALWAYS_ASK,
            ActionType.SEND_EMAIL: PermissionLevel.AUTO_HIGH_MATCH,
            ActionType.SHARE_PROFILE: PermissionLevel.ALWAYS_AUTO,
            ActionType.REQUEST_CONNECTION: PermissionLevel.AUTO_HIGH_MATCH,
        }

    def get_user_permissions(self, user_id: str) -> Dict[ActionType, PermissionLevel]:
        """
        Get user's permission settings from MCP

        Args:
            user_id: User ID

        Returns:
            dict mapping action types to permission levels
        """
        prefs = self.mcp_client.get_user_preferences(user_id)
        permissions = prefs.get('permissions', {})

        # Convert string keys back to enums
        result = {}
        for action_type in ActionType:
            perm_str = permissions.get(action_type.value)
            if perm_str:
                try:
                    result[action_type] = PermissionLevel(perm_str)
                except ValueError:
                    result[action_type] = self.default_permissions[action_type]
            else:
                result[action_type] = self.default_permissions[action_type]

        return result

    def can_auto_execute(
        self,
        user_id: str,
        action_type: ActionType,
        is_high_match: bool
    ) -> bool:
        """
        Determine if an action can be executed automatically

        Args:
            user_id: User ID
            action_type: Type of action to execute
            is_high_match: Whether the target is a high match

        Returns:
            bool indicating if auto-execution is allowed
        """
        permissions = self.get_user_permissions(user_id)
        permission_level = permissions.get(action_type, PermissionLevel.ALWAYS_ASK)

        if permission_level == PermissionLevel.NEVER:
            return False
        elif permission_level == PermissionLevel.ALWAYS_AUTO:
            return True
        elif permission_level == PermissionLevel.AUTO_HIGH_MATCH:
            return is_high_match
        else:  # ALWAYS_ASK
            return False

    def update_permission(
        self,
        user_id: str,
        action_type: ActionType,
        permission_level: PermissionLevel
    ) -> bool:
        """
        Update a specific permission setting

        Args:
            user_id: User ID
            action_type: Action type to update
            permission_level: New permission level

        Returns:
            bool indicating success
        """
        prefs = self.mcp_client.get_user_preferences(user_id)
        permissions = prefs.get('permissions', {})

        permissions[action_type.value] = permission_level.value

        return self.mcp_client.update_user_preferences(
            user_id,
            {'permissions': permissions}
        )

    def log_permission_response(
        self,
        user_id: str,
        action_type: ActionType,
        was_approved: bool,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Log user's approval/rejection of an action for analytics.

        This logs the interaction to the MCP server. The data can be used
        for future machine learning-based permission tuning, but this method
        does not implement any learning logic itself.

        Args:
            user_id: User ID
            action_type: Action that was approved/rejected
            was_approved: Whether user approved the action
            context: Optional context about the decision

        Returns:
            True if interaction logged successfully

        Raises:
            MCPConnectionError: If cannot connect to MCP server
            MCPTimeoutError: If request times out
            MCPError: For other server errors
        """
        return self.mcp_client.log_interaction(
            user_id=user_id,
            other_user_id=context.get('other_user_id', '') if context else '',
            interaction_type=f"permission_{action_type.value}",
            metadata={
                'approved': was_approved,
                'action_type': action_type.value,
                'context': context or {}
            }
        )
