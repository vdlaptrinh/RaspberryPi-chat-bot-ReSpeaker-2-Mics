import pyaudio
import speech_recognition as sr

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("Danh sách các thiết bị âm thanh khả dụng:\n")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"ID: {i}, Tên: {device_info['name']}, Loại: {device_info['maxInputChannels']} kênh đầu vào")
    p.terminate()
    
    # Use the microphone as source for input (specify the microphone index)
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

list_audio_devices()
