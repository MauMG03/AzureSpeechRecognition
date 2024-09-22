import os
import io
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def speech_to_microphone(api_key,region):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = "es-ES"
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)

    
    
    # set timeout 
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "60000")
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "20000")

    print("Speak into your microphone. Say \"Stop session\" to end.")

    while True:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
            if "stop session" in speech_recognition_result.text.lower():
                print("Session ended by user.")
                break
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}", format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Verify api_key and region are correct.")



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

#speech_to_microphone(api_key,region)
text_to_speech(api_key,region)
