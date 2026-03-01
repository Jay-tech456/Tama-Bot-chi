# Proximity Detection Service

This service detects when users with the TamaBotchi app are nearby and notifies the Agent API.

## Architecture

The proximity service will:
1. Listen for network discovery broadcasts from other TamaBotchi users
2. Detect when users join the same WiFi network at events
3. Optionally integrate with event platform APIs for attendee lists
4. Notify the Agent API when matches are found

## Implementation Status

**Current:** Stub/placeholder - needs iOS/mobile implementation

**Recommended approach:**
- iOS: Use Multipeer Connectivity framework
- Android: Use Nearby Connections API
- Both: Combine with WiFi network detection and event API integration

## API Contract

When a user is detected, this service should POST to the Agent API:

```http
POST http://localhost:5000/users/{user_id}/detected
Content-Type: application/json

{
  "user_id": "current_user_id",
  "other_user_id": "detected_user_id",
  "context": {
    "event_name": "TechConf 2025",
    "location": "San Francisco",
    "detection_method": "multipeer_connectivity",
    "timestamp": "2025-11-21T10:30:00Z"
  }
}
```

## Future Implementation

This will likely be implemented as:
1. **iOS app** with Multipeer Connectivity
2. **Android app** with Nearby Connections
3. **Background service** that monitors WiFi networks
4. **Event integration** that fetches attendee lists

The mobile apps should call the Agent API when users are detected.

## Testing

For testing the agent without the proximity service, you can manually trigger detections:

```bash
curl -X POST http://localhost:5000/users/user123/detected \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "other_user_id": "user456",
    "context": {
      "event_name": "Test Event",
      "location": "Test Location"
    }
  }'
```
