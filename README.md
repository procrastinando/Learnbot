# Study-languages-using-telegram-and-whisper

### 1. Advantages and Technologies

Learnbot is an innovative language learning tool that combines the power of several cutting-edge technologies to help users learn new languages efficiently. Some of the advantages and features of Learnbot include:

* Whisper: Learnbot uses the Whisper library, which is an open-source tool that uses deep learning models to transcribe spoken words into text. This feature allows users to improve their pronunciation skills by practicing speaking the language and receiving immediate feedback on their pronunciation accuracy.
* Azure Cognitive Services: Learnbot also utilizes Azure Cognitive Services to transcribe audio to text in the cloud, which allows for more accurate transcriptions and eliminates the need for local resources. This feature also enables Learnbot to offer additional language learning features, such as text-to-speech and translation.
* Telegram Bot: Learnbot is a Telegram bot, which means that users can access it from any device that has the Telegram app installed. This feature makes it easy for users to learn on-the-go and from anywhere, as long as they have an internet connection.
* Multiple Users: Learnbot is designed to be used by multiple users, making it ideal for group language learning sessions or classroom settings.
Easy Setup: Learnbot can be set up quickly and easily, with just a few simple steps, making it accessible to users of all skill levels.

With these features, Learnbot provides an effective and convenient way for users to learn new languages and improve their pronunciation skills.

### 2. Creating an Azure Cognitive Services Account, Creating a Telegram Bot, Installing Dependencies, and Hardware Requirements

Before you can use Learnbot, you will need to create an Azure Cognitive Services account, create a Telegram bot, install the necessary dependencies, and ensure that your computer meets the hardware requirements.

#### Creating an Azure Cognitive Services Account:

* Go to the Azure Cognitive Services website (https://azure.microsoft.com/en-us/services/cognitive-services/) and click on "Get started for free."
* Sign in with your Microsoft account or create a new one.
* Choose the Azure Cognitive Services you want to use, in this case, Speech Services.
* Create a new Speech Services resource by following the on-screen instructions.
Once the resource is created, copy the Speech Services subscription key and region for use in the Learnbot config.json file.

#### Creating a Telegram Bot:

* Open the Telegram app and search for the "BotFather" user.
* Send a message to the BotFather user and type "/newbot" to create a new bot.
* Follow the on-screen instructions to choose a name and username for your bot.
Once the bot is created, copy the bot token for use in the Learnbot config.json file.

#### Installing Dependencies:

* Clone the repository
* Open a terminal or command prompt and run the following command: ```sudo apt-get update && sudo apt-get install -y libleptonica-dev tesseract-ocr tesseract-ocr-eng libtesseract-dev ffmpeg```
* Next, install the Whisper library by running the following command: ```pip install git+https://github.com/openai/whisper.git```
* Finally, install the remaining dependencies by running the following command from the Learnbot directory: ```pip install -r learnbot/requirements.txt```
>> For ubuntu 22 only: ```wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb && sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb```

#### Hardware Requirements:

To use Learnbot with Azure Cognitive Services, you will need an Azure subscription. In terms of hardware requirements, the amount of RAM and VRAM required depends on the size of the Whisper model you choose to use:

* Tiny and base models use 1G of VRAM
* Small model: 2G VRAM
* Medium model: 5G VRAM
* Large model: 10G VRAM

It is recommended to have at least 4GB of RAM to use Learnbot with any of the Whisper models.

With these steps completed, you are ready to move on to setting up the Learnbot ```config.json``` file and running the Learnbot scripts.

### 3. Configuring and Running the Learnbot

Configure the config.json file in the learnbot directory with the following information:

* token: The API token of your Telegram bot.
* admin: A list of Telegram user IDs who will have admin access to the bot. Separate each ID with a comma.
* speech_key: The subscription key of your Azure Cognitive Services account.
* service_region: The region where your Azure Cognitive Services account is located.
* allowed_voices: A list of voices that are allowed for speech synthesis. The voices should be in the format <language>-<country>. Separate each voice with a comma.
* model: The size of the Whisper model to use for speech recognition. Available options are tiny, base, small, medium, and large.
* ex_rate: The exchange rate of successful letters for rewards. For example, if the exchange rate is 10000, the user will receive 0.0001 dollars for each successfully pronounced letter.

To use the learnbot_whisper.py script for speech recognition using Whisper, run the following command in the root directory of the cloned repository:
```
python learnbot_whisper.py
```
To use the learnbot_azure.py script for speech recognition using Azure Cognitive Services, run the following command in the root directory of the cloned repository:
```
python learnbot_azure.py
```
To add more jobs to the data.json file using OCR, place the images in the images directory and run the following command in the learnbot directory of the cloned repository:
```
python add_jobs.py
```
Interact with the bot on Telegram by adding it to a group chat or sending it direct messages. The bot will provide instructions on how to use it for language learning.

https://user-images.githubusercontent.com/74340724/206840669-94e40f2f-2d33-42fe-918a-c504a9161550.mp4
