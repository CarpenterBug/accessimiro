import speech_recognition as sr
from wit import Wit
from miro import *

WIT_API_KEY = "TAS4VSQRWLVL554LN3TCXJQUXQ7ABMAL"
client = Wit(WIT_API_KEY)


def classify(data):
    print('text:', data['text'])
    entities: dict = {}
    e: dict = data['entities']
    print(e)
    for entity in e.keys():
        entities[entity.split(':')[1]] = e[entity][0]['value']

    print('intents:', data['intents'])
    print(entities)

    for intent in data['intents']:
        if intent['name'] == 'create_note':
            add_sticky_note(entities.get('content'), entities.get('color'))
        elif intent['name'] == 'create_text':
            add_text_item(entities.get('content'))
        elif intent['name'] == 'create_card':
            add_card_to_frame(entities.get('content'), entities.get('column'), color=entities.get('color'))
        elif intent['name'] == 'create_shape':
            add_rectangle(entities.get('x'), entities.get('y'), entities.get('width'), entities.get('height'),
                          entities.get('color'))
        elif intent['name'] == 'read':
            return get_sticky_note(entities.get('ordinal'), entities.get('column'))
            # read_back('bruh')
        elif intent['name'] == 'create_frame':
            templates = {'kanban': ['Backlog', 'In progress', 'Done'],
                         'retrospective': ['Start', 'Stop', 'Continue']}

            if not entities.get('type'):
                columns = templates['kanban']
            else:
                columns = templates[entities.get('type')]

            add_column_template(columns)
        elif intent['name'] == 'move_object':
            move_card_in_frame(entities.get('ordinal'), entities.get('from'), entities.get('to'))
        elif intent['name'] == 'delete_object':
            delete_card_from_frame(entities.get('ordinal'), entities.get('column'))

    return None


def read():
    query = input("Type something!\n")
    res = client.message(query)

    classify(res)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print('sending to wit')

    res = client.speech(audio.get_wav_data(), {'Content-Type': 'audio/wav'})
    classify(res)


if __name__ == '__main__':
    # read()
    # read_back('kanban')
    listen()
import speech_recognition as sr
from wit import Wit
from miro import *

WIT_API_KEY = "TAS4VSQRWLVL554LN3TCXJQUXQ7ABMAL"
client = Wit(WIT_API_KEY)


def classify(data):
    print('text:', data['text'])
    entities: dict = {}
    e: dict = data['entities']
    for entity in e.keys():
        entities[entity.split(':')[1]] = e[entity][0]['value']

    print('intents:', data['intents'])
    print(entities)

    for intent in data['intents']:
        if intent['name'] == 'create_note':
            add_sticky_note(entities.get('content'), entities.get('color'))
        elif intent['name'] == 'create_text':
            add_text_item(entities.get('content'))
        elif intent['name'] == 'create_card':
            add_card_to_frame(entities.get('content'), entities.get('column'), color=entities.get('color'))
        elif intent['name'] == 'create_shape':
            add_rectangle(entities.get('x'), entities.get('y'), entities.get('width'), entities.get('height'),
                          entities.get('color'))
        elif intent['name'] == 'read':
            return get_sticky_note(entities.get('ordinal'), entities.get('column'))
            # read_back('bruh')
        elif intent['name'] == 'create_frame':
            templates = {'kanban': ['Backlog', 'In progress', 'Done'],
                         'retrospective': ['Start', 'Stop', 'Continue']}

            if not entities.get('type'):
                columns = templates['kanban']
            else:
                columns = templates[entities.get('type')]

            add_column_template(columns)
        elif intent['name'] == 'move_object':
            move_card_in_frame(entities.get('ordinal'), entities.get('from'), entities.get('to'))
        elif intent['name'] == 'delete_object':
            delete_card_from_frame(entities.get('ordinal'), entities.get('column'))

    return None


def read():
    query = input("Type something!\n")
    res = client.message(query)

    classify(res)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print('sending to wit')

    res = client.speech(audio.get_wav_data(), {'Content-Type': 'audio/wav'})
    classify(res)


if __name__ == '__main__':
    # read()
    # read_back('kanban')
    listen()
