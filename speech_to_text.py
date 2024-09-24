import os
import threading
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def speech_to_microphone(api_key, region, label=None, window=None):
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language = "es-ES"
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "60000")
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "20000")

    if label:
        label.config(text="Speak into your microphone. Say \"Stop session\" to end.")
    else:
        print("Speak into your microphone. Say \"Stop session\" to end.")

    def recognize():
        while True:
            speech_recognition_result = speech_recognizer.recognize_once_async().get()
            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                result_text = "Recognized: {}".format(speech_recognition_result.text)
                if "stop session" in speech_recognition_result.text.lower():
                    result_text += "\nSession ended by user."
                    if label:
                        label.config(text=result_text)
                    else:
                        print(result_text)
                    if window:
                        window.destroy()
                    break
                if label:
                    label.config(text=result_text)
                else:
                    print(result_text)
            elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                result_text = "No speech could be recognized."
                if label:
                    label.config(text=result_text)
                else:
                    print(result_text)
            elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_recognition_result.cancellation_details
                result_text = "Speech Recognition canceled: {}".format(cancellation_details.reason)
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    result_text += "\nError details: {}".format(cancellation_details.error_details)
                    result_text += "\nVerify api_key and region are correct."
                if label:
                    label.config(text=result_text)
                else:
                    print(result_text)
                break

    # Run the recognition in a separate thread
    recognition_thread = threading.Thread(target=recognize)
    recognition_thread.start()

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('api_key')
    region = os.getenv('region')
    speech_to_microphone(api_key, region)