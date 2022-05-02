import time
import requests
import json


def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['access_token'], config['fetch_interval'], config['webhook']


def get_giveaways():
    giveaways = []
    try:
        resp = requests.get("https://legacy.rbxflip-apis.com/giveaways")
        resp.raise_for_status()
        giveaways = resp.json()['data']['giveaways']
    except Exception:
        print(Exception)

    if giveaways and resp.status_code == 200:
        "Successfully fetched an active giveaway."
        return True, giveaways
    else:
        return False


def get_image(itemid):
    try:
        itemimage = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={itemid}&size=420x420&format=Png&isCircular=false").json()['data'][0]['imageUrl']
    except Exception:
        return f"Image fetch failed, exception: {Exception}"
    return itemimage


def join_giveaways(giveaways: list, fliptoken):
    joinedgiveaways = []
    with requests.Session() as session:
        for giveaway in giveaways:
            giveawayid = giveaway['_id']
            headers = {
                "authorization": f"Bearer {fliptoken}"
            }
            resp = session.put(f'https://legacy.rbxflip-apis.com/giveaways/{giveawayid}', headers=headers)
            resp.raise_for_status()
            joinedgiveaways.append((giveawayid, giveaway['item']['assetId']))
    return joinedgiveaways


def send_webhooks(webhook, joinedgiveaways: list):
    for giveawaytuple in joinedgiveaways:
        giveawayid, assetId = giveawaytuple
        image = get_image(assetId)
        data = {
            "content": "",
            "embeds": [
                {
                    "title": "RBXFlip Giveaway Joiner",
                    "description": f"Giveaway joined!\n\nGiveaway ID: {giveawayid}",
                    "color": 10085589,
                    "thumbnail": {
                        "url": image
                    }
                }
            ],
            "username": "RFGJ",
            "avatar_url": "https://i.imgur.com/KMTZO4n.jpeg",
            "attachments": []
        }

        resp = requests.post(webhook, json=data)

        if resp.status_code == 204 or resp.status_code == 200:
            print("Successfully sent webhook.")
        else:
            print(f"Something went wrong when sending a webhook. Status Code: {resp.status_code}")
            try:
                resp.raise_for_status()
            except requests.HTTPError as error:
                print(error)


def main():
    token, interval, webhook = load_config()

    if input("Debugging on? (only turn this on if asked to.) | Y or N | ").lower() == "y":
        debugging = True
    else:
        debugging = False
    while True:
        giveaways = get_giveaways()

        if debugging:
            print(giveaways)
        opengiveaways = []

        if giveaways:
            for giveaway in giveaways[1]:

                if giveaway['status'] == "Open":
                    opengiveaways.append(giveaway)

            if opengiveaways:
                joinedgiveaways = join_giveaways(opengiveaways, token)
                send_webhooks(webhook, joinedgiveaways)

            elif not opengiveaways:
                print("No open giveaways found.")

        elif not giveaways:
            print("No giveaways found.")
        time.sleep(interval)


if __name__ == "__main__":
    main()
