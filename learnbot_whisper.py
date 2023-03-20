import whisper
import requests
import json
import time
import difflib
import datetime
import re
import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text: str, azure_voice):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = azure_voice
    audio_config = speechsdk.AudioConfig(filename="learnbot/"+azure_voice+".mp3")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        return False

def generate_markup_languages(textfile: str, regions: list) -> list:
    with open(textfile) as f:
        lines = f.readlines()
    result = []
    for region in regions:
        region_result = []
        for line in lines:
            if line.startswith(region):
                voice_text = re.sub(r'[^a-zA-Z0-9\-\(\)]', '', line.strip())
                voice_callback = re.sub(r'[^a-zA-Z0-9\-\(\)]', '', line.strip())
                region_result.append({'text': voice_text, 'callback_data': voice_callback.replace('(Male)', '').replace('(Female)', '').replace('(FemaleChild)', '')})
        result.extend([[item] for item in region_result])
    return result

def list_filtered(textfile: str, regions: list) -> list:
    with open(textfile) as f:
        lines = f.readlines()
    result = []
    for region in regions:
        for line in lines:
            if line.startswith(region):
                voice_name = line.strip().split(' ', 1)[0]
                voice_callback = re.sub(r'[^a-zA-Z0-9\-\(\)]', '', line.strip())
                result.append(voice_callback.replace('(Male)', '').replace('(Female)', '').replace('(FemaleChild)', ''))
    return result

def read_msg(offset):
    url = BOT_URL + "/getUpdates?offset=" + str(offset)
    response = requests.get(url).json()

    if response["result"]:
        for i in response["result"]:

            try: # If the user is asking for its ID
                if i["message"]["text"] == "/get_id":
                    send_message_noreply(i["message"]["from"]["id"], "ID:  " + str(i["message"]["from"]["id"]))
            except:
                pass

            with open("learnbot/data.json", "r") as f:
                data = json.load(f)
            
            if 'message' in i:
                user_id = str(i["message"]["from"]["id"])
                if user_id in data or user_id in admin:

                    if 'voice' in i['message'] and type(data[user_id]["current"]) != str:
                        print(datetime.datetime.now().strftime("%H:%M:%S") + ": => voice")
                        resp_media = requests.get(BOT_URL + '/getFile?file_id=' + i["message"]["voice"]["file_id"]) # https://api.telegram.org/bot<token>/getFile?file_id=<file_id>
                        result_transcription = transcribe(resp_media) # high work
                        
                        speech = result_transcription["text"]
                        to_compare = data[user_id]["jobs"][data[user_id]["current"]]["text"]
                        characters = [',', '.', ':', '?', '!', '¿', '¡', "'", '\n']
                        for j in characters:
                            speech = speech.replace(j, '')
                            to_compare = to_compare.replace(j, '')
                        print(datetime.datetime.now().strftime("%H:%M:%S") + ": " +speech)

                        score = round(compare(speech, to_compare, data[user_id]["jobs"][data[user_id]["current"]]["difficulty"]) - 1, 1)
                        print("Score: " + str(score))
                        total = round(data[user_id]["jobs"][data[user_id]["current"]]["current_score"] + score, 1)
                        data[user_id]["jobs"][data[user_id]["current"]]["current_score"] = total

                        emoji = " 😍" if score > 6 else " 😐" if score > 3 else " 😭" if score > 0.0 else " ❗"

                        if data[user_id]["jobs"][data[user_id]["current"]]["current_score"] > data[user_id]["jobs"][data[user_id]["current"]]["target_score"]:
                            send_message(user_id, "Score: " + str(score) + emoji + "\nFinished! 🎉 🎉 🎉 🎉 🎉 Total: " + str(total), i["message"]["message_id"])
                        else:
                            send_message(user_id, "Score: " + str(score) + emoji + "\nTotal: " + str(total), i["message"]["message_id"])
                            data[user_id]["coins"] = data[user_id]["coins"] + score*len(to_compare)/ float(config["ex_rate"])

                    elif 'text' in i['message']:
                        if i['message']['text'] == '/jobs':
                            print(datetime.datetime.now().strftime("%H:%M:%S") + ": => jobs")
                            if not user_id in admin:
                                reply_markup = []
                                for k in range(len(data[user_id]["jobs"])):
                                    a={}
                                    a["text"] = f"{data[user_id]['jobs'][k]['lang']} {k}  ➡️  {data[user_id]['jobs'][k]['current_score']}/{data[user_id]['jobs'][k]['target_score']}"
                                    a["callback_data"] = str(k)
                                    reply_markup.append([a])
                                send_inline(user_id, "=====>              List of jobs              <=====", reply_markup)

                            if user_id in admin:
                                for s in list(data.keys()):
                                    reply_markup = []
                                    for k in range(len(data["5983337071"]["jobs"])):
                                        a={}
                                        a["text"] = f"{data['5983337071']['jobs'][k]['lang']} {k}  ➡️  {data['5983337071']['jobs'][k]['current_score']}/{data['5983337071']['jobs'][k]['target_score']}"
                                        a["callback_data"] = str(k)
                                        reply_markup.append([a])
                                    send_inline(user_id, "=====>        List of jobs (" + str(s) + ")        <=====", reply_markup)

                        elif i['message']['text'] == '/wallet':
                            print(datetime.datetime.now().strftime("%H:%M:%S") + ": => wallet")
                            if user_id in admin:
                                for s in list(data.keys()):
                                    reply_markup = [[{'text':  '+0.1', 'callback_data': s+'#0.1'}, {'text':  '+0.5', 'callback_data': s+'#0.5'}, {'text': '+1', 'callback_data': s+'#1'}, {'text': '+2', 'callback_data': s+'#2'}, {'text': '+5', 'callback_data': s+'#5'}, {'text': '+10', 'callback_data': s+'#10'}]]
                                    send_inline(user_id, "(" + str(s) + ") Balance :  $ " + str(round(data[s]['coins'], 2)), reply_markup) # sends user balance
                            
                            if not user_id in admin:
                                reply_markup = [[{'text': '-0.1', 'callback_data': user_id + '@0.1'}, {'text': '-0.5', 'callback_data': user_id + '@0.5'}, {'text': '-1', 'callback_data': user_id + '@1'}, {'text': '-2', 'callback_data': user_id + '@2'}, {'text': '-5', 'callback_data': user_id + '@5'}, {'text': '-10', 'callback_data': user_id + '@10'}]]
                                send_inline(user_id, "Balance:  $ " + str(round(data[user_id]['coins'], 2)), reply_markup)

                        elif i['message']['text'] == '/voices':
                            print(datetime.datetime.now().strftime("%H:%M:%S") + ": => voices")
                            if not user_id in admin:
                                reply_markup = generate_markup_languages(voices_file, allowed_voices) # languages list and languages filtering
                                send_inline(user_id, "Choose a voice", reply_markup)

                    with open("learnbot/data.json", "w") as f:
                        json.dump(data, f)
            
            if 'callback_query' in i:
                user_id = str(i["callback_query"]["from"]["id"])
                print(datetime.datetime.now().strftime("%H:%M:%S") + ": => " + i['callback_query']['data'])
                if user_id in data or user_id in admin:

                    if "#" in i['callback_query']['data']: # add coins (admin)
                        ammount = i['callback_query']['data'].split("#")
                        data[ammount[0]]["coins"] = data[ammount[0]]["coins"] + float(ammount[1])
                        for s in list(data.keys()):
                            reply_markup = [[{'text': '+0.1', 'callback_data': s+'#0.1'}, {'text': '+0.5', 'callback_data': s+'#0.5'}, {'text': '+1', 'callback_data': s+'#1'}, {'text': '+2', 'callback_data': s+'#2'}, {'text': '+5', 'callback_data': s+'#5'}, {'text': '+10', 'callback_data': s+'#10'}]]
                            send_inline(user_id, "(" + str(ammount[0]) + ") Balance :  $ " + str(round(data[s]['coins'], 2)), reply_markup) # sends users balance

                    elif "@" in i['callback_query']['data']: # rest coins (user)
                        ammount = i['callback_query']['data'].split("@")
                        data[ammount[0]]["coins"] = data[ammount[0]]["coins"] - float(ammount[1])
                        reply_markup = [[{'text': '-0.1', 'callback_data': '@0.1'}, {'text': '-0.5', 'callback_data': '@0.5'}, {'text': '-1', 'callback_data': '@1'}, {'text': '-2', 'callback_data': '@2'}, {'text': '-5', 'callback_data': '@5'}, {'text': '-10', 'callback_data': '@10'}]]
                        send_inline(ammount[0], "Balance:  $ " + str(round(data[ammount[0]]['coins'], 2)), reply_markup)

                    elif not user_id in admin: # Options: integer value
                        lista = list_filtered(voices_file, allowed_voices)
                        if i["callback_query"]["data"] in lista:
                            data[user_id]["voice"] = i["callback_query"]["data"]
                            name = i["callback_query"]["data"]
                            name = name.split('-', 2)[2].split('Neural', 1)[0]
                            send_message_noreply(user_id, "Hi! I am " + name)
                        else:
                            data[user_id]["current"] = int(i["callback_query"]["data"])
                            #send_message_noreply(user_id, data[user_id]["jobs"][data[user_id]["current"]]["text"])
                            azure_voice = data[user_id]["voice"]
                            tts_result = text_to_speech(data[user_id]["jobs"][data[user_id]["current"]]["text"], azure_voice)
                            if tts_result == True:
                                send_audio(user_id, data[user_id]["jobs"][data[user_id]["current"]]["text"], "learnbot/"+azure_voice+".mp3")
                            else:
                                send_message_noreply(user_id, "Sorry, I can't speak 😥\n\n" + data[user_id]["jobs"][data[user_id]["current"]]["text"])
                        
                    with open("learnbot/data.json", "w") as f:
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

def send_audio(chat_id, message, audio_file):
    url = BOT_URL + "/sendAudio"
    data = {
        "chat_id": chat_id,
        "caption": message
    }
    files = {
        "audio": open(audio_file, "rb")
    }
    response = requests.post(url, data=data, files=files)

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
        "commands": [{"command": "jobs", "description": "📖"}, {"command": "wallet", "description": "💵"}, {"command": "get_id", "description": "Get your ID"}, {"command": "voices", "description": "Choose a voice!"}]
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

with open("learnbot/config.json", "r") as f:
    config = json.load(f)

speech_key = config["speech_key"]
service_region = config["service_region"]

allowed_voices = config["allowed_voices"]
voices_file = "learnbot/voices.txt"

token = config["token"]
BOT_URL = 'https://api.telegram.org/bot' + token

admin = config["admin"]

model = whisper.load_model(config["model"])
set_commands()
offset = 0

while True:
    try:
        offset = read_msg(offset)
        time.sleep(0)
    except:
        print("Connection error, restarting...")
        time.sleep(1)
