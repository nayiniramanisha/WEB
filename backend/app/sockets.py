import socketio
from .services.chat import handle_incoming_message


def register_socketio(sio: socketio.AsyncServer):
    @sio.event
    async def connect(sid, environ):
        print(f"🔍 SOCKET: Client connected: {sid}")
        try:
            await sio.emit("connected", {"sid": sid}, to=sid)
            print(f"🔍 SOCKET: Sent connected message to {sid}")
            
            # Send a test message to verify connection
            await sio.emit("test_message", {"message": "Connection test", "timestamp": "now"}, to=sid)
            print(f"🔍 SOCKET: Sent test message to {sid}")
        except Exception as e:
            print(f"🔍 SOCKET: Error in connect handler: {e}")

    @sio.event
    async def disconnect(sid):
        # no-op; could log
        pass

    @sio.event
    async def chat_message(sid, data):
        # data: { session_id, content, user_email? }
        print(f"🔍 SOCKET: Processing chat_message from {sid}: {data}")
        
        # Send immediate acknowledgment to keep connection alive
        try:
            print(f"🔍 SOCKET: Attempting to send processing_started to {sid}")
            await sio.emit("processing_started", {"message": "AI is processing your request..."}, to=sid)
            print(f"🔍 SOCKET: Successfully sent processing_started to {sid}")
        except Exception as e:
            print(f"🔍 SOCKET: Error sending processing_started to {sid}: {e}")
            print(f"🔍 SOCKET: Exception type: {type(e)}")
            print(f"🔍 SOCKET: Exception details: {str(e)}")
        
        # Process the message (this takes time)
        print(f"🔍 SOCKET: Starting AI processing for {sid}")
        response = await handle_incoming_message(data)
        print(f"🔍 SOCKET: AI processing completed for {sid}")
        print(f"🔍 SOCKET: Emitting bot_message with related field: {response.get('related', [])}")
        print(f"🔍 SOCKET: Full response: {response}")
        
        # Send the final response
        success = False
        
        # Method 1: Send to specific session
        try:
            print(f"🔍 SOCKET: Attempting to send bot_message to {sid}")
            await sio.emit("bot_message", response, to=sid)
            print(f"🔍 SOCKET: Successfully sent bot_message to {sid}")
            success = True
        except Exception as e:
            print(f"🔍 SOCKET: Error sending bot_message to {sid}: {e}")
            print(f"🔍 SOCKET: Exception type: {type(e)}")
            print(f"🔍 SOCKET: Exception details: {str(e)}")
        
        # Method 2: Send as broadcast if specific send failed
        if not success:
            try:
                print(f"🔍 SOCKET: Attempting broadcast fallback")
                await sio.emit("bot_message", response)
                print(f"🔍 SOCKET: Sent bot_message as broadcast fallback")
                success = True
            except Exception as e2:
                print(f"🔍 SOCKET: Error sending broadcast fallback: {e2}")
                print(f"🔍 SOCKET: Exception type: {type(e2)}")
                print(f"🔍 SOCKET: Exception details: {str(e2)}")
        
        # Method 3: Store in database for later retrieval if all else fails
        if not success:
            print(f"🔍 SOCKET: All send methods failed, storing response for later retrieval")
            # TODO: Store response in database for later retrieval
    
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
    
    @sio.event
    async def ping(sid, data):
        """Simple ping endpoint to test connection"""
        print(f"🔍 SOCKET: Ping received from {sid}")
        try:
            await sio.emit("pong", {"message": "pong", "timestamp": "now"}, to=sid)
            print(f"🔍 SOCKET: Successfully sent pong to {sid}")
        except Exception as e:
            print(f"🔍 SOCKET: Error sending pong to {sid}: {e}")


