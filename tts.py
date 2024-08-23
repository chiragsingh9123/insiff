import azure.cognitiveservices.speech as speechsdk
import wave
from upload2 import *
import os

import numpy as np
from scipy.io import wavfile

def resample_wav(input_wav_file, output_wav_file, target_rate=8000):
    # Read the input WAV file
    with wave.open(input_wav_file, 'rb') as wf:
        params = wf.getparams()
        frames = wf.readframes(params.nframes)
    
    # Convert frames to numpy array
    audio_data = np.frombuffer(frames, dtype=np.int16)

    # Get the original sample rate
    original_rate = params.framerate

    # Resample the audio data
    resampled_data = np.interp(
        np.linspace(0, len(audio_data), int(len(audio_data) * target_rate / original_rate)),
        np.arange(len(audio_data)),
        audio_data
    ).astype(np.int16)

    # Write the resampled data to the output WAV file
    with wave.open(output_wav_file, 'wb') as wf:
        wf.setnchannels(params.nchannels)
        wf.setsampwidth(params.sampwidth)
        wf.setframerate(target_rate)
        wf.writeframes(resampled_data.tobytes())

    print(f"Audio resampled to {target_rate} Hz and saved as {output_wav_file}.")




def text_to_speech(text, output_wav_file, voice_name,script_id):
    subscription_key = "a86b6602cbf9436fb9f3a1595e3a39a8"
    region = "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice_name  # Set the voice name
    audio_config = speechsdk.audio.AudioOutputConfig(filename=f"tempscripts/{script_id}/temp.wav")

    # Create a speech synthesizer with the given settings
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    # Check if the speech synthesis succeeded
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized and saved to temporary file successfully.")

        # Read the temporary file and resample it to 8000 Hz
        resample_wav(f"tempscripts/{script_id}/temp.wav",output_wav_file)


   

def Convert_TTS(text1,text2,text3,text4,text5,script_id:int,voice):
    directory_path = f"scripts/{script_id}"
    check_path = f"../../var/www/atlanta-api.online/scripts/{script_id}"
    if not os.path.exists(check_path):
        os.makedirs(directory_path)
        os.makedirs("temp"+directory_path)
        print(f"Directory '{directory_path}' created.")
        
        text_to_speech(
        f"{text1}",
        f"scripts/{script_id}/output1.wav",
        voice_name=f"{voice}",
        script_id=script_id
    )
        text_to_speech(
        f"{text2}",
        f"scripts/{script_id}/output2.wav",
        voice_name=f"{voice}",
        script_id=script_id
    )
        text_to_speech(
        f"{text3}",
        f"scripts/{script_id}/output3.wav",
        voice_name=f"{voice}",
        script_id=script_id
    )
        text_to_speech(
        f"{text4}",
        f"scripts/{script_id}/output4.wav",
        voice_name=f"{voice}",
        script_id=script_id
    )
        text_to_speech(
        f"{text5}",
        f"scripts/{script_id}/output5.wav",
        voice_name=f"{voice}",
        script_id=script_id
    )
        os.remove("temp"+directory_path+"/temp.wav")
        os.removedirs("temp"+directory_path)
        
        create_folder_and_upload(f"scripts/{script_id}")

    else:
        
        print(f"Directory '{check_path}' already exists.")
