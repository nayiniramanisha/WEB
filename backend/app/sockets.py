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
        print(f"🔍 SOCKET: Received chat_message from {sid}: {data}")
        try:
            response = await handle_incoming_message(data)
            print(f"🔍 SOCKET: Emitting bot_message with related field: {response.get('related', [])}")
            print(f"🔍 SOCKET: Full response: {response}")
            await sio.emit("bot_message", response, to=sid)
        except Exception as e:
            print(f"🔍 SOCKET: Error processing chat_message: {e}")
            error_response = {"session_id": data.get("session_id"), "role": "assistant", "content": "Sorry, I encountered an error. Please try again.", "related": []}
            await sio.emit("bot_message", error_response, to=sid)


