import requests
from requests.exceptions import HTTPError
import speech_recognition

def get_weather_info(location):
    try:
        response = requests.get("http://api.weatherstack.com/current?access_key=####&query="+location)
        # If the response was successful, no Exception will be raised
        return response.json()
    except HTTPError as http_err:
        return print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        return print(f'Other error occurred: {err}')  # Python 3.6


def speech_to_text_microphone(recognizer, microphone):
    if not isinstance(recognizer, speech_recognition.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, speech_recognition.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    response = {
        "success": True,
        "error": None,
        "transcription": None,
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio,language="id-ID")
        
    except speech_recognition.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except speech_recognition.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response



if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    response = speech_to_text_microphone(recognizer, microphone)

    if response["success"] == True:
        weather = get_weather_info(response["transcription"])
        print("currently "+format(weather["location"]["name"]+" Region "+weather["location"]["region"]+"\n Weather condition " +weather["current"]["weather_descriptions"][0]))
    elif response["success"] == False:
        print(response["error"])
    else:
        print("Unknown error")     
