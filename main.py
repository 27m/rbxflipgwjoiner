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
    except:
        return "none"
    return itemimage


def join_giveaway(giveawayid, fliptoken):
    headers = {
        "authorization": "Bearer " + fliptoken
    }
    resp = requests.put(f'https://legacy.rbxflip-apis.com/giveaways/{giveawayid}', headers=headers)
    return resp.status_code


def send_webhook(webhook, itemimageurl, id):
    data = {
        "content": "",
        "embeds": [
            {
                "title": "RBXFlip Giveaway Joiner",
                "description": f"Giveaway joined!\n\n[Giveaway ID: {id}](",
                "color": 10085589,
                "thumbnail": {
                    "url": itemimageurl
                }
            }
        ],
        "username": "RFGJ",
        "avatar_url": "https://i.imgur.com/KMTZO4n.jpeg",
        "attachments": []
    }

    resp = requests.post(webhook, json=data)

    if resp.status_code == 204 or resp.status_code == 200:
        return "Successfully sent webhook."
    else:
        print(f"Something went wrong when sending a webhook. Status Code: {resp.status_code}")
        try:
            resp.raise_for_status()
        except requests.HTTPError as error:
            print(error)


def main():
    token, interval, webhook = load_config()

    if input("debugging on? (only turn this on if asked to) | y or n ").lower() == "y":
        debugging = True
    else:
        debugging = False
    while True:
        giveaways = get_giveaways()

        if debugging:
            print(giveaways)

        if giveaways and giveaways[1][0]:
            giveaway = giveaways[1][0]

            if giveaway['status'] == "Open":
                response = join_giveaway(giveaway['_id'], token)

                if response == 200:
                    image = get_image(giveaway['item']['assetId'])
                    id = giveaway['_id']
                    print(send_webhook(webhook, image, id))
                else:
                    print(response)

            elif giveaway['status'] != "Open":
                print("No open giveaways found.")

        elif not giveaways:
            print("No giveaways found.")
        time.sleep(interval)


if __name__ == "__main__":
    main()
