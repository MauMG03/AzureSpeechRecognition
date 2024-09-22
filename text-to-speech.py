import os
import io
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def text_to_speech(api_key,region):  
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)    
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speechsynthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)

    text = input("Enter the text to be spoken: ")

    speech_synthesis_result = speechsynthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

load_dotenv()

api_key = os.getenv('api_key')
region = os.getenv('region')

text_to_speech(api_key,region)