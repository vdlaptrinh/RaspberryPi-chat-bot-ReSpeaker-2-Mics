# 1. detect wake word,
# 2. prompt for question, 
# 3. pass query to OpenAi and 
# 4. speak response

import waitForWakeWord
from datetime import datetime
import threading
import subprocess, os, re
from config import gemini_key
from config import my_city
from speech_to_text import recognize_speech
#from stt_gg_cloud_v1 import stt_process
from text_to_speech import text_to_speech
#from pixels import Pixels
from led_ws2812 import Led
import google.generativeai as genai
#from chatgpt_response import chatgpt_response
from yt_dlp_play_m3u8 import play_m3u8
from hass_process import hass_process
from get_weather import get_weather
from ngay_nay_nam_xua import today_history_process
from gpiozero import Button

obj_music = {"bài hát", "nhạc"}
obj_hass = {"kịch bản", "thực hiện", "thực thi", "quạt","đèn"}
obj_weather = {"thời tiết","có mưa không", "Thời tiết"}
obj_today_history = {"lịch sử","năm xưa" }

loi=0
success = False


# Khai báo các nút nhấn với các chân GPIO tương ứng K1 K3 K4 K2
button_increase = Button(5)
button_decrease = Button(25)
button_wakeup = Button(26)
button_stop = Button(6)



led = Led()
filename = "respond.mp3"
btn_wakeup = False
tts_thread = None 
playing_tts = False
music_path = None


# Cấu hình Generative AI
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")
# Hàm sinh phản hồi từ Generative AI
def generate_ai_response(data):
    response = model.generate_content(data)
    return response.text


def increase_volume():
    print("Tăng âm lượng")
    subprocess.run(["amixer", "sset", "Speaker", "5%+"])
    #subprocess.run(["amixer", "sset", "Playback", "5%+"])
    answer_text = "đã tăng âm lượng thêm 5%"
    led.set_state('SPEAK')
    text_to_speech(answer_text, "vi", music_path)
    led.set_state('OFF')

def decrease_volume():
    print("Giảm âm lượng")
    #print("Giảm âm lượng")
    subprocess.run(["amixer", "sset", "Speaker", "5%-"])
    #subprocess.run(["amixer", "sset", "Playback", "5%-"])
    answer_text = "đã giảm âm lượng thêm 5%"
    led.set_state('SPEAK')
    text_to_speech(answer_text, "vi", music_path)
    led.set_state('OFF')

def wakeup():
    global btn_wakeup, loi,  music_path, led
    print("Wakeup")
    btn_wakeup = True
    while btn_wakeup:
        #pixels.wakeup()
        #led.set_color((0, 255, 0))
        led.set_state('WAKEUP')
        subprocess.call(["ffplay", "-nodisp", "-autoexit", 'sounds/ding.mp3'])
        #led.set_color((0, 0, 0))
        #text_to_speech("Xin chào", filename)
        #play(filename)
        query = recognize_speech()
        #query = stt_process()
        #led.set_color((0, 0, 255))
        led.set_state('THINK')
        #pixels.think()
        try:
            if query == 'Chào bạn':
                btn_wakeup = False
                #led.rainbow_cycle(0.001)
                #pixels.speak()
                #led.set_state('SPEAK')
                answer_text = "Chào bạn nhé. Cần điều khiển thiết bị hay mở bài hát, bạn cứ gọi và ra lệnh cho tôi nhé."
                #text_to_speech("Chào bạn nhé. Cần điều khiển thiết bị hay mở bài hát, bạn cứ gọi và ra lệnh cho tôi nhé.", filename)
                #play(filename)
            elif 'tăng âm lượng' in query:
                subprocess.run(["amixer", "sset", "Speaker", "5%+"])
                answer_text = "đã tăng âm lượng thêm 5%"
                #led.rainbow_cycle(0.001)
                #text_to_speech(answer_text, filename)
                #play(filename)
        
            elif 'giảm âm lượng' in query:
                subprocess.run(["amixer", "sset", "Speaker", "5%-"])
                answer_text = "đã giảm âm lượng thêm 5%"
                #led.rainbow_cycle(0.001)
                #text_to_speech(answer_text, filename)
                #play(filename)
                
            elif 'Mấy giờ' in query or 'mấy giờ' in query:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M")
                answer_text = f"Bây giờ là: {formatted_time}"
                #led.rainbow_cycle(0.001)
                #text_to_speech(answer_text, filename)
                #play(filename)   
            elif any(item in query for item in obj_today_history): 
                answer_text = today_history_process('TODAY') 
                btn_wakeup = False
                
            elif any(item in query for item in obj_music):
                song_name = extract_song_name(query)
                #led.rainbow_cycle(0.001)
                answer_text, music_path = play_m3u8(song_name)
                btn_wakeup = False
                #handle_music_and_lights(song_name, pixels)
                
            elif any(item in query for item in obj_hass):
                answer_text = hass_process(query)
                #led.rainbow_cycle(0.001)
                #pixels.speak()
                #text_to_speech(answer_text, filename)
                #play(filename)
            elif any(item in query for item in obj_weather):
                answer_text = get_weather(my_city)
                #led.rainbow_cycle(0.001)
                #pixels.speak()
                #text_to_speech(answer_text, filename)
                #play(filename)
            else:
                #response = callOpenai.openai_create(query)
                answer_text = generate_ai_response(query)
                #ranswer_text = chatgpt_response(query)
                print("GPT:", answer_text)
                btn_wakeup = False
                #led.set_state('SPEAK')
                #led.rainbow_cycle(0.001)
                #pixels.speak()
                #text_to_speech(result, filename)
                #play(filename)

        except Exception as e:
            print(f"Lỗi xử lý: {e}")
            answer_text = 'Không nhận dạng được câu lệnh'
            #text_to_speech(answer_text, "vi", music_path)
            #led.set_state('SPEAK')
            #led.rainbow_cycle(0.001)
            #pixels.speak()
            #text_to_speech(answer_text, filename)
            #play(filename)
            loi=loi+1
            if(loi==2): 
                loi=0
                btn_wakeup = False
        handle_tts_and_lights(answer_text, "vi", led, music_path)
        music_path = None
        subprocess.call(["ffplay", "-nodisp", "-autoexit", "sounds/dong.mp3"])
        led.set_state('OFF')
        #led._off()
        #pixels.off()
        print("End trò chuyện")

def stop():
    global success, music_path, playing_tts, tts_thread, btn_wakeup
    print("Nút stop được nhấn")
    if playing_tts and tts_thread.is_alive():
        success = False
        btn_wakeup = False
        subprocess.call(["pkill", "ffplay"])  # Dừng phát nhạc
        playing_tts = False
        music_path = None
        #pixels.off()
        

def extract_song_name(text):
    match = re.search(r"(nhạc|bài hát)\s+(.*)", text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    return 'Mộng hoa sim'
    
def handle_tts_and_lights(answer, lang, led, music_path):
    global tts_thread, playing_tts
    """
    Chạy đồng thời phát nhạc và hiệu ứng đèn.
    """
    # Tạo thread cho phát nhạc
    tts_thread = threading.Thread(target=text_to_speech, args=(answer, lang, music_path))
    # Tạo thread cho hiệu ứng đèn
    lights_thread = threading.Thread(target=led.set_state('SPEAK'))

    # Bắt đầu cả hai thread
    tts_thread.start()
    lights_thread.start()
    playing_tts = True

    # Chờ cả hai hoàn thành (nếu cần)
    tts_thread.join()
    lights_thread.join()
    playing_tts = False    
    
def play(filename):
    #playsound.playsound(filename)
    subprocess.call(["ffplay", "-nodisp", "-autoexit", filename])
    os.remove(filename)

 
def main():
    global success, loi, music_path, playing_tts, tts_thread, btn_wakeup
    
    try:
        #buttons = setup_buttons()
        #pixels = Pixels()
        #led=Led()
        # Gắn hàm cho sự kiện nhấn nút
        button_increase.when_pressed = increase_volume
        button_decrease.when_pressed = decrease_volume
        button_wakeup.when_pressed = wakeup
        button_stop.when_pressed = stop
        led.set_state('SPEAK')
        #pixels.speak()
        #led.rainbow_cycle(0.001)
        speech = "Xin chào, mời bạn đánh thức và ra khẩu lệnh cho tôi"
        text_to_speech(speech, "vi", music_path)
        #text_to_speech(speech, filename)
        #play(filename)
        #led.set_color((0, 0, 0))
        music_path = None
        #pixels.off()
        led.set_state('OFF')
        

        while True:
            success = waitForWakeWord.wait()
            #if not success:
            #    break  # Nếu không kích hoạt, thoát chương trình
            while success:
                #pixels.wakeup()
                #led.set_color((0, 255, 0))
                led.set_state('WAKEUP')
                subprocess.call(["ffplay", "-nodisp", "-autoexit", 'sounds/ding.mp3'])
                #led.set_color((0, 0, 0))
                #text_to_speech("Xin chào", filename)
                #play(filename)
                query = recognize_speech()
                #query = stt_process()
                #led.set_color((0, 0, 255))
                led.set_state('THINK')
                #pixels.think()
                try:
                    if query == 'Chào bạn':
                        success = False
                        #led.rainbow_cycle(0.001)
                        #pixels.speak()
                        #led.set_state('SPEAK')
                        answer_text = "Chào bạn nhé. Cần điều khiển thiết bị hay mở bài hát, bạn cứ gọi và ra lệnh cho tôi nhé."
                        #text_to_speech("Chào bạn nhé. Cần điều khiển thiết bị hay mở bài hát, bạn cứ gọi và ra lệnh cho tôi nhé.", filename)
                        #play(filename)
                    elif 'tăng âm lượng' in query:
                        subprocess.run(["amixer", "sset", "Speaker", "5%+"])
                        answer_text = "đã tăng âm lượng thêm 5%"
                        #led.rainbow_cycle(0.001)
                        #text_to_speech(answer_text, filename)
                        #play(filename)
                
                    elif 'giảm âm lượng' in query:
                        subprocess.run(["amixer", "sset", "Speaker", "5%-"])
                        answer_text = "đã giảm âm lượng thêm 5%"
                        #led.rainbow_cycle(0.001)
                        #text_to_speech(answer_text, filename)
                        #play(filename)
                        
                    elif 'Mấy giờ' in query or 'mấy giờ' in query:
                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%H:%M")
                        answer_text = f"Bây giờ là: {formatted_time}"
                        #led.rainbow_cycle(0.001)
                        #text_to_speech(answer_text, filename)
                        #play(filename)   
                    elif any(item in query for item in obj_today_history): 
                        answer_text = today_history_process('TODAY') 
                        success = False
                    elif any(item in query for item in obj_music):
                        song_name = extract_song_name(query)
                        #led.rainbow_cycle(0.001)
                        answer_text, music_path = play_m3u8(song_name)
                        success = False
                        #handle_music_and_lights(song_name, pixels)
                        
                    elif any(item in query for item in obj_hass):
                        answer_text = hass_process(query)
                        #led.rainbow_cycle(0.001)
                        #pixels.speak()
                        #text_to_speech(answer_text, filename)
                        #play(filename)
                    elif any(item in query for item in obj_weather):
                        answer_text = get_weather(my_city)
                        #led.rainbow_cycle(0.001)
                        #pixels.speak()
                        #text_to_speech(answer_text, filename)
                        #play(filename)
                    else:
                        #response = callOpenai.openai_create(query)
                        answer_text = generate_ai_response(query)
                        #ranswer_text = chatgpt_response(query)
                        print("GPT:", answer_text)
                        success = False
                        #led.set_state('SPEAK')
                        #led.rainbow_cycle(0.001)
                        #pixels.speak()
                        #text_to_speech(result, filename)
                        #play(filename)

                except Exception as e:
                    print(f"Lỗi xử lý: {e}")
                    answer_text = 'Không nhận dạng được câu lệnh'
                    #text_to_speech(answer_text, "vi", music_path)
                    #led.set_state('SPEAK')
                    #led.rainbow_cycle(0.001)
                    #pixels.speak()
                    #text_to_speech(answer_text, filename)
                    #play(filename)
                    loi=loi+1
                    if(loi==2): 
                        loi=0
                        success = False
                handle_tts_and_lights(answer_text, "vi", led, music_path)
                music_path = None
                subprocess.call(["ffplay", "-nodisp", "-autoexit", "sounds/dong.mp3"])
                led.set_state('OFF')
                #led._off()
                #pixels.off()
                print("End trò chuyện")
    except KeyboardInterrupt:
        print("Chương trình đã dừng lại.")
    finally:
        # Cleanup GPIO khi chương trình kết thúc
        #GPIO.cleanup()
        print("GPIO đã được giải phóng.")
    
if __name__ == "__main__":
    main()