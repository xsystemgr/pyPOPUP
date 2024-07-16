import webview
import schedule
import time
import ctypes

def get_display_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)
    name_buffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, name_buffer, size)
    return name_buffer.value

display_name = get_display_name()

html_content = f"""
<!doctype html>
<html>
<head>
   
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }}
        .popup {{
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            text-align: center;
        }}
        .logo {{
            width: 249px;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="popup">
        <img src="https://i.imgur.com/1.png" alt="Logo" class="logo"/>
        <h1>Σημαντική Ειδοποίηση</h1>
        <p>Αγαπητέ/ή {display_name}, παρακαλώ βεβαιώσου ότι έχεις εισάγει την Ψηφιακή Κάρτα Εργασίας κατά την προσέλευσή σου και την αποχώρησή σου!</p>
    </div>
</body>
</html>
"""

def set_topmost_and_close(window):
    window.evaluate_js("""
        window.focus();
        setTimeout(() => {
            window.focus();
        }, 100);
    """)


def show_popup():
    window = webview.create_window("Ενημερωτικό μήνυμα", html=html_content, width=600, height=260, resizable=False,  on_top=True, frameless=False, draggable=False)
    webview.start(set_topmost_and_close, window)

def schedule_popup():
    show_popup()

def read_schedule_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        times = file.readlines()
        for time_str in times:
            time_str = time_str.strip()
            if time_str:
                schedule.every().day.at(time_str).do(schedule_popup)


read_schedule_from_file('time.dat')


while True:
    schedule.run_pending()
    time.sleep(1)
