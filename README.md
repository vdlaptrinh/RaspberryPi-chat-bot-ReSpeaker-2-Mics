# Voice-chatbot-Pi-4-ReSpeaker-2-Mics hoặc pi zero 2w
Project Trợ lý ảo Tiếng Việt (giống như google home, alexa, maika...)
- Cần điền api key vào file config.py: picovoive, gemini, HASS IP, LONG TOKEN, my_city, openweather
- Từ khoá đánh thức: picovoice
- Hỏi sau khi nghe ding
- Chào bạn, Mấy giờ rồi
- Tăng âm lượng, giảm âm lượng
- Bật/Tắt đèn xxx, Bật/Tắt quạt xxx, Thực hiện + tên kịch bản
- Mở bài hát + tên bài hát, Mở nhạc + ...
- Thời tiết hôm nay/ Hôm nay có mưa không
- Các Câu hỏi khác sẽ được chuyển đến gemini
- Sau khi phát câu trả lời sẽ nghe dong
- Chế độ hội thoại được bật: cứ hỏi liên tục không cần đánh thức tới khi bạn nói "Chào bạn" hoặc 2 lần loa không nghe gì
- Led có 3 hiệu ứng: wakeup, think, speak
- Wakeup: Picovoice
- STT: GG CLOUD V1 hoặc V2 hoặc GG FREE
- TTS: EDGE-TTS

#Phần cứng sử dụng: Raspberry pi4 hoặc pi zero 2w, ReSpeaker-2-Mics, Loa (AUX)
- Chương trình test, thời gian sử dụng thực tế chưa nhiều. Các bạn dùng có thấy lỗi gì vui lòng cho tôi biết. Thanks
- pi 4 thì dùng led apa102, pi zero 2w thì dùng led2812
```sh
from pixels import Pixels
from led_ws2812 import Led

pixels = Pixels()
led = Led()

pixels.speak()
led.set_state('SPEAK')

pixels.wakeup()
led.set_state('WAKEUP')

led.set_state('THINK')
pixels.think()

pixels.off()
led.set_state('OFF')
```

#Button Raspberry pi4
- Chương trình có 1 nút nhấn: stop
- tương ứng GPIO 17 (button_wakeup = Button(17))
- Trong lúc loa đang phát tiếng, có thể bấm nút stop để ngừng
#Button Raspberry pi zero 2W (loa xiaodu) 
- Chương trình có 4 nút nhấn: + - wakeup stop
- tương ứng GPIO 5 25 26 6
- + - tăng giảm âm lượng
- wakeup: đánh thức bot, ra lệnh cho loa sau khi nghe ding
- Trong lúc loa đang phát tiếng, có thể bấm nút stop để ngừng

git clone https://github.com/vdlaptrinh/RaspberryPi-chat-bot-ReSpeaker-2-Mics.git

#Hướng dẫn:
https://github.com/vdlaptrinh/RaspberryPi-chat-bot-ReSpeaker-2-Mics/blob/main/01_cai_dat_vibot_tu_dau.md

#Video:
https://www.youtube.com/shorts/eudpXOqnEOw
https://www.youtube.com/shorts/YsV573PEA30


#pip list
(vibot_env) pi@pi4250123:~ $ pip list
Package                      Version
---------------------------- ----------
aiohappyeyeballs             2.4.4
aiohttp                      3.11.11
aiosignal                    1.3.2
annotated-types              0.7.0
attrs                        24.3.0
beautifulsoup4               4.12.3
cachetools                   5.5.1
certifi                      2024.12.14
charset-normalizer           3.4.1
colorzero                    2.0
edge-tts                     7.0.0
frozenlist                   1.5.0
google-ai-generativelanguage 0.6.15
google-api-core              2.24.0
google-api-python-client     2.159.0
google-auth                  2.38.0
google-auth-httplib2         0.2.0
google-generativeai          0.8.4
googleapis-common-protos     1.66.0
gpiozero                     2.0.1
grpcio                       1.69.0
grpcio-status                1.69.0
httplib2                     0.22.0
idna                         3.10
lgpio                        0.2.2.0
multidict                    6.1.0
pigpio                       1.78
pip                          23.0.1
propcache                    0.2.1
proto-plus                   1.25.0
protobuf                     5.29.3
pvporcupine                  3.0.4
pyasn1                       0.6.1
pyasn1_modules               0.4.1
PyAudio                      0.2.14
pydantic                     2.10.5
pydantic_core                2.27.2
pyparsing                    3.2.1
requests                     2.32.3
RPi.GPIO                     0.7.1
rsa                          4.9
setuptools                   66.1.1
soupsieve                    2.6
SpeechRecognition            3.14.0
spidev                       3.6
srt                          3.5.3
tabulate                     0.9.0
tqdm                         4.67.1
typing_extensions            4.12.2
uritemplate                  4.1.1
urllib3                      2.3.0
yarl                         1.18.3
yt-dlp                       2025.1.15




