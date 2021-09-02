# waitBot
A package integrated with ROS capable of taking an order at example a coffee shop via speech recognition and nlp processing


How to manual...
Depends on:
If on MELODIC: sudo apt install python3-pip python3-yaml
sudo apt install libportaudio2
sudo apt install espeak
pip3 install vosk
pip3 install sounddevice
sudo apt-get install libportaudio2
pip3 install word2number
pip3 install cdifflib
pip3 install python-Levenshtein
pip3 install fuzzywuzzy
pip3 install fuzzywuzzy[speedup]
pip3 install --user -U nltk
pip3 install pyttsx3
python3 -m nltk.downloader punkt
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader averaged_perceptron_tagger
---------------------------------------------------------------------------------------------
Structure:
Topics:
/waitbot/speech_recognizer  -> custom message you can publish manually with rostopic pub /waitbot/speech_recognizer waitbot/speech_recognizer (press tab to show the message)
/waitbot/tts/phrase -> string message, you can publish here so the tts will speak your command
/waitbot/tts/status -> the status of the TTS engine.. Is it speaking? yes? no? subscribe and find out :slightly_smiling_face:
nodes:
vosk_sr.py -> the speech recognition node publishes to topic /waitbot/speech_recognition and subscribes to /waitbot/tts/status (if status is true it won't work so it won't listen to itself)
nlp_parser.py -> parses the phrase published to the topic /waitbot/speech_recognizer and recognizes what the poet tries to say :slightly_smiling_face: after, it publishes it to /waitbot/tts/phrase so it should be spoken...
tts_engine.py -> name your desire and it shall be heard by all in the room.. publishes to /waitbot/tts/status
run the package by:  roslaunch waitbot waitbot.launch
