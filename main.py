from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import time
import asyncio
import logging

#  Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

topics = {}
messages = {}  


def make_unique_username(topic, username):
    existing = [user["username"] for user in topics.get(topic, [])]

    if username not in existing:
        return username

    count = 2
    while f"{username}#{count}" in existing:
        count += 1

    return f"{username}#{count}"

# Message expiry
async def expire_message(topic, message_data):
    await asyncio.sleep(30)

    if topic in messages and message_data in messages[topic]:
        messages[topic].remove(message_data)
        logger.info(f"Expired message removed from {topic}: {message_data}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")

    username = None
    topic = None

    try:
        try:
            data = await websocket.receive_text()
            data = json.loads(data)
        except json.JSONDecodeError:
            await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
            await websocket.close()
            return

        username = data.get("username")
        topic = data.get("topic")

        if not username or not topic:
            await websocket.send_text(json.dumps({"error": "Invalid join data"}))
            await websocket.close()
            return

        topic = topic.strip().lower()
        username = username.strip()

        if topic not in topics:
            topics[topic] = []
            messages[topic] = []

        username = make_unique_username(topic, username)

        topics[topic].append({
            "username": username,
            "ws": websocket
        })

        logger.info(f"{username} joined {topic}")

        # JOIN response
        await websocket.send_text(json.dumps({
            "event": "join",
            "status": "success",
            "username": username,
            "topic": topic
        }))

        while True:
            try:
                raw_msg = await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break

            if not raw_msg.strip():
                continue

            if raw_msg.strip() == "/list":
                topic_list = []

                for t, users in topics.items():
                    count = len(users)
                    label = "user" if count == 1 else "users"

                    topic_list.append({
                        "topic": t,
                        "users": count,
                        "label": label
                    })

                await websocket.send_text(json.dumps({
                    "event": "list",
                    "topics": topic_list if topic_list else []
                }))
                continue

            #  MESSAGE 
            message_data = {
                "username": username,
                "message": raw_msg,
                "timestamp": int(time.time())
            }

            messages[topic].append(message_data)

            #  BROADCAST 
            dead_users = []

            for user in topics.get(topic, []):
                if user["ws"] != websocket:
                    try:
                        await user["ws"].send_text(json.dumps(message_data))
                    except:
                        dead_users.append(user)

            for dead in dead_users:
                topics[topic].remove(dead)

            #  ACK 
            await websocket.send_text(json.dumps({
                "status": "sent"
            }))

            #  EXPIRY 
            asyncio.create_task(expire_message(topic, message_data))

    except WebSocketDisconnect:
        logger.info(f"{username} disconnected")

    finally:
        #  CLEANUP 
        if topic and topic in topics:
            topics[topic] = [
                user for user in topics[topic]
                if user["ws"] != websocket
            ]

            logger.info(f"{username} removed from {topic}")

            if not topics[topic]:
                del topics[topic]
                if topic in messages:
                    del messages[topic]
                logger.info(f"{topic} deleted (empty)")