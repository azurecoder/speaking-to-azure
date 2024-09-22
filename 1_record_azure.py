import pyaudio
import wave
import lameenc
from enum import Enum
import argparse
import os

class AudioFormat(Enum):
    WAV = 'wav'
    MP3 = 'mp3'

def record_audio(filename, audio_format=AudioFormat.MP3, duration=30, sample_rate=16000, chunk_size=1024, audio_format_size=pyaudio.paInt16, channels=1, quality=2):
    p = pyaudio.PyAudio()  
    stream = p.open(format=audio_format_size, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    print(f"Recording for {duration} seconds...")

    frames = []
    for _ in range(int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    if audio_format == AudioFormat.MP3:
        encoder = lameenc.Encoder()
        encoder.set_bit_rate(128)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(channels)
        encoder.set_quality(quality)
        mp3_data = b''.join([encoder.encode(pcm) for pcm in frames])
        mp3_data += encoder.flush()
        with open(filename, 'wb') as mp3_file:
            mp3_file.write(mp3_data)
        print(f"File saved as {filename}")
    elif audio_format == AudioFormat.WAV:
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(p.get_sample_size(audio_format_size))
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(frames))
        print(f"File saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Record audio and save as WAV or MP3.")
    parser.add_argument('filename', type=str, help="The name of the file to save the recording.")
    parser.add_argument('--duration', type=int, default=30, help="Duration of the recording in seconds (default: 30).")
    args = parser.parse_args()
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    full_file_path = os.path.join(output_directory, args.filename)
    file_extension = os.path.splitext(args.filename)[1].lower()
    if file_extension == '.wav':
        audio_format = AudioFormat.WAV
    elif file_extension == '.mp3':
        audio_format = AudioFormat.MP3
    else:
        raise ValueError("Invalid file extension. Please use either .wav or .mp3.")
    record_audio(full_file_path, duration=args.duration, audio_format=audio_format)

if __name__ == '__main__':
    main()

# python3 1_record_azure.py richard.wav --duration 40