import whisper
import requests
import json
import time
import difflib

def read_msg(offset):
    url = BOT_URL + "/getUpdates?offset=" + str(offset)
    response = requests.get(url).json()

    if response["result"]:
        for i in response["result"]:

            with open("data.json", "r") as f:
                data = json.load(f)
            
            if 'message' in i:
                user_id = str(i["message"]["from"]["id"])
                if user_id in data:

                    if 'voice' in i['message'] and type(data[user_id]["current"]) != str:
                        resp_media = requests.get(BOT_URL + '/getFile?file_id=' + i["message"]["voice"]["file_id"]) # https://api.telegram.org/bot<token>/getFile?file_id=<file_id>
                        result_transcription = transcribe(resp_media) # high work
                        
                        speech = result_transcription["text"]
                        to_compare = data[user_id]["jobs"][data[user_id]["current"]]["text"]
                        characters = [',', '.', ':', '?', '!', '¿', '¡', "'", '\n']
                        for j in characters:
                            speech = speech.replace(j, '')
                            to_compare = to_compare.replace(j, '')
                        print(speech)

                        score = round(compare(speech, to_compare, data[user_id]["jobs"][data[user_id]["current"]]["dificulty"]) - 1, 1)
                        print(score)
                        total = round(data[user_id]["jobs"][data[user_id]["current"]]["current_score"] + score, 1)
                        data[user_id]["jobs"][data[user_id]["current"]]["current_score"] = total

                        emoji = " 😍" if score > 6.6 else " 😐" if score > 3.3 else " 😭" if score > 3.3 else " ❗"

                        if data[user_id]["jobs"][data[user_id]["current"]]["current_score"] > data[user_id]["jobs"][data[user_id]["current"]]["target_score"]:
                            send_message(user_id, "Score: " + str(score) + emoji + "\nFinished! 🎉 🎉 🎉 🎉 🎉 Total: " + str(total), i["message"]["message_id"])
                        else:
                            send_message(user_id, "Score: " + str(score) + emoji + "\nTotal: " + str(total), i["message"]["message_id"])
                            data[user_id]["coins"] = data[user_id]["coins"] + score*len(to_compare)/5000

                    elif 'text' in i['message']:
                        if i['message']['text'] == '/jobs':
                            if not user_id in admin:
                                reply_markup = []
                                for k in range(len(data[user_id]["jobs"])):
                                    a={}
                                    a["text"] = f"{data[user_id]['jobs'][k]['lang']} {k}  ➡️  {data[user_id]['jobs'][k]['current_score']}/{data[user_id]['jobs'][k]['target_score']}"
                                    a["callback_data"] = str(k)
                                    reply_markup.append([a])

                                send_inline(user_id, "====>               List of jobs               <====", reply_markup)
                            
                        elif i['message']['text'] == '/wallet':
                            if user_id in admin:
                                reply_markup = [[{'text': '+0.5', 'callback_data': '+0.5'}, {'text': '+1', 'callback_data': '+1'}, {'text': '+2', 'callback_data': '+2'}, {'text': '+5', 'callback_data': '+5'}, {'text': '+10', 'callback_data': '+10'}]]
                                send_inline(user_id, "Balance:  $ " + str(round(data[student_id]['coins'], 2)), reply_markup) # sends julias balance
                            else:
                                reply_markup = [[{'text': '-0.5', 'callback_data': '-0.5'}, {'text': '-1', 'callback_data': '-1'}, {'text': '-2', 'callback_data': '-2'}, {'text': '-5', 'callback_data': '-5'}, {'text': '-10', 'callback_data': '-10'}]]
                                send_inline(user_id, "Balance:  $ " + str(round(data[user_id]['coins'], 2)), reply_markup)

                    with open("data.json", "w") as f:
                        json.dump(data, f)
            
            if 'callback_query' in i:
                user_id = str(i["callback_query"]["from"]["id"])
                if user_id in data:

                    if i['callback_query']['data'] in ['-0.5', '+0.5', '-1', '+1', '-2', '+2', '-5', '+5', '-10', '+10']:
                        data[student_id]["coins"] = data[student_id]["coins"] + float(i['callback_query']['data'])

                        if user_id in admin:
                            reply_markup = [[{'text': '+0.5', 'callback_data': '+0.5'}, {'text': '+1', 'callback_data': '+1'}, {'text': '+2', 'callback_data': '+2'}, {'text': '+5', 'callback_data': '+5'}, {'text': '+10', 'callback_data': '+10'}]]
                            send_inline(user_id, "Balance:  $ " + str(round(data[student_id]['coins'], 2)), reply_markup) # sends julias balance
                        else:
                            reply_markup = [[{'text': '-0.5', 'callback_data': '-0.5'}, {'text': '-1', 'callback_data': '-1'}, {'text': '-2', 'callback_data': '-2'}, {'text': '-5', 'callback_data': '-5'}, {'text': '-10', 'callback_data': '-10'}]]
                            send_inline(user_id, "Balance:  $ " + str(round(data[user_id]['coins'], 2)), reply_markup)

                    elif not user_id in admin: # Options: integer value
                        data[user_id]["current"] = int(i["callback_query"]["data"])
                        send_message_noreply(user_id, data[user_id]["jobs"][data[user_id]["current"]]["text"])
                        
                    with open("data.json", "w") as f:
                        json.dump(data, f)

        return response["result"][-1]["update_id"] + 1
    else:
        return offset

def send_message(chat_id, message, reply):
    url = BOT_URL + "/sendMessage?chat_id=" + str(chat_id) + "&text=" + message + "&reply_to_message_id=" + str(reply)
    response = requests.get(url)

def send_message_noreply(chat_id, message):
    url = BOT_URL + "/sendMessage?chat_id=" + str(chat_id) + "&text=" + message
    response = requests.get(url)

def send_inline(chat_id, message, reply_markup):
    url = BOT_URL + '/sendMessage'
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": {
            "inline_keyboard": reply_markup,
            },
        }
    data = json.dumps(data)
    resp = requests.post(url, data=data, headers=headers)

def set_commands():
    url = BOT_URL + "/setMyCommands"
    headers = {"Content-Type": "application/json"}
    data = {
        "commands": [{"command": "jobs", "description": "📖"}, {"command": "wallet", "description": "💵"}]
        }
    data = json.dumps(data)
    resp = requests.post(url, data=data, headers=headers)

def transcribe(resp_media):
    response_media = resp_media.json()
    url_media = 'https://api.telegram.org/file/bot' + token + '/' + response_media['result']["file_path"] # https://api.telegram.org/file/bot<token>/<file_path>
    return model.transcribe(url_media)

def compare(text1, text2, dificulty):
    sequence = difflib.SequenceMatcher(isjunk=None, a=text1, b=text2)
    return (sequence.ratio() ** dificulty) * 11

##################################################################################################################################

token = 'BotToken'
BOT_URL = 'https://api.telegram.org/bot' + token

sudent_id = "5983337071"
admin = {'649792299', '316747837'}

model = whisper.load_model("medium")
set_commands()
offset = 0

while True:
    try:
        offset = read_msg(offset)
        time.sleep(0)
    except:
        print("Connection error, restarting...")
        time.sleep(2)
