import socketio
from .services.chat import handle_incoming_message


def register_socketio(sio: socketio.AsyncServer):
    @sio.event
    async def connect(sid, environ):
        await sio.emit("connected", {"sid": sid}, to=sid)

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


