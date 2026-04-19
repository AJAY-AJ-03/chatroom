# 📡 Real-Time WebSocket Chat Server (FastAPI)

A lightweight real-time chat application built using **FastAPI WebSockets**.  
It supports **topic-based chat rooms**, **real-time messaging**, **unique usernames**, and **message expiry**.

---

## 🚀 Features

- 🔌 WebSocket-based real-time communication  
- 🏷️ Topic-based chat rooms (e.g., sports, movies)  
- 👤 Unique username handling (`alice`, `alice#2`, etc.)  
- 💬 Real-time message broadcasting  
- 📜 `/list` command (JSON response of active topics)  
- ⏳ Automatic message expiry after 30 seconds  
- 🔄 Automatic cleanup of empty topics  
- ⚡ In-memory storage (no database required)  
- 🧾 Logging for debugging and monitoring  

---

## 🧱 Tech Stack

- Python 3.9+  
- FastAPI  
- Uvicorn  
- WebSockets (`websockets` library)  

---

## 📁 Project Structure
chatroom/
│── main.py # WebSocket server (FastAPI)
│── client_example.py # Interactive WebSocket client
│── README.md # Documentation

text

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/AJAY-AJ-03/chatroom.git
cd chatroom
2. Create a virtual environment (optional)
bash
python -m venv venv
Windows:

bash
venv\Scripts\activate
Mac/Linux:

bash
source venv/bin/activate
3. Install dependencies
bash
pip install fastapi uvicorn websockets
▶️ How to Run Server
Start the FastAPI WebSocket server:

bash
uvicorn main:app --reload
Server will run at:

HTTP: http://127.0.0.1:8000

WebSocket: ws://127.0.0.1:8000/ws

💻 How to Run Client
Run the client in a separate terminal:

bash
python client_example.py
Enter details when prompted:

text
Enter username: Ajay
Enter topic: sports
💬 How to Use
1. Join a Topic
When the client starts, it sends:

json
{"username": "Ajay", "topic": "sports"}
2. Send Messages
Type any message:

text
hello everyone
3. List Active Topics
Type:

text
/list
Response:

json
{
  "event": "list",
  "topics": [
    {
      "topic": "sports",
      "users": 2,
      "label": "users"
    }
  ]
}
⏳ Message Expiry
Messages automatically expire after 30 seconds

Expired messages are removed from memory

Expiry events are logged on the server

🔄 Session Behavior
User disconnect → removed from topic

Topic becomes empty → automatically deleted

Duplicate usernames → auto-renamed (#2, #3, etc.)

📊 Example Flow
User A joins sports

User B joins sports

They chat in real-time

/list shows active topics

Messages expire after 30 seconds

If all users leave → topic is removed

🧪 Testing Scenarios
✅ Two users chat in the same topic

✅ Users in different topics are isolated

✅ /list shows correct user counts

✅ Messages expire after 30 seconds

✅ Topics are deleted when empty

✅ Invalid JSON is handled safely

🧠 Notes
Uses in-memory storage only

No database required

Designed for learning and assignment purposes

Easily extendable using Redis or a database

👨‍💻 Author
Ajay Rathnam
Built using FastAPI WebSockets for real-time communication practice.