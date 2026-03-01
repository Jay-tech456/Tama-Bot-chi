"""
Custom exceptions for TamaBotchi agent.
"""


class TamaError(Exception):
    """Base exception for all TamaBotchi errors"""


# MCP Server Errors

class MCPError(TamaError):
    """Base exception for MCP server errors"""


class MCPConnectionError(MCPError):
    """Cannot connect to MCP server"""



class MCPTimeoutError(MCPError):
    """MCP server request timed out"""



class MCPNotFoundError(MCPError):
    """Requested resource not found on MCP server"""



class MCPValidationError(MCPError):
    """MCP server rejected request due to validation error"""



# iMessage Server Errors

class iMessageError(TamaError):
    """Base exception for iMessage errors"""



class iMessageConnectionError(iMessageError):
    """Cannot connect to iMessage server"""



class iMessageSendError(iMessageError):
    """Failed to send iMessage"""



# Gmail/Calendar Errors

class GmailError(TamaError):
    """Base exception for Gmail errors"""



class GmailAuthError(GmailError):
    """Gmail authentication failed"""



class GmailSendError(GmailError):
    """Failed to send email"""



class CalendarError(TamaError):
    """Base exception for Calendar errors"""



class CalendarAuthError(CalendarError):
    """Calendar authentication failed"""



class CalendarEventError(CalendarError):
    """Failed to create calendar event"""



# Agent Errors

class AgentError(TamaError):
    """Base exception for agent errors"""



class ProfileNotFoundError(AgentError):
    """User profile not found"""



class InvalidMatchError(AgentError):
    """Invalid match calculation"""



class PermissionDeniedError(AgentError):
    """User permission denied for action"""



# Configuration Errors

class ConfigurationError(TamaError):
    """Configuration error"""



class MissingAPIKeyError(ConfigurationError):
    """Required API key not found"""

