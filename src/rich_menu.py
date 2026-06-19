import requests
import os
import io
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from config import QUICK_TOPICS

load_dotenv()
token = os.getenv("CHANNEL_ACCESS_TOKEN")

def create_rich_menu_image(labels: list, button_width: int) -> bytes:
    img = Image.new("RGB", (2500, 843), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_path = os.path.join(os.path.dirname(__file__), "../fonts/NotoSansJP-Regular.ttf")
    try:
        font = ImageFont.truetype(font_path, 80)
    except OSError:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 80)
        except OSError:
            font = ImageFont.load_default(size=80)


    for i, label in enumerate(labels):
        x = i * button_width
        draw.rectangle([x, 0, x + button_width, 843], outline=(200, 200, 200), width=3)
        draw.text((x + button_width // 2, 421), label, fill=(0, 0, 0), anchor="mm", font=font)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def create_rich_menu():
    button_width = 2500 // len(QUICK_TOPICS)

    areas = [
        {
            "bounds": {
                "x": i * button_width,
                "y": 0,
                "width": button_width,
                "height": 843
            },
            "action": {"type": "message", "text": label}
        }
        for i, label in enumerate(QUICK_TOPICS)
    ]

    rich_menu = {
        "size": {"width": 2500, "height": 843},
        "selected": True,
        "name": "トピック設定メニュー",
        "chatBarText": "メニューを開く",
        "areas": areas
    }

    try:
        response = requests.post(
            "https://api.line.me/v2/bot/richmenu",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=rich_menu
        )
        response.raise_for_status()
        rich_menu_id = response.json()["richMenuId"]

        image_data = create_rich_menu_image(QUICK_TOPICS, button_width)

        response = requests.post(
            f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "image/png"
            },
            data=image_data
        )
        response.raise_for_status()

        response = requests.post(
            f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        print("create richmenu")
        return rich_menu_id
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None