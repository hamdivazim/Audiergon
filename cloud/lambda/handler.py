import os
import base64
import json
import wave
from audiergon import process_audio

def handler(event, context):
    """
    Audiergon Cloud - Lambda Handler

    Check out Audiergon :) https://github.com/hamdivazim/Audiergon
    """

    input_path = "/tmp/input.wav"
    output_path = "/tmp/output.wav"
    
    try:
        body = json.loads(event.get('body', '{}'))
        base64_audio = body.get('audio')
        gains = body.get('gains', {})
        
        if not base64_audio:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing audio data"})}
            
        if len(base64_audio) > 2097152: # <-- Currently this imposes a 1.5MB filesize limit. Remove or change as you wish!
            return {"statusCode": 413, "body": json.dumps({"error": "File payload too large. Max size is 1.5MB."})}

        audio_bytes = base64.b64decode(base64_audio)

        with open(input_path, "wb") as f:
            f.write(audio_bytes)
            
        with wave.open(input_path, 'rb') as wav_check:
            nchannels = wav_check.getnchannels()
            sampwidth = wav_check.getsampwidth()
            framerate = wav_check.getframerate()
            nframes = wav_check.getnframes()
            
            duration = nframes / float(framerate)
            
            if duration > 5.1: # <-- Change this if you want a larger audio length limit. You may also have to increase Lambda memory allocation (even with 5s it takes 27s with 512mb to process in my experience!)
                raise ValueError("Audio exceeds 5 second limit")
            if nchannels != 1 or sampwidth != 2:
                raise ValueError("Audio must be 16 bit Mono PCM WAV")
        
        process_audio(
            audio_filepath=input_path,
            bass_gain=float(gains.get('bass', 1.0)),
            low_mid_gain=float(gains.get('low_mid', 1.0)),
            mid_gain=float(gains.get('mid', 1.0)),
            high_mid_gain=float(gains.get('high_mid', 1.0)),
            treble_gain=float(gains.get('treble', 1.0)),
            output=output_path
        )
        
        with open(output_path, "rb") as f:
            processed_encoded = base64.b64encode(f.read()).decode('utf-8')
            
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"audio": processed_encoded})
        }
        
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Error: {str(e)}"})
        }
    
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)