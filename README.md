# Study-languages-using-telegram-and-whisper

Send an audio to telegram bot, it will reply with a score (from -1 to 10) based in your pronounciation. _data.json_ is used to store the texts to read, the scores and the target scores, addicionally, the bot generates *coins* when the pronounciation is correct to incentivate its use on kids.

## FEATURES

1. Uses whisper to recognize the pronounciation
2. Multiple users can use the bot
3. Multiple admins can see the _coins balance_ and add more if necesary

## Hardware requirements:

Up to 4G of RAM will be used.

    Tiny and base models use 1G of VRAM
    small model: 2G VRAM
    medium model: 5G VRAM
    large model: 10G VRAM

### Install dependencies

1. pip install git+https://github.com/openai/whisper.git
2. pip install difflib

## Setup

1. Create a telegram bot https://telegram.me/BotFather
2. Insert the telegram bot token in the line 147
3. Insert the admins *IDs* in the line 150
4. Select the whisper model size in the line 152
5. Add an user in the _data.json_ file

## About _data.json_

1. Send */user_id* command to the bot to get your ID, add it into _data.json_ or _admin_
2. *coins* refers to the accumulated reward, the calculation methos is included in the line 52
3. *current* refers to the actual job the user is in
4. *lang* (optional) is the assigned name to the text
5. *target_score* the score limit, on which more coins will not be added
6. *difficulty* refers how difficult will be to get a perfect score or easier to get lower, the calculation detail is in the line 143



https://user-images.githubusercontent.com/74340724/206840669-94e40f2f-2d33-42fe-918a-c504a9161550.mp4


