import speech_recognition as sr


def speech_to_text(audio_file, language="en-IN"):
    """
    Convert recorded audio into text.

    Parameters:
        audio_file: Streamlit audio input file
        language: Speech recognition language

    Returns:
        Recognized text
    """

    recognizer = sr.Recognizer()

    try:
        # Move to beginning of uploaded audio
        audio_file.seek(0)

        # SpeechRecognition can read the WAV audio
        # recorded by Streamlit
        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(
            audio_data,
            language=language
        )

        return text

    except sr.UnknownValueError:

        return ""

    except sr.RequestError as e:

        raise RuntimeError(
            f"Speech recognition service error: {e}"
        )

    except Exception as e:

        raise RuntimeError(
            f"Could not process audio: {e}"
        )