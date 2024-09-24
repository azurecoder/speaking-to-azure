# Summary

This is my talk on Speaking to Azure. As Azure grows in complexity and aligns to the age of the AI we are being gifted with a bunch of services which make quickstarting much easier. In this case understanding the speech SDK and what you can do with voice in your applications is key. This set of examples and slides show the breadth but not the depth of how you can leverage speech services in Azure. Feel free to use as needed and just add a citation.

# File descriptions

There are seven examples in this repository. Here is a short description of each and how to configure them.

- **1_record_azure.py** - this contains a method to record your voice using pyaudio. In order to install ensure that you use pip to install all of the dependencies. I'll be adding a requirements file to help in a future release. If you are using mac or linux use brew or apt-get to install portaudio first.
- **2_voice_of_azure.py** - this allows you to choose between three voices Sonia, Jorge and Aria from the Microsoft voice collection.
- **3_custom_voices.py** - this uses a custom neural voice that has been trained on your voice. at the time of writing the custom neural voice is in private preview so you will need to request access. You need at least 20 training samples through *speech studio* and this will give you the ability to use your voice as per sample 2 with a custom endpoint.
- **4_transcribing_voice.py** - this will allow you to transcribe a wav file and spit out the audio as text. It uses the batch speech to text api.
- **5_decomposing_video.py** - this takes parts of the first sample and allows you to record video and strip the audio channel from it so that you can use the *speech service SDK*.
- **6_video_indexing.py** - takes an example from the video indexing service to show how you can use the API to get insight and audio data from the service.
- **7_speech_enrolment.py** - [TBC] uses the speech enrolment API which allows you to enrol as a speaker using voice snippets and then verify or identify speakers in audio.

To configure use the following **config.yaml** file replacing the values below. 
```
azure:
  region: <add your speech region here>
  speech_key: <add your speech key here>
  custom_endpoint_id: <add your custom endpoint id here>
  video_key: <add your video key here>
  video_account_id: <add your video account id here>
```

In order to complete this it's important to ensure that you get the values from the right places.

- *region* - is the Azure region which is generally a lower case concatenation of the region, for example West Europe is **westeurope**
- *speech_key* - this is the key that comes from the Azure Speech Service. You can find this in the Azure Portal.
- *custom_endpoint_id* - this is the endpoint of the trained custom neural voice that you can find in the speech services portal after you've deployed your model. More details on this here https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice-lite
- *video_key* - the key for the videio indexer account can be found through the Azure Portal in the service blade.
- *video_account_id* - this is the id of the video account can also be found through the Video Indexer Portal.