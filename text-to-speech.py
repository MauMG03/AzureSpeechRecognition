import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def text_to_speech(api_key, region, text):  
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)    
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('api_key')
    region = os.getenv('region')
    text = input("Enter the text to be spoken: ")
    text_to_speech(api_key, region, text)