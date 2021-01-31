# SheepBotFrame

Simple Program to run custom AI Bots on Discord

## How to install

`
git clone https://github.com/TheBlackfurGuy/SheepBotFrame.git
cd SheepBotFrame
pip install -r requirements.txt
`
## How to set up
Edit the config.yml file to your likings. <br>
Change "botname" to the name of the bot (currently has no effect) <br>
Change "filterpings" to false if you don't want to have pings filtered out. <br>
Change "excludeprefix" to set the text sequence that will hide a message from the bot <br>
Change "usechannels" to the IDs of the channels the bot should react in <br>
Change "trainchannels" to the channel IDs and ammounts the bot should download <br>
Change "corpus" to all the corpus the bot should train <br>
Change "token" to the Bots token

## How to run

This will give you all information you need to get started. 

`
python3 run.py --help
`
