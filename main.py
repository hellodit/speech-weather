from wave import openfp
import requests
from requests.exceptions import HTTPError
import speech_recognition

def get_weather_info(location):
    try:
        response = requests.get("http://api.weatherstack.com/current?access_key=20e25db211b545e23f0419d47236e321&query="+location)
        # If the response was successful, no Exception will be raised
        result =  response.json()
        if 'success' in result and result['success'] == False:
            raise TypeError("`Location not valid")
        return result 

    except HTTPError as http_err:
        return print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        return print(f'Other error occurred: {err}')  # Python 3.6


def speech_to_text_microphone(recognizer, microphone):
    if not isinstance(recognizer, speech_recognition.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, speech_recognition.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    print("Say something!")

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
    print("A moment of silence, please... \n")

    response = speech_to_text_microphone(recognizer, microphone)

    if response["success"] == True:
        print("You said: {} \n".format(response["transcription"]))
        
        print("Getting weather data, please wait... \n")
        weather = get_weather_info(response["transcription"])

        print(
            "Currently {}, region {}, country {}, \n"
            "Temperature {}f, feelslike {}c, Wind speed {} \n"
            "Weather condition {} \n"
            .format(
                weather["location"]["name"],weather["location"]["region"],weather["location"]["country"],
                weather["current"]["temperature"],weather["current"]["feelslike"],weather["current"]["wind_speed"],
                weather["current"]["weather_descriptions"][0]
            )
        )
    elif response["success"] == False:
        print(response["error"])
    else:
        print("Unknown error")     
