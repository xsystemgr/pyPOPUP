import tkinter as tk
from tkinterweb import HtmlFrame
import schedule
import time
import threading
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
    <title>Popup Message</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .popup {{
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            text-align: center;
        }}
        .logo {{
            width: 250px;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="popup">
        <img src="https://i.imgur.com/1.png" alt="Logo" class="logo"/>
        <h1>Σημαντική Ειδοποίηση</h1>
        <p>Αγαπητέ/ή {display_name}, παρακαλώ βεβαιώσου ότι έχεις εισάγει την κάρτα ωρομέτρησης κατά την προσέλευσή σου και την αποχώρησή σου!</p>
    </div>
</body>
</html>
"""

def show_popup():
    root = tk.Tk()
    root.title("Ενημερωτικό μήνυμα")
    root.geometry("600x225")
    root.attributes("-topmost", True)
    root.resizable(False, False)
    root.attributes("-toolwindow", True)
    frame = HtmlFrame(root, horizontal_scrollbar="auto")
    frame.load_html(html_content)
    frame.pack(fill="both", expand=True)


    root.after(50000, root.destroy)

    root.mainloop()

def schedule_popup():
    threading.Thread(target=show_popup).start()

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
