import asyncio
import websockets
import json
from datetime import datetime
import logging

# logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# colors (UI)
RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def format_time(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")


async def send_messages(ws):
    while True:
        try:
            msg = await asyncio.to_thread(input, f"{CYAN}You: {RESET}")
            await ws.send(msg)
            logger.info(f"Sent message: {msg}")
        except Exception as e:
            logger.error(f"Send error: {e}")
            break


async def receive_messages(ws):
    while True:
        try:
            response = await ws.recv()
            logger.info(f"Received raw: {response}")

            try:
                data = json.loads(response)

                # Chat message
                if "message" in data:
                    time_str = format_time(data["timestamp"])
                    print(f"\n{BLUE}[{time_str}] {data['username']}: {data['message']}{RESET}")

                # ACK
                elif "status" in data:
                    print(f"\n{GREEN}✔ Message sent{RESET}")

                # Other info
                else:
                    print(f"\n{YELLOW}{data}{RESET}")

            except json.JSONDecodeError:
                print(f"\n{YELLOW}{response}{RESET}")

            print(f"{CYAN}You: {RESET}", end="", flush=True)

        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed by server")
            print(f"\n{YELLOW}Disconnected from server{RESET}")
            break
        except Exception as e:
            logger.error(f"Receive error: {e}")
            break


async def chat():
    uri = "ws://127.0.0.1:8000/ws"

    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to server")
            print(f"{GREEN}Connected to server ✅{RESET}")

            username = input("Enter username: ").strip()
            topic = input("Enter topic: ").strip()

            join_payload = {
                "username": username,
                "topic": topic
            }

            await websocket.send(json.dumps(join_payload))
            logger.info(f"Join sent: {join_payload}")

            response = await websocket.recv()
            logger.info(f"Join response: {response}")
            print(f"{YELLOW}{response}{RESET}")

            await asyncio.gather(
                send_messages(websocket),
                receive_messages(websocket)
            )

    except Exception as e:
        logger.error(f"Connection failed: {e}")


asyncio.run(chat())