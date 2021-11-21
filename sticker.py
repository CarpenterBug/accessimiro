import requests

url = "https://api.miro.com/v2/boards/o9J_linzwIA%3D/sticky_notes"

payload = {
    "data": {"content": "sample sticky note"},

    "style": {
        "backgroundColor": "light_yellow",
        "textAlign": "center",
        "textAlignVertical": "top"
    },
    "geometry": {
        "x": "0.0",
        "y": "0.0",
        "width": "200",
        "rotation": "0"
    }
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer 2-AEzXjtVydsb8NiicnILGwrw64"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)