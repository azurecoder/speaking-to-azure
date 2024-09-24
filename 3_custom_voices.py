import azure.cognitiveservices.speech as speechsdk
import yaml
import argparse

def speak_to_azure(speech_key, speech_region, speech_voice, custom_endpoint):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = speech_voice
    speech_config.endpoint_id = custom_endpoint
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    print("Type some text that you want to speak...")
    text = input()
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Is your speech services info correct?")

def load_yaml(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Load region and speech_key from a YAML file.")
    parser.add_argument('config_file', type=str, help="The path to the YAML configuration file.")
    args = parser.parse_args()

    config = load_yaml(args.config_file)
    region = config['azure']['region']
    speech_key = config['azure']['speech_key']
    custom_endpoint = config['azure']['custom_endpoint_id']
    print(f"Region: {region}")
    print(f"Speech Key: ****")

    speak_to_azure(speech_key, region, "Richard VoiceNeural", custom_endpoint)
    print("Done!")

if __name__ == '__main__':
    main()
# python3 3_custom_voices.py richard.yaml

"""
This is the story of the book "The Hitchhiker's Guide to the Galaxy"—perhaps the most remarkable, certainly the most successful book ever to come out of the great publishing corporations of Ursa Minor. More popular than The Celestial Home Care Omnibus, better-selling than Fifty-Three More Things to Do in Zero Gravity, and more controversial than Oolon Colluphid's trilogy of philosophical blockbusters, Where God Went Wrong, Some More of God's Greatest Mistakes, and Who is This God Person Anyway?
"""