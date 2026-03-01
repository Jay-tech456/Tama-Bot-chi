# Instructions for Claude Code

## Absolute Rules - No Exceptions

### 1. NO PLACEHOLDERS OR STUB CODE
- Every function must have complete, working implementation
- Never write comments like "# TODO", "# Placeholder", "# To be implemented"
- Never write "pass" as function body unless it's an intentional abstract base class
- If you cannot implement something fully, state that limitation upfront and refuse to write partial code

### 2. NO FALSE CLAIMS ABOUT TESTING
- Never say "I've tested this" unless you have ACTUALLY run the code
- Never say "tests pass" without showing actual test output
- Never claim code works without evidence
- If code is untested, explicitly state: "This code is untested and may have bugs"

### 3. NO EMOJIS IN CODE OR TECHNICAL COMMUNICATION
- No emojis in code comments, docstrings, or variable names
- No emojis in commit messages
- No emojis in technical documentation
- Emojis may only appear in user-facing UI strings if explicitly requested

### 4. EXPLICIT TYPE CHECKING
- All function parameters must have type hints
- All return values must have type hints
- Use TypedDict or Pydantic models for complex dictionaries
- Never use bare `dict`, `list`, or `any` without specific type parameters

### 5. ERROR HANDLING MUST BE EXPLICIT
- Every external API call must have explicit error handling
- Never silently catch exceptions with bare `except:` or `except Exception: pass`
- All error paths must return or raise with meaningful messages
- Document what errors can occur in function docstrings

### 6. DEPENDENCIES ON EXTERNAL SERVICES
- If code depends on an external service (MCP server, API), document that dependency
- Provide graceful degradation when service is unavailable
- Never fail silently - log errors or return error responses
- Include health check endpoints for all services

## Code Quality Standards

### Function Implementation Checklist
Before writing any function, verify:
- [ ] I can implement this completely with available information
- [ ] All dependencies exist or are properly mocked
- [ ] Error cases are handled explicitly
- [ ] Return type matches type hint
- [ ] No placeholder comments remain

### Documentation Requirements
Every function must have:
```python
def function_name(param: Type) -> ReturnType:
    """
    Brief description of what function does.

    Args:
        param: Description of parameter and constraints

    Returns:
        Description of return value

    Raises:
        SpecificError: When this error occurs
    """
```

### Type Hints Example
```python
# WRONG - vague types
def get_user(user_id) -> dict:
    return {}

# CORRECT - explicit types
from typing import Dict, Optional, List

class UserProfile(TypedDict):
    user_id: str
    name: str
    email: str
    interests: List[str]

def get_user(user_id: str) -> Optional[UserProfile]:
    """
    Retrieve user profile from database.

    Args:
        user_id: Unique identifier for user

    Returns:
        User profile if found, None if not found

    Raises:
        DatabaseError: If database connection fails
    """
    # Implementation here
```

### Error Handling Example
```python
# WRONG - silent failure
def send_message(recipient: str, message: str) -> dict:
    try:
        response = requests.post(url, json=data)
        return response.json()
    except:
        return {}

# CORRECT - explicit error handling
def send_message(recipient: str, message: str) -> Dict[str, Any]:
    """
    Send message via external API.

    Args:
        recipient: Message recipient identifier
        message: Message content

    Returns:
        API response with success status

    Raises:
        ConnectionError: If cannot connect to API
        ValidationError: If recipient or message invalid
    """
    try:
        response = requests.post(
            url,
            json={"recipient": recipient, "message": message},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout as e:
        raise ConnectionError(f"API timeout after 10s: {e}")

    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(f"Cannot connect to API: {e}")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            raise ValidationError(f"Invalid request: {e.response.text}")
        raise ConnectionError(f"API error {e.response.status_code}: {e.response.text}")
```

## Detecting and Fixing Violations

### How to Identify Placeholder Code
Look for:
- Comments containing "TODO", "FIXME", "placeholder", "stub", "to be implemented"
- Functions with only `pass` or `...` as body
- Functions returning empty dict/list without logic
- Comments saying "Future enhancement" or "This will be implemented"
- Docstrings describing functionality that isn't implemented

### How to Identify Type Issues
Look for:
- Missing type hints on parameters or returns
- Generic `dict` or `list` without type parameters
- `Any` used without justification
- Inconsistent return types (sometimes dict, sometimes None without Optional)

### How to Identify Error Handling Issues
Look for:
- Bare `except:` blocks
- `except Exception:` without re-raising or logging
- External API calls without try/except
- Functions that can fail but don't raise or return error status

## Rewriting Existing Code

When asked to fix code violations:

1. **Read the entire file** - understand what it's trying to do
2. **List all violations** - be specific about line numbers
3. **Propose complete fix** - no partial solutions
4. **Verify types are complete** - every function fully typed
5. **Verify error handling** - every failure path handled
6. **Remove all placeholders** - implement or remove features

## When Implementation Is Not Possible

If you cannot fully implement something:

1. State clearly: "I cannot implement X because Y"
2. Explain what information or dependencies are missing
3. Propose alternatives or ask for clarification
4. **Never write placeholder code anyway**

Example:
```
I cannot implement the MCP client fully because:
- The MCP server API contract is not defined
- I don't know the authentication scheme
- The data schemas are not specified

Options:
1. Define the API contract first, then I'll implement
2. Create a mock MCP server for testing
3. Use dependency injection to make the client swappable
```

## Testing Requirements

### Unit Tests
- Test all public functions
- Test error cases, not just happy path
- Use pytest fixtures for setup
- No mocking unless absolutely necessary

### Integration Tests
- Test with actual services when available
- Document which services must be running
- Provide docker-compose for dependencies
- Include health checks before tests

### Test Documentation
Every test must have:
```python
def test_feature_name():
    """
    Test that feature works correctly when given valid input.

    Setup:
        - Creates test user
        - Mocks external API

    Validates:
        - Return value matches expected schema
        - Side effects occur correctly
    """
```

## Final Checklist Before Submitting Code

- [ ] No TODO, placeholder, or stub comments
- [ ] All functions have complete type hints
- [ ] All external calls have error handling
- [ ] All docstrings are complete and accurate
- [ ] No emojis in code or technical docs
- [ ] Code actually implements claimed functionality
- [ ] Tests exist and pass (if claiming "tested")
- [ ] Dependencies are documented
- [ ] Error messages are helpful

## Consequences of Violations

If I (Claude) write code that violates these rules:
- User will reject the code
- User will point out specific violations
- I must rewrite from scratch following all rules
- No partial fixes - complete compliance only

These rules exist because placeholder code and false claims waste time and create technical debt. Following them ensures the codebase is maintainable and trustworthy.
