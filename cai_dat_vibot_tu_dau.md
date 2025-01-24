### CÀI ĐẶT VIBOT TỪ ĐẦU TIÊN

### STEP1. Kết nối Console

1.1. Chờ Pi boot up xong, xác định IP của Pi từ Modem, Access Point hoặc các phần mềm quét IP có hiển thị hostname

1.2. Sử dụng các phần mêm SSH như putty/Securec CRT truy cập ssh vào địa chỉ IP của Pi

```sh
username: ...
password: ...
```

### STEP2. Cài đặt môi trường

2.1. Nâng cấp gói
Trên console của Pi, sử dụng lần lượt các lệnh sau

```sh
sudo apt-get update -y
```
Sau khi chạy xong, chạy tiếp
```sh
sudo apt-get upgrade -y
```
2.2. Cài gói cơ bản
```sh
sudo apt-get install nano git -y
```
2.3. Cài đặt Swap 2G

```sh
sudo dphys-swapfile swapoff
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
```
Cửa sổ nano mở ra
Tại dòng 
```sh
CONF_SWAPSIZE=1000
```
tăng giá trị 500 thành 2000, sau đó bấm Ctrl + Alt + X để save lại

2.4. Cài đặt Soundcard cho Mic2Hat, mạch AIO (Nếu sử dụng)
```sh
git clone https://github.com/waveshareteam/WM8960-Audio-HAT.git
```
Sau khi git xong
```sh
cd WM8960-Audio-HAT
sudo ./install.sh 
```
Sau khi cài xong
```sh
sudo reboot
```
2.5. Mở SPI cho led ws_2812 (Nếu sử dụng)
```sh
sudo raspi-config
```
Tìm đến mục Interface và kích hoạt mở SPI

### STEP3. Cài đặt các gói liên quan
3.1. Cài các gói phục vụ cho Python

```sh
sudo apt-get install libopenblas-dev vlc -y
```
và
```sh
sudo apt-get install python3 python3-pip python3-venv python3-dev python3-rpi.gpio python3-pyaudio
```
và
```sh
sudo apt-get install ffmpeg flac portaudio19-dev
```

3.2. Tạo env
```sh
python3 -m venv vibot_env
```
3.3. Chạy Env
```sh
source vibot_env/bin/activate
```
Nếu ra dấu nhắc lệnh như sau:
```sh
(vibot_env) pi@vibot64:~ 
```
là thành công

3.4. Cài đặt gói Python
Trong môi trường evn, gõ
```sh
pip install -U google-generativeai
```
```sh
pip install pvporcupine PyAudio RPi.GPIO SpeechRecognition edge_tts yt_dlp spidev beautifulsoup4 requests
```

Nếu dùng phím bấm cần cài đặt, nếu không dùng bỏ qua
```sh
sudo apt-get install python3-rpi.gpio 
pip install pigpio RPi.GPIO lgpio gpiozero
```


### STEP4. Cài đặt & Chạy vibot

4.1. Download code vietbot từ github
```sh
git clone --depth 1 https://github.com/vdlaptrinh/Personal-AI-Assistant.git
```
Chờ cho đến khi kết thúc

4.2. Config vietbot
Mở file config.json trong src thay key của bạn
```sh
porcupine_access_key = "YOUR API KEY"
gemini_key = "YOUR API KEY"
#Địa chỉ IP của Pi cài home assistant
HASS_IP = "http://192.168.10.25:8123"
LONG_TOKEN = "YOUR API KEY"
```

4.3. Chạy vibot
activate vibot_env nếu rồi bỏ qua 2 lệnh đầu
```sh
cd /home/pi
source vibot_env/bin/activate
cd /home/pi/Personal-AI-Assistant/
python3 main.py
```

4.4. Các lệnh tạm dừng, vô hiệu, xem trạng thái...
```sh
sudo systemctl daemon-reload
sudo systemctl enable ai_assistant.service
sudo systemctl start ai_assistant.service
sudo systemctl stop ai_assistant.service
sudo systemctl status ai_assistant.service
journalctl -u ai_assistant.service
sudo systemctl disable ai_assistant.service
```
```sh
sudo nano /etc/systemd/system/ai_assistant.service
```
Nội dung ai_assistant.service
```sh
[Unit]
Description=VIBOT
After=network.target

[Service]
ExecStart=/home/pi/vibot_env/bin/python3 /home/pi/Personal-AI-Assistant/main.py
WorkingDirectory=/home/pi/Personal-AI-Assistant/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```