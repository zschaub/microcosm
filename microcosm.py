from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from googletrans import Translator

app = Flask(__name__)

# First element is language name, second is Google Translate language code, third is twilio Alice language code
languages = [["Danish", 'da', 'da-DK'], ["German", 'de', 'de-DE'], ["English", 'en', 'en-US'],
             ["Catalan", 'ca', 'ca-ES'], ["Spanish", 'es', 'es-ES'], ["Finish", 'fi', 'fi-FI'],
             ["French", 'fr', 'fr-FR'], ["Italian", 'it', 'it-IT'], ["Japanese", 'ja', 'ja-JP'],
             ["Korean", 'ko', 'ko-KR'], ["Norwegian", 'nb', 'nb-NO'], ["Dutch", 'nl', 'nl-NL'],
             ["Polish", 'pl', 'pl-PL'], ["Portuguese", 'pt', 'pt-PT'], ["Russian", 'ru', 'ru-RU'],
             ["Swedish", 'sv', 'sv-SE'], ["Chinese Mandarin", 'zh-CN', 'zh-CN']]

source = 2
destination = 2


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='/gather')
    gather.say(
        'For Spanish press 1, for Italian press 2, for German press 3, for French press 4, for Mandarin Chinese '
        'press 5, for Japanese press 6, to manually enter a language press 9', voice='Alice', language=languages[source][2])
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    resp = VoiceResponse()
    global destination
    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        gather = Gather(input='speech', action='/translate')
        # <Say> a different message depending on the caller's choice
        if choice == '1':
            destination = 4
            gather.say('You have picked Spanish, speak your message now', voice='Alice', language=languages[source][2])
            resp.append(gather)
        elif choice == '2':
            destination = 7
            gather.say('You have picked Italian, speak your message now', voice='Alice', language=languages[source][2])
            resp.append(gather)
        elif choice == '3':
            destination = 1
            gather.say('You have picked German, speak your message now', voice='Alice', language=languages[source][2])
            resp.append(gather)
        elif choice == '4':
            destination = 6
            gather.say('You have picked French, speak your message now', voice='Alice', language=languages[source][2])
            resp.append(gather)
        elif choice == '5':
            destination = 16
            gather.say('You have picked Mandarin Chinese, speak your message now', voice='Alice',
                       language=languages[source][2])
            resp.append(gather)
        elif choice == '6':
            destination = 8
            gather.say('You have picked Japanese, speak your message now', voice='Alice', language=languages[source][2])
            resp.append(gather)
        elif choice == '9':
            gather = Gather(input='speech', action='/language')
            gather.say('Please say what language you want to use', voice='Alice', language=languages[source][2])
            resp.append(gather)
        else:
            resp.say("Sorry, I don't understand that choice.", voice='Alice', language=languages[source][2])

    return str(resp)


@app.route("/language", methods=['GET', 'POST'])
def manual_language():
    resp = VoiceResponse()
    # print(request.values)
    user_speech = request.form['SpeechResult']
    for i in range(len(languages)):
        if languages[i][0] == user_speech:
            gather = Gather(input='speech', action='/translate')
            gather.say('You have picked ' + languages[i][0] + ' speak your message now', voice='Alice', language=languages[source][2])
            global destination
            destination = i
            resp.append(gather)
            return str(resp)
    resp.say(user_speech + ' is not a language I can help you with, please try again', voice='Alice', language=languages[source][2])
    return str(resp)


@app.route("/translate", methods=['GET', 'POST'])
def translate():
    translator = Translator()
    resp = VoiceResponse()
    # print(request.values)
    user_speech = request.form['SpeechResult']
    x = translator.translate(user_speech, src=languages[source][1], dest=languages[destination][1])
    translated_text = x.text
    resp.say(translated_text, voice='Alice', language=languages[destination][2])
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
