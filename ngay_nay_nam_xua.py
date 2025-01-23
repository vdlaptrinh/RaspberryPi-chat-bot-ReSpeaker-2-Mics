import requests
from datetime import datetime, timedelta
import bs4
obj_history = {"lịch sử","năm xưa"}

today_history_url = "https://lichngaytot.com/ngay-nay-nam-xua.html"
today_hisotry_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

def get_current_date():
    """
    This function returns a list of dates: yesterday, today, tomorrow,
    the day after tomorrow, and the same day next week.
    """
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    next_day = today + timedelta(days=2)
    next_week = today + timedelta(weeks=1)

    return [yesterday, today, tomorrow, next_day, next_week]

def clean_content(content):
    """
    Cleans the raw HTML content and extracts meaningful text within all elements of class 'table1'.
    If duplicate dates appear in succession, only one is retained.

    Args:
        content (list of BeautifulSoup elements): The list of BeautifulSoup elements with class 'table1'.

    Returns:
        str: The cleaned and processed text from all 'table1' class elements.
    """
    try:
        # Check if the input is valid
        if content:
            combined_text = ""
            for element in content:
                combined_text += ' '.join(element.get_text().strip().split()) + " "

            # Remove duplicate consecutive dates (format DD-MM-YYYY)
            import re
            date_pattern = r"\b(\d{1,2}-\d{1,2}-\d{4})\b"
            seen_dates = set()

            def remove_duplicates(match):
                date = match.group(1)
                if date in seen_dates:
                    return ""  # Remove duplicate date
                seen_dates.add(date)
                return date

            cleaned_text = re.sub(date_pattern, remove_duplicates, combined_text)
            return ' '.join(cleaned_text.split())
        else:
            return "No content found in class 'table1'."
    except Exception as e:
        #print_out('left',f"Error in clean_content: {str(e)}",'red')
        print(f"Error in clean_content: {str(e)}")
        return ""

def today_history_process(opt):
    try:

        # Using a dictionary to map the options to their corresponding functions
        date_map = {
            'YESTERDAY': get_current_date()[0],
            'TODAY': get_current_date()[1],
            'TOMORROW': get_current_date()[2],
            'NEXT_DAY': get_current_date()[3],
            'NEXT_WEEK': get_current_date()[4]  # adding an option for the 5th date
        }
        selected_date = date_map.get(opt)
        if not selected_date:
            return None
        payload = {
            'ngayxem': f"{selected_date.day:02d}-{selected_date.month:02d}-{selected_date.year}"
        }
        response = requests.post(today_history_url, headers=today_hisotry_headers, data=payload)
        
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        table1_content = soup.find_all(class_='table1')
        #print(table1_content)
        return clean_content(table1_content)
    except Exception as e:
        #print_out('left',f"Lỗi xử lý Today_history Skill: {str(e)}",'red')
        return 'Không có câu trả lời từ skill của vietbot trong tình huống này'





# Hàm xử lý văn bản
def custom_skill_process(data):
    answer='Không có câu trả lời từ skill của vietbot trong tình huống này'
    if any(item in data for item in obj_history):
        answer=today_history_process('TODAY')            
    elif 'tăng âm lượng' in data:
        #subprocess.run(["amixer", "sset", "Speaker", "5%+"])
        answer='đã tăng âm lượng thêm 5%'
    elif 'giảm âm lượng' in data:
        #subprocess.run(["amixer", "sset", "Speaker", "5%-"])
        answer='đã giảm âm lượng thêm 5%'
    else:
        #answer=dify_process(data)   
        #answer=chatgpt_process(data) 
        answer='Không có câu trả lời'
    return answer
# Chạy thử chương trình
if __name__ == "__main__":
    data = "ngày này năm xưa"
    result = custom_skill_process(data)
    print(result)
