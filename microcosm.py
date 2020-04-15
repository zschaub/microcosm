from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from googletrans import Translator

app = Flask(__name__)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""

    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='/gather')
    gather.say('For English to Spanish translation, press 1. For English to French translation, press 2. For English to Italian translation, press 3.')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            gather = Gather(input='speech', action='/spanish')
            gather.say('You have picked Spanish, speak your message now')
            resp.append(gather)
        elif choice == '2':
            gather = Gather(input='speech', action='/french')
            gather.say('You have picked french, speak your message now')
            resp.append(gather)
        elif choice == '3':
            gather = Gather(input='speech', action='/italian')
            gather.say('You have picked italian, speak your message now')
            resp.append(gather)
        else:
            resp.say("Sorry, I don't understand that choice.")

    return str(resp)


@app.route("/spanish", methods=['POST'])
def spanish():
    translator = Translator()
    resp = VoiceResponse()
    # print(request.values)
    userSpeech = request.form['SpeechResult']
    x = translator.translate(userSpeech, src='en', dest='es')
    translatedText = x.text
    resp.say(translatedText, language='es')
    return str(resp)


@app.route("/french", methods=['GET', 'POST'])
def french():
    translator = Translator()
    resp = VoiceResponse()
    # print(request.values)
    userSpeech = request.form['SpeechResult']
    x = translator.translate(userSpeech, src='en', dest='fr')
    translatedText = x.text
    resp.say(translatedText, language='fr')
    return str(resp)


@app.route("/italian", methods=['GET', 'POST'])
def italian():
    translator = Translator()
    resp = VoiceResponse()
    # print(request.values)
    userSpeech = request.form['SpeechResult']
    x = translator.translate(userSpeech, src='en', dest='it')
    translatedText = x.text
    resp.say(translatedText, language='it')
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
