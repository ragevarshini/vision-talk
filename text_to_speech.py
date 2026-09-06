import pyttsx3
import tempfile
import os


def text_to_speech(text):
    """
    Convert text into speech and return
    the generated audio file path.
    """

    if not text:
        return None

    # Create TTS engine
    engine = pyttsx3.init()

    # Voice settings
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    audio_path = temp_file.name

    temp_file.close()

    # Generate speech
    engine.save_to_file(
        text,
        audio_path
    )

    engine.runAndWait()

    engine.stop()

    # Check whether file was created
    if not os.path.exists(audio_path):
        raise RuntimeError(
            "Could not create speech audio file."
        )

    return audio_path