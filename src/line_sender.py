import requests
ENDPOINTS ={
    "push": "https://api.line.me/v2/bot/message/push",
    "reply": "https://api.line.me/v2/bot/message/reply",
    "broadcast": "https://api.line.me/v2/bot/message/broadcast"
}

def push_message(text: str, user_id: str, token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    try:
        response = requests.post(ENDPOINTS["push"],
                                json=payload,
                                headers=headers)
        response.raise_for_status()
        return response

    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    
def reply_message(text: str, reply_token: str, token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    try:
        response = requests.post(ENDPOINTS["reply"],
                                json=payload,
                                headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    
def broadcast_message(text: str, token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    try:
        response = requests.post(ENDPOINTS["broadcast"],
                                json=payload,
                                headers=headers)
        response.raise_for_status()
        return response
    except  requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    
def send_quick_reply(text: str, options: list, reply_token: str, token: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text,
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type": "message",
                                "label": option,
                                "text": option
                            }
                        }
                        for option in options
                    ]
                }
            }
        ]
    }

    try:
        response = requests.post(ENDPOINTS["reply"],
                                json=payload,
                                headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error sending message: {e}")
        return None