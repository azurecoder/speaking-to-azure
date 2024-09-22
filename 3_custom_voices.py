import azure.cognitiveservices.speech as speechsdk
import yaml
import argparse

def speak_to_azure(speech_key, speech_region, endpoint):    
    config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    config.endpoint_id = endpoint
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=config)
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
    endpoint = config['azure']['custom_endpoint_id']
    print(f"Region: {region}")
    print(f"Speech Key: ****")
    print(f"Endpoint ID: ****")
    speak_to_azure(speech_key, region, endpoint)
    print("Done!")