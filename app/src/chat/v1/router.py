from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse

from src.user.schema import UserSchema
from src.database import database
from src.auth.security import get_current_user
from src.crud.crud_chat import crud_chat
from src.chat.schema import ChatListSchema, ChatBase, ChatSchema

chat_router = APIRouter(prefix='/im',)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/im/websocket");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@chat_router.get("/", response_model=ChatListSchema)
async def get(sel: int | None = None,
              current_user: UserSchema = Depends(get_current_user)):
    chats = await crud_chat.read(database, current_user)
    chat_list = []
    for chat in chats:
        if chat.id_1 != current_user.id:
            chat_user = ChatSchema(id=chat.id, sel=UserSchema(id=chat.id_1, username=chat.username))
        else:
            chat_user = ChatSchema(id=chat.id, sel=UserSchema(id=chat.id_2, username=chat.username_1))
        chat_list.append(chat_user)
    response = ChatListSchema(chats=chat_list)
    return response


@chat_router.websocket('/websocket')
async def get_im(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
    return 