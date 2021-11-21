import json
from time import sleep

from colordict import *
import requests


auth_token = 'TEwBLmv_4j6PhA2gRd6Zs_IwiUs'

colors = ColorDict()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth_token}"
}


def add_text_item(content):
    if not content:
        content = 'Empty note'

    url = "https://api.miro.com/v2/boards/o9J_linzwIA%3D/texts"

    payload = {
        "data": {"content": content},
        "style": {
            "backgroundColor": "#e6e6e6",
            "backgroundOpacity": "1.0",
            "fontFamily": "arial",
            "textAlign": "left"
        },
        "geometry": {
            "x": "100.0",
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

    # print(response.text)


sticky_notes_x = 0
sticky_notes_y = 0


def add_sticky_note(content, color):
    global sticky_notes_x, sticky_notes_y
    x = 100 + sticky_notes_x * 150
    y = 500 + sticky_notes_y * 150

    if sticky_notes_x == 0:
        sticky_notes_x = sticky_notes_y + 1
        sticky_notes_y = 0
    elif sticky_notes_x > sticky_notes_y:
        sticky_notes_y += 1
    else:
        sticky_notes_x -= 1

    width = 200

    if not content:
        content = 'Empty note'
    if not color:
        color = 'yellow'

    print(f'created a sticky note with text={content}, color={color}')
    # return

    url = "https://api.miro.com/v2/boards/o9J_linzwIA%3D/sticky_notes"

    payload = {
        "data": {"content": content},
        "style": {"backgroundColor": color,
                  "textAlign": "center",
                  "textAlignVertical": "top"
        },
        "geometry": {
            "x": x,
            "y": y,
            "width": width,
            "rotation": "0"
        }
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)


def get_sticky_note(index, column_header):
    try:
        assert column_header in column_headers
    except:
        return 'Perkele! This column was not found.'

    column_index = column_headers.index(column_header)
    try:
        assert 0 < index <= len(cards[column_index])
    except:
        return 'Perkele! This card was not found.'

    index -= 1

    return cards[column_index][index][1]


def add_column_template(column_names: list, height=600):
    global cards, column_headers, frame_height
    cards = [[] for _ in range(len(column_names))]

    frame_height = height

    column_headers = column_names

    column_x = 0
    for column_name in column_names:
        add_rectangle(column_x, 0, 320, height, "#ffffff")
        add_card(column_name, column_x, -height/2+50, 300, 200, color='red')

        column_x += 330

    column_headers = [c.lower() for c in column_names]

    print('created a column template')


def add_rectangle(x, y, width, height, background_color):
    if not x:
        x = 0
    if not y:
        y= 0
    if not width:
        width = 320
    if not height:
        height = 600
    if not background_color:
        background_color = "#ffffff"

    url = "https://api.miro.com/v2/boards/o9J_linzwIA=/shapes"

    payload = {
        "data": {
            "content": "",
            "shapeType": "rectangle"
        },
        "style": {
            "backgroundColor": background_color,
            "backgroundOpacity": "1.0",
            "fontFamily": "arial",
            "fontSize": "14",
            "borderColor": "#1a1a1a",
            "borderWidth": "2.0",
            "borderOpacity": "0.0",
            "borderStyle": "normal",
            "textAlign": "center"
        },
        "geometry": {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "rotation": "0"
        }
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)


def add_card(text, x, y, width=300, height=200, color='#2d9bf0'):
    if not color.startswith('#'):
        color = '#%02x%02x%02x' % tuple([int(i) for i in colors[color]])

    print('adding a card, color:', color)

    url = "https://api.miro.com/v2/boards/o9J_linzwIA=/cards"
    payload = {
        "data": {
            "title": text
        },
        "style": {"cardTheme": color},
        "geometry": {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "rotation": "0.0"
        }
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return json.loads(response.text)['id']


def delete_card(id):
    url = f"https://api.miro.com/v2/boards/o9J_linzwIA=/widgets/{id}"

    response = requests.request("DELETE", url, headers=headers)


def move_card(id, x, y):
    url = f"https://api.miro.com/v2/boards/o9J_linzwIA=/widgets/{id}/position"

    payload = {
        "x": x,
        "y": y
    }

    response = requests.request("PATCH", url, json=payload, headers=headers)


def add_card_to_frame(text, column_header, color=None):
    if not color:
        color = '#2d9bf0'

    column_header = column_header.lower()

    if column_header not in column_headers:
        print(f"error: {column_header} not in column headers (maybe you haven't created the frame?)")
        print('column headers rn:', column_headers)
        return

    column_index = column_headers.index(column_header)
    id = add_card(text, 330 * column_index, -frame_height/2 + 140 + 90 * len(cards[column_index]), color=color)
    cards[column_index].append((id, text))


def delete_card_from_frame(index, column_header):
    global column_headers, cards
    column_header = column_header.lower()

    assert column_header in column_headers
    column_index = column_headers.index(column_header)
    assert 0 < index <= len(cards[column_index])

    index -= 1

    id, text = cards[column_index][index]
    cards[column_index].remove((id, text))
    delete_card(id)
    for i in range(len(cards[column_index])):
        if i >= index:
            id = cards[column_index][i][0]
            move_card(id, 330 * column_index, -frame_height/2 + 140 + 90 * i)


def move_card_in_frame(index, from_column, to_column):
    global column_headers, cards, frame_height
    from_column = from_column.lower()
    to_column = to_column.lower()

    assert to_column in column_headers

    assert from_column in column_headers
    column_index = column_headers.index(from_column)
    id, text = cards[column_index][index-1]

    add_card_to_frame(text, to_column)

    # don't decrement the index before delete_card_from_frame()
    delete_card_from_frame(index, from_column)


column_headers = []
cards = []
frame_height = 0

# add_column_template(['To do', 'In progress', 'Done'])
# add_card('im bored', 10, 10, 256, 30, color='grey')
add_column_template(['Backlog', 'In progress', 'Done'])
add_card_to_frame('the presentation', 'done')
add_card_to_frame('photos', 'done')
add_card_to_frame('website', 'done')
add_card_to_frame('getting off the corn addiction', 'done')

sleep(1)

move_card_in_frame(2, 'done', 'backlog')

