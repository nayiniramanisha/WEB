import socketio
from .services.chat import handle_incoming_message


def register_socketio(sio: socketio.AsyncServer):
    @sio.event
    async def connect(sid, environ):
        print(f"🔍 SOCKET: Client connected: {sid}")
        await sio.emit("connected", {"sid": sid}, to=sid)
        
        # Send a test message to verify connection
        await sio.emit("test_message", {"message": "Connection test", "timestamp": "now"}, to=sid)
        print(f"🔍 SOCKET: Sent test message to {sid}")

    @sio.event
    async def disconnect(sid):
        # no-op; could log
        pass

    @sio.event
    async def chat_message(sid, data):
        # data: { session_id, content, user_email? }
        response = await handle_incoming_message(data)
        print(f"🔍 SOCKET: Emitting bot_message with related field: {response.get('related', [])}")
        print(f"🔍 SOCKET: Full response: {response}")
        
        # Try to send the response with error handling
        try:
            await sio.emit("bot_message", response, to=sid)
            print(f"🔍 SOCKET: Successfully sent bot_message to {sid}")
        except Exception as e:
            print(f"🔍 SOCKET: Error sending bot_message to {sid}: {e}")
            # Try to send to all connected clients as fallback
            try:
                await sio.emit("bot_message", response)
                print(f"🔍 SOCKET: Sent bot_message as broadcast fallback")
            except Exception as e2:
                print(f"🔍 SOCKET: Error sending broadcast fallback: {e2}")
    
    @sio.event
    async def test_bot_message(sid, data):
        """Test endpoint to manually trigger a bot message"""
        print(f"🔍 SOCKET: Test bot message requested by {sid}")
        test_response = {
            "session_id": "test",
            "role": "assistant", 
            "content": "This is a test message from the backend!",
            "related": ["Test question 1", "Test question 2"]
        }
        try:
            await sio.emit("bot_message", test_response, to=sid)
            print(f"🔍 SOCKET: Successfully sent test bot_message to {sid}")
        except Exception as e:
            print(f"🔍 SOCKET: Error sending test bot_message to {sid}: {e}")


