import azure.cognitiveservices.speech as speechsdk
import yaml
import argparse
import time
import os
from scipy.io import wavfile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

SAMPLE_RATE = 16000
BITS_PER_SAMPLE = 16
CHANNELS = 1

def extract_audio_from_mp4(mp4_filename, output_wav_filename):
    video = VideoFileClip(mp4_filename)
    audio_mp3_filename = "./output/temp_audio.mp3"
    video.audio.write_audiofile(audio_mp3_filename, codec="mp3")
    audio = AudioSegment.from_mp3(audio_mp3_filename)
    audio = audio.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS).set_sample_width(BITS_PER_SAMPLE // 8)
    audio.export("./output/{}".format(output_wav_filename), format="wav")
    os.remove(audio_mp3_filename)
    print(f"Audio extracted and saved as {output_wav_filename}")
    return "./output/{}".format(output_wav_filename)

def conversation_transcriber_recognition_canceled_cb(self, evt: speechsdk.SessionEventArgs): print('Canceled event')
def conversation_transcriber_session_stopped_cb(self, evt: speechsdk.SessionEventArgs): print('SessionStopped event')
def conversation_transcriber_session_started_cb(self, evt: speechsdk.SessionEventArgs): print('SessionStarted event')
def conversation_transcriber_transcribed_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        line = '{}: {}'.format(evt.result.speaker_id, evt.result.text)    
        print(line)
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))

def recognize_from_file(wav_file, key, region):
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "./output/speech_sdk.log")
    speech_config.speech_recognition_language = "en-GB"
    wave_format = speechsdk.audio.AudioStreamFormat(SAMPLE_RATE, BITS_PER_SAMPLE, CHANNELS)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config=speech_config, audio_config=audio_config
    )
    transcribing_stop = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        print('CLOSING on {}'.format(evt))
        nonlocal transcribing_stop
        transcribing_stop = True
    def transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        line = '{}: {}'.format(evt.result.speaker_id, evt.result.text)    
        print('TRANSCRIBED: {}'.format(line))

    conversation_transcriber.transcribed.connect(transcribed_cb)
    conversation_transcriber.session_started.connect(lambda evt: print("SESSION STARTED: {}".format(evt)))
    conversation_transcriber.session_stopped.connect(lambda evt: print("SESSION STOPPED: {}".format(evt)))
    conversation_transcriber.canceled.connect(lambda evt: print("CANCELED: {}".format(evt)))
    conversation_transcriber.session_stopped.connect(stop_cb)
    conversation_transcriber.canceled.connect(stop_cb)
    conversation_transcriber.start_transcribing_async()
    _, wav_data = wavfile.read(wav_file)
    stream.write(wav_data.tobytes())
    stream.close()
    while not transcribing_stop:
        time.sleep(.5)
    conversation_transcriber.stop_transcribing_async()
    os.remove(wav_file)

def load_yaml(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Load region and speech_key from a YAML file.")
    parser.add_argument('config_file', type=str, help="The path to the YAML configuration file.")
    parser.add_argument('--filename', type=str, required=True, help="the filename used for the transcription")
    args = parser.parse_args()

    config = load_yaml(args.config_file)
    region = config['azure']['region']
    speech_key = config['azure']['speech_key']
    print(f"Region: {region}")
    print(f"Speech Key: ****")

    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    full_file_path = os.path.join(output_directory, args.filename)
    file_extension = os.path.splitext(args.filename)[1].lower()
    if file_extension != '.mp4':
        raise ValueError("Only mp4 files are supported")

    wav_file = extract_audio_from_mp4(full_file_path, "temp.wav")
    recognize_from_file(wav_file, speech_key, region)
    print("Done!")

if __name__ == '__main__':
    main()
# python3 5_decomposing_video.py richard.yaml --filename "Richard as Peter Jones.mp4"