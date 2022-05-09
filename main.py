import time
import httpx
import json
import cloudscraper
from rich.console import Console


def load_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config['access_token'], config['fetch_interval'], config['webhook']


def fprint(color, content):
    console = Console()
    current_time = time.strftime('%r')
    console.print(f'[bold bright_blue][{current_time}][bold {color}] {content}')


def get_giveaways():
    session = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    request = session.get('https://legacy.rbxflip-apis.com/giveaways')
    try:
        response = request.json()
    except json.decoder.JSONDecodeError as json_error:
        fprint("bright_red", json_error)
        return None
    
    return response['data'].get('giveaways')


def get_image(item_id, client):
    console = Console()
    try:
        item_image = client.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={item_id}&size=420x420&format=Png&isCircular=false").json()['data'][0]['imageUrl']
    except Exception:
        fprint("bright_red", f"Image fetch failed, exception: {Exception}")
        return
    return item_image


def send_webhook(webhook, client, item_image, giveaway_id):
    console = Console()
    data = {
        "content": "",
        "embeds": [
            {
                "title": "RBXFlip Giveaway Joiner",
                "description": f"Giveaway joined!\n\nGiveaway ID: {giveaway_id}",
                "color": 10085589,
                "thumbnail": {
                    "url": item_image
                }
            }
        ],
        "username": "RFGJ",
        "avatar_url": "https://i.imgur.com/KMTZO4n.jpeg",
        "attachments": []
    }

    response = client.post(webhook, json=data)

    if response.status_code == 204 or response.status_code == 200:
        fprint("bright_green", "Successfully sent webhook.")

    else:
        fprint("bright_red", f"Something went wrong when sending a webhook. Check the following response: {response}")

    try:
        response.raise_for_status()
    except httpx.HTTPError as error:
        print(error)


class User:
    def __init__(self, flip_token, webhook):
        self.flip_token = flip_token
        self.joined = []
        self.client = httpx.Client()
        self.client.headers = {'authorization': f'Bearer {self.flip_token}'}
        self.webhook = webhook

    def join_giveaway(self, giveaway):
        console = Console()
        giveaway_id = giveaway['_id']
        if giveaway_id in self.joined:
            return

        with console.status(f"[bold bright_blue][{time.strftime('%r')}][bold bright_yellow] Attempting to join giveaway {giveaway_id}.", spinner_style="[bold bright_yellow]") as status:
            try:
                request = self.client.put(f'https://legacy.rbxflip-apis.com/giveaways/{giveaway_id}')
            except Exception as error:
                print(f"error: {error}")
                return
            if request.status_code == 200:
                self.joined.append(giveaway_id)
                time.sleep(0.5)
                status.stop()
                fprint("bright_green", f"Giveaway (ID:{giveaway_id}) successfully joined. Sending embed to webhook.")
                item_image = get_image(giveaway['item']['assetId'], self.client)
                send_webhook(self.webhook, self.client, item_image, giveaway_id)

            else:
                time.sleep(0.5)
                status.stop()
                fprint("bright_red", f"Something went wrong when joining Giveaway (ID:{giveaway_id}). Check the following response: {request.text}")


def main():
    console = Console()
    flip_token, fetch_interval, webhook = load_config()
    user = User(flip_token, webhook)
    while 1:
        with console.status("[bold light_goldenrod1]Fetching giveaways...", spinner_style="bright_yellow") as status:
            giveaways = get_giveaways()
            time.sleep(0.5)
        if giveaways:
            for giveaway in giveaways:
                if giveaway['_id'] not in user.joined:
                    if giveaway['status'] != "Open":
                        fprint("light_goldenrod1", f"Giveaway #{giveaways.index(giveaway) + 1} (ID:{giveaway['_id']}) is closed.")
                    elif giveaway['status'] == "Open":
                        fprint("light_goldenrod1", f"Giveaway #{giveaways.index(giveaway) + 1} (ID:{giveaway['_id']}) is open. Queuing this giveaway.")
                        user.join_giveaway(giveaway)
        else:
            fprint("light_goldenrod1", "No giveaways found.")

        time.sleep(fetch_interval)
        
        
if __name__ == "__main__":
    main()
