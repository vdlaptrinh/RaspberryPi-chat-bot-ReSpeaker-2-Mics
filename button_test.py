from gpiozero import Button
import time

# Khai báo nút nhấn, kết nối với GPIO pin 17
button = Button(17)

def button_pressed():
    print("Nút được nhấn")

def button_released():
    print("Nút đã được nhả ra")

def main():
    print("Chương trình đang chạy. Nhấn nút để kiểm tra.")
    button.when_pressed = button_pressed
    while True:

        time.sleep(0.2)  # Tránh lặp liên tục khi nút nhấn giữ

if __name__ == "__main__":
    main()
