import pvporcupine
import pyaudio
import struct
import webrtcvad
import wave
import numpy as np
import math
import os 
import logging


from communication_mediator import CommunicationMediator
from agent import Agent
from message import Message
from faster_whisper import WhisperModel, BatchedInferencePipeline
from agent_labels import label

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@label("agent", "s2t")
class SpeechToTextAgent(Agent):
    def __init__(self, comm_mediator: CommunicationMediator):
        self.comm_mediator = comm_mediator  
        self.id = self.__class__._labels[1]  

    def get_id(self):
        return self.id
    
    def log(self, level: str, message: str):
        level = level.lower()  
        getattr(logging, level)(message)  

    def record_audio(self, audio_stream, vad):
        frames = []
        active = True
        silence_count = 0
        
        self.log("INFO", "Audio capture starting...")
        sampling_freq = 16000
        chunks_read = 480
        silence_threshold = math.ceil((3 * sampling_freq) / chunks_read)

        while True:
            pcm = audio_stream.read(chunks_read)
        
            # da correggere 
            if vad.is_speech(pcm, sampling_freq):
                frames.append(pcm)
                active = True
                silence_count = 0 
                self.log("INFO", "Audio detected...")
            elif active:  
                silence_count += 1
                frames.append(pcm)
                self.log("INFO", "Silence detected, monitoring...")
                if silence_count >= silence_threshold:
                    self.log("INFO", "Extended silenced detected, stopping recording...")
                    break

        audio_stream.close()

        audio_file = "recorded_audio.wav"
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sampling_freq) 
            wf.writeframes(b''.join(frames))

        return audio_file


    def run(self):
        model = WhisperModel("turbo", device="cpu", compute_type="int8")
        batched_model = BatchedInferencePipeline(model=model)

        # insert here your access key
        access_key = ""
        handle = pvporcupine.create(
            access_key=access_key,
            model_path="porcupine_params_it.pv",
            keyword_paths=['Svegliati_it_mac_v3_0_0.ppn']
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=handle.frame_length
        )

        vad = webrtcvad.Vad(1) 

        try:
            while True:
                pcm = struct.unpack_from("h" * handle.frame_length, audio_stream.read(handle.frame_length))
                keyword_index = handle.process(pcm)

                if keyword_index >= 0:
                    self.log("INFO", "Wake word detected!")

                    audio_file = self.record_audio(audio_stream, vad)

                    segments, _ = batched_model.transcribe(audio_file)
                    transcription = " ".join(segment.text for segment in segments)
                    self.log("INFO", "Transcription: " % transcription)
                    os.remove("recorded_audio.wav")

                    sender = self.id
                    receiver = "mensab"
                    body = transcription

                    message = Message(sender, receiver, body)
                    self.comm_mediator.handle_request(message)
                    self.log("INFO", "S2T agent sent a message..")

                    receiver = self.id
                    response = self.comm_mediator.get_response(receiver)[0]

                    self.log("INFO", "S2t received a response: " % response)

                    if "sleep" in response["body"].lower():
                        break

                    audio_stream = pa.open(
                        rate=handle.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=handle.frame_length
                    )

            self.log("INFO", "Shutting down s2t agent..")

        finally:
            audio_stream.close()
            pa.terminate()
            handle.delete()



