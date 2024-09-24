import os
import threading
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

def recognize_from_microphone(api_key, region, label=None, window=None):
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=api_key, region=region)
    speech_translation_config.speech_recognition_language = "en-US"

    to_language = "es"
    speech_translation_config.add_target_language(to_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    if label:
        label.config(text="Speak into your microphone.")
    else:
        print("Speak into your microphone.")

    def recognize():
        while True:
            translation_recognition_result = translation_recognizer.recognize_once_async().get()
            if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
                result_text = "Recognized: {}\nTranslated: {}".format(
                    translation_recognition_result.text,
                    translation_recognition_result.translations[to_language])
                if "stop session" in translation_recognition_result.text.lower():
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
            elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                result_text = "No speech could be recognized."
                if label:
                    label.config(text=result_text)
                else:
                    print(result_text)
            elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = translation_recognition_result.cancellation_details
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
    recognize_from_microphone(api_key, region)