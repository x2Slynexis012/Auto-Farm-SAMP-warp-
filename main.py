from customtkinter import *
import ctypes
import subprocess
import keyboard
from tkinter import messagebox
import pyautogui
import pymem
import time
import math
import threading

app = CTk()
width = 350
height = 350
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
app.title("Onyx Hub ( Update 1.0 ) Newthings City")
app.geometry(f"{width}x{height}+{x}+{y}")
app.attributes("-topmost", True)
app.overrideredirect(True)
app.lift()
app.iconbitmap("https://media.discordapp.net/attachments/1325067517034758155/1333466876319240222/1000001898-removebg-preview.png?ex=67aacb8d&is=67a97a0d&hm=8923538dcb1a86b8d4230a1818835a60fb9ea8a821e39e5ff7777691939ec52e&=&format=webp&quality=lossless&width=473&height=473")


def close_app(event=None):
    app.destroy()

def start_move(event):
    app.x = event.x
    app.y = event.y

def on_move(event):
    x = app.winfo_x() + (event.x - app.x)
    y = app.winfo_y() + (event.y - app.y)
    app.geometry(f"+{x}+{y}")

app.bind("<ButtonPress-1>", start_move)
app.bind("<B1-Motion>", on_move)
app.bind("<Escape>", close_app)

class GTAWarp:
    def __init__(self):
        self.process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    def get_player_pointer(self):
        """ ดึงค่า Pointer ของผู้เล่น """
        return self.process.read_ulong(0xB6F5F0)

    def warp(self, x, y, z):
        """ วาร์ปตัวละครไปยังพิกัด X, Y, Z """
        try:
            pPed = self.get_player_pointer()
            if pPed == 0:
                print("ไม่พบตัวละครผู้เล่น")
                return
            
            pMatrix = self.process.read_ulong(pPed + 0x14)  # อ่านค่าพิกัด Matrix
            if pMatrix == 0:
                print("ไม่พบ Matrix ของตัวละคร")
                return

            # เขียนค่าพิกัดใหม่
            self.process.write_float(pMatrix + 0x30, x)  # พิกัด X
            self.process.write_float(pMatrix + 0x34, y)  # พิกัด Y
            self.process.write_float(pMatrix + 0x38, z)  # พิกัด Z

            print(f"วาร์ปไปที่ X: {x}, Y: {y}, Z: {z}")

        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการวาร์ป: {e}")

#Data
fivem_rock_points = [
    (571.2614, 853.9786, -42.6644),
    (558.6510, 841.1940, -41.5409),
    (540.0502, 857.3710, -42.8959),
    (530.1744, 874.4430, -40.7905),
    (545.1473, 909.4879, -42.9609),
    (560.8115, 920.2154, -42.9609),
    (575.9242, 923.8702, -42.9609),
    (590.2299, 919.7897, -42.9713),
    (597.8012, 921.9247, -42.6737)
]
fivem_iron_points = [
    (-2002.5619, -1587.7234, 86.4764),
    (-1983.7312, -1576.8341, 87.1471),
    (-1999.0846, -1548.3113, 84.6718),
    (-1975.8281, -1525.5272, 88.1155),
    (-1992.2220, -1509.0991, 84.4888),
    (-1980.5570, -1480.8966, 85.9530),
    (-2006.9398, -1471.7588, 84.6051)
]
fivem_durian_points = [
    (-189.5543, 78.0180, 3.1172),
    (-192.6612, 70.7056, 3.1172),
    (-200.0063, 51.2652, 3.1172),
    (-202.0906, 46.3317, 3.1172),
    (-192.3195, 27.4379, 3.1172),
    (-191.3208, 31.7573, 3.1172),
    (-189.6457, 37.5022, 3.1172),
    (-188.2370, 42.4932, 3.1172),
    (-186.0526, 48.3083, 3.1172),
    (-184.8260, 54.8555, 3.1172),
    (-181.7953, 61.1823, 3.1172)
]
fivem_avocado_points = [
    (-138.4264, 57.1933, 3.1172),
    (-136.7897, 47.5599, 3.1172),
    (-140.8993, 45.1871, 3.1172),
    (-144.1347, 38.5332, 3.1172),
    (-142.0209, 34.0285, 3.1172),
    (-139.0228, 39.8258, 3.1172)
]


#Function
# switch
autorock_var = IntVar()
goprocressrock_var = IntVar()

autoiron_var = IntVar()
goprocressiron_var = IntVar()

autodurian_var = IntVar()
goprocressdurian_var = IntVar()

autoavocado_var = IntVar()
goprocressavocado_var = IntVar()


# System
is_Walking = False

is_AutoRock = False

is_AutoIron = False

is_AutoDurian = False

is_AutoAvocado = False


# Value
press_distance = 1.0
press_duration = 13.0

def get_player_pointer(process):
    return process.read_ulong(0xB6F5F0)

def get_position(process):
    pPed = get_player_pointer(process)
    if pPed == 0:
        return None

    pMatrix = process.read_ulong(pPed + 0x14)
    if pMatrix == 0:
        return None

    x = process.read_float(pMatrix + 0x30)
    y = process.read_float(pMatrix + 0x34)
    z = process.read_float(pMatrix + 0x38)
    return (x, y, z)

def press_n_key():
    for _ in range(5):
        pyautogui.press('f6')
        pyautogui.press('enter')
        keyboard.press('n')
        pyautogui.press('f6')
        pyautogui.press('enter')
    time.sleep(press_duration)

def press_n_key_procress():
    keyboard.press('n')
    time.sleep(0.1)
    keyboard.release('n')

def go_procress(target_x, target_y, target_z, speed=0.2):
    global is_Walking
    process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    print(f"🚶‍♂️ กำลังเดินไปที่ X={target_x}, Y={target_y}, Z={target_z}")

    while is_Walking:
        pos = get_position(process)
        if pos is None:
            break

        x, y, z = pos
        distance = math.sqrt((target_x - x) ** 2 + (target_y - y) ** 2)

        if distance < 0.5:
            threading.Thread(target=press_n_key_procress).start()

            break

        # คำนวณทิศทางการเคลื่อนที่
        direction_x = (target_x - x) / distance
        direction_y = (target_y - y) / distance
        direction_z = (target_z - z) / distance

        # อัปเดตตำแหน่งทีละนิด
        new_x = x + direction_x * speed
        new_y = y + direction_y * speed
        new_z = z + direction_z * speed

        # เขียนค่าพิกัดใหม่
        pPed = get_player_pointer(process)
        if pPed == 0:
            return

        pMatrix = process.read_ulong(pPed + 0x14)
        if pMatrix == 0:
            return

        process.write_float(pMatrix + 0x30, new_x)
        process.write_float(pMatrix + 0x34, new_y)
        process.write_float(pMatrix + 0x38, new_z)

        time.sleep(0.04)

def start_walking(target_x, target_y, target_z):
    global is_Walking
    if not is_Walking:
        is_Walking = True
        walk_thread = threading.Thread(target=go_procress, args=(target_x, target_y, target_z))
        walk_thread.start()

def stop_walking():
    global is_Walking
    is_Walking = False



def AutoRock(fivem_rock_points, speed=0.1):
    global is_AutoRock, press_distance
    process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    for index, (target_x, target_y, target_z) in enumerate(fivem_rock_points):
        if not is_AutoRock:
            print("การเดินถูกหยุด")
            return  # หยุดการเดิน

        print(f"กำลังวาร์ปไปยังจุดที่ {index + 1}/{len(fivem_rock_points)}: X={target_x}, Y={target_y}, Z={target_z}")

        # วาร์ปไปยังพิกัดใหม่ทันที
        pPed = get_player_pointer(process)
        if pPed == 0:
            return

        pMatrix = process.read_ulong(pPed + 0x14)
        if pMatrix == 0:
            return

        # เขียนค่าพิกัดใหม่ให้กับตัวละคร
        process.write_float(pMatrix + 0x30, target_x)
        process.write_float(pMatrix + 0x34, target_y)
        process.write_float(pMatrix + 0x38, target_z)

        print(f"ถึงจุดที่ {index + 1} แล้ว!")

        # ใช้ Threading ในการกดปุ่ม N
        n_thread = threading.Thread(target=press_n_key_procress)
        n_thread.start()

        time.sleep(6)  # รอเวลา 13 วินาที ก่อนที่จะไปยังจุดถัดไป

    is_AutoRock = False
    print("วาร์ปไปทุกจุดเสร็จสิ้นแล้ว!")
    StartAutoRock()  # เริ่มต้นการทำงานใหม่ หากต้องการให้ฟังก์ชันนี้ทำงานซ้ำ

def start_AutoRock_thread(fivem_rock_points):
    global is_AutoRock
    is_AutoRock = True
    AutoRock(fivem_rock_points)  # เรียกใช้ฟังก์ชันเดินไปยังพิกัด

def StartAutoRock():
    global is_AutoRock
    if not is_AutoRock:
        is_AutoRock = True
        thread = threading.Thread(target=start_AutoRock_thread, args=(fivem_rock_points,))
        thread.start()

def stop_AutoRock():
    global is_AutoRock
    is_AutoRock = False



def Start_AutoRock():
    if autorock_var.get():
        print("1")
        StartAutoRock()
    else:
        print("2")
        stop_AutoRock()

def Start_ProcressAutoRock():
    if goprocressrock_var.get():
        start_walking(-1062.4270,1562.6608,33.2313)
    else:
        stop_walking()

def AutoIron(fivem_iron_points, speed=0.1):
    global is_AutoIron, press_distance
    process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    for index, (target_x, target_y, target_z) in enumerate(fivem_iron_points):
        if not is_AutoIron:
            print("การเดินถูกหยุด")
            return  # หยุดการเดิน

        print(f"กำลังวาร์ปไปยังจุดที่ {index + 1}/{len(fivem_iron_points)}: X={target_x}, Y={target_y}, Z={target_z}")

        # วาร์ปไปยังพิกัดใหม่ทันที
        pPed = get_player_pointer(process)
        if pPed == 0:
            return

        pMatrix = process.read_ulong(pPed + 0x14)
        if pMatrix == 0:
            return

        # เขียนค่าพิกัดใหม่ให้กับตัวละคร
        process.write_float(pMatrix + 0x30, target_x)
        process.write_float(pMatrix + 0x34, target_y)
        process.write_float(pMatrix + 0x38, target_z)

        print(f"ถึงจุดที่ {index + 1} แล้ว!")

        # ใช้ Threading ในการกดปุ่ม N
        n_thread = threading.Thread(target=press_n_key_procress)
        n_thread.start()

        time.sleep(6)  # รอเวลา 13 วินาที ก่อนที่จะไปยังจุดถัดไป

    is_AutoIron = False
    print("วาร์ปไปทุกจุดเสร็จสิ้นแล้ว!")
    StartAutoIron()  # เริ่มต้นการทำงานใหม่ หากต้องการให้ฟังก์ชันนี้ทำงานซ้ำ

def start_AutoIron_thread(fivem_iron_points):
    global is_AutoIron
    is_AutoIron = True
    AutoIron(fivem_iron_points)  # เรียกใช้ฟังก์ชันเดินไปยังพิกัด

def StartAutoIron():
    global is_AutoIron
    if not is_AutoIron:
        is_AutoIron = True
        thread = threading.Thread(target=start_AutoIron_thread, args=(fivem_iron_points,))
        thread.start()

def stop_AutoIron():
    global is_AutoIron
    is_AutoIron = False



def Start_AutoIron():
    if autoiron_var.get():
        print("1")
        StartAutoIron()
    else:
        print("2")
        stop_AutoIron()

def Start_ProcressAutoIron():
    if goprocressiron_var.get():
        start_walking(-1062.4270,1562.6608,33.2313)
    else:
        stop_walking()

def _Tobee():
    gta = GTAWarp()
    gta.warp(-280.8791,-951.5029,40.6325)
    time.sleep(4)
    press_n_key_procress()

def AutoDurian(fivem_durian_points, speed=0.1):
    global is_AutoDurian, press_distance
    process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    for index, (target_x, target_y, target_z) in enumerate(fivem_durian_points):
        if not is_AutoDurian:
            print("การเดินถูกหยุด")
            return  # หยุดการเดิน

        print(f"กำลังวาร์ปไปยังจุดที่ {index + 1}/{len(fivem_durian_points)}: X={target_x}, Y={target_y}, Z={target_z}")

        # วาร์ปไปยังพิกัดใหม่ทันที
        pPed = get_player_pointer(process)
        if pPed == 0:
            return

        pMatrix = process.read_ulong(pPed + 0x14)
        if pMatrix == 0:
            return

        # เขียนค่าพิกัดใหม่ให้กับตัวละคร
        process.write_float(pMatrix + 0x30, target_x)
        process.write_float(pMatrix + 0x34, target_y)
        process.write_float(pMatrix + 0x38, target_z)

        print(f"ถึงจุดที่ {index + 1} แล้ว!")

        # ใช้ Threading ในการกดปุ่ม N
        n_thread = threading.Thread(target=press_n_key_procress)
        n_thread.start()

        time.sleep(6)  # รอเวลา 13 วินาที ก่อนที่จะไปยังจุดถัดไป

    is_AutoDurian = False
    print("วาร์ปไปทุกจุดเสร็จสิ้นแล้ว!")
    StartAutoDurian()  # เริ่มต้นการทำงานใหม่ หากต้องการให้ฟังก์ชันนี้ทำงานซ้ำ

def start_AutoDurian_thread(fivem_durian_points):
    global is_AutoDurian
    is_AutoDurian = True
    AutoDurian(fivem_durian_points)  # เรียกใช้ฟังก์ชันเดินไปยังพิกัด

def StartAutoDurian():
    global is_AutoDurian
    if not is_AutoDurian:
        is_AutoDurian = True
        thread = threading.Thread(target=start_AutoDurian_thread, args=(fivem_durian_points,))
        thread.start()

def stop_AutoDurian():
    global is_AutoDurian
    is_AutoDurian = False

def AutoAvocado(fivem_avocado_points, speed=0.1):
    global is_AutoAvocado, press_distance
    process = pymem.Pymem("gta_sa.exe")  # เชื่อมต่อกับเกม

    for index, (target_x, target_y, target_z) in enumerate(fivem_avocado_points):
        if not is_AutoAvocado:
            print("การเดินถูกหยุด")
            return  # หยุดการเดิน

        print(f"กำลังวาร์ปไปยังจุดที่ {index + 1}/{len(fivem_avocado_points)}: X={target_x}, Y={target_y}, Z={target_z}")

        # วาร์ปไปยังพิกัดใหม่ทันที
        pPed = get_player_pointer(process)
        if pPed == 0:
            return

        pMatrix = process.read_ulong(pPed + 0x14)
        if pMatrix == 0:
            return

        # เขียนค่าพิกัดใหม่ให้กับตัวละคร
        process.write_float(pMatrix + 0x30, target_x)
        process.write_float(pMatrix + 0x34, target_y)
        process.write_float(pMatrix + 0x38, target_z)

        print(f"ถึงจุดที่ {index + 1} แล้ว!")

        # ใช้ Threading ในการกดปุ่ม N
        n_thread = threading.Thread(target=press_n_key_procress)
        n_thread.start()

        time.sleep(6)  # รอเวลา 13 วินาที ก่อนที่จะไปยังจุดถัดไป

    is_AutoAvocado = False
    print("วาร์ปไปทุกจุดเสร็จสิ้นแล้ว!")
    StartAutoAvocado()  # เริ่มต้นการทำงานใหม่ หากต้องการให้ฟังก์ชันนี้ทำงานซ้ำ

def start_AutoAvocado_thread(fivem_avocado_points):
    global is_AutoAvocado
    is_AutoAvocado = True
    AutoAvocado(fivem_avocado_points)  # เรียกใช้ฟังก์ชันเดินไปยังพิกัด

def StartAutoAvocado():
    global is_AutoAvocado
    if not is_AutoAvocado:
        is_AutoAvocado = True
        thread = threading.Thread(target=start_AutoAvocado_thread, args=(fivem_avocado_points,))
        thread.start()

def stop_AutoAvocado():
    global is_AutoAvocado
    is_AutoAvocado = False



def Start_AutoAvocado():
    if autoavocado_var.get():
        print("1")
        StartAutoAvocado()
    else:
        print("2")
        stop_AutoAvocado()

def Start_ProcressAutoAvocado():
    if goprocressavocado_var.get():
        start_walking(-1062.4270,1562.6608,33.2313)
    else:
        stop_walking()


def Start_AutoDurian():
    if autodurian_var.get():
        print("1")
        StartAutoDurian()
    else:
        print("2")
        stop_AutoDurian()

def Start_ProcressAutoDurian():
    if goprocressdurian_var.get():
        start_walking(-1062.4270,1562.6608,33.2313)
    else:
        stop_walking()

def Menu(value):
    if value == "GENERAL":
        general.pack(pady=10, padx=20, fill="both", expand=True)
        blackjob.pack_forget()
        progress.pack_forget()
    if value == "BLACKJOB":
        general.pack_forget()
        blackjob.pack(pady=10, padx=20, fill="both", expand=True)
        progress.pack_forget()
    if value == "PROGRESS":
        general.pack_forget()
        blackjob.pack_forget()
        progress.pack(pady=10, padx=20, fill="both", expand=True)
    if value == "DISCORD":
        os.system("start https://discord.gg/J6YyhWhbx7")



segmented_button = CTkSegmentedButton(app, values=["GENERAL", "BLACKJOB", "PROGRESS", "DISCORD"], selected_color="#0066FF", selected_hover_color="#0066FF", command=Menu)
segmented_button.pack(pady=20)
segmented_button.set("GENERAL")

general = CTkScrollableFrame(app, width=450, height=250, fg_color="gray14")
general.pack(pady=10, padx=20, fill="both", expand=True)

CTkLabel(general, text="FiveM Game | 2.0", font=("Lucida Console", 20)).pack(pady=5,padx=5, fill="x")
CTkLabel(general, text="IP | 191.96.92.87:7777", font=("Lucida Console", 15)).pack(pady=5,padx=5, fill="x")

CTkLabel(general, text="[ ⛏ ] Auto Mining", font=("Lucida Console", 20)).pack(pady=10,padx=5, fill="x")
CTkSwitch(general, text="Auto Mining / ขุดเหมืองออโต้ ", variable=autorock_var, command=Start_AutoRock, progress_color="#0066CC",font=("Lucida Console", 15)).pack(pady=7,padx=5, fill="x")

CTkLabel(general, text="[ ⛏ ] Auto Mining [2]", font=("Lucida Console", 20)).pack(pady=10,padx=5, fill="x")
CTkSwitch(general, text="Auto Mining / ขุดเหมืองออโต้ [2]", variable=autoiron_var, command=Start_AutoIron, progress_color="#0066CC",font=("Lucida Console", 15)).pack(pady=7,padx=5, fill="x")

CTkLabel(general, text="[ 🐝 ] Auto Bee ", font=("Lucida Console", 20)).pack(pady=10,padx=5, fill="x")
CTkButton(general, text="งานผึ้ง (มีออโต้ฟาร์มอยู่แล้ว)", command=_Tobee, corner_radius=5, fg_color="#0066FF", hover_color="#0066CC",font=("Lucida Console", 15)).pack(pady=7,padx=5, fill="x")

CTkLabel(general, text="[ 🌲 ] Auto Avocado ", font=("Lucida Console", 20)).pack(pady=10,padx=5, fill="x")
CTkSwitch(general, text="Auto Avocado / เก็บทอะโวคาโดออโต้", variable=autoavocado_var, command=Start_AutoAvocado, progress_color="#0066CC",font=("Lucida Console", 15)).pack(pady=7,padx=5, fill="x")

CTkLabel(general, text="[ 🌲 ] Auto Durian ", font=("Lucida Console", 20)).pack(pady=10,padx=5, fill="x")
CTkSwitch(general, text="Auto Durian / เก็บทุเรียนออโต้", variable=autodurian_var, command=Start_AutoDurian, progress_color="#0066CC",font=("Lucida Console", 15)).pack(pady=7,padx=5, fill="x")


blackjob = CTkScrollableFrame(app, width=450, height=250, fg_color="gray14")

def on_select_poon(choice):
    if choice == "จกปูน 1":
        gta = GTAWarp()
        gta.warp(2380.8499,2755.9158,10.8203)
    elif choice == "จกปูน 2":
        gta = GTAWarp()
        gta.warp(2401.8691,2571.1565,21.8750)
    elif choice == "จกปูน 3":
        gta = GTAWarp()
        gta.warp(2402.2561,2527.1079,21.8750)
    elif choice == "จกปูน 4":
        gta = GTAWarp()
        gta.warp(1741.7793,770.6240,10.8279)
    elif choice == "จกปูน 5":
        gta = GTAWarp()
        gta.warp(1711.6165,1286.8607,10.8203)
    else:
        print("ยังไม่เลือก")

def on_select_wire(choice):
    if choice == "จกสายไฟ 1":
        gta = GTAWarp()
        gta.warp(2057.9954,862.1374,6.8831)
    elif choice == "จกสายไฟ 2":
        gta = GTAWarp()
        gta.warp(1815.9474,959.4778,7.6242)
    elif choice == "จกสายไฟ 3":
        gta = GTAWarp()
        gta.warp(1560.2120,905.3335,10.8203)
    elif choice == "จกสายไฟ 4":
        gta = GTAWarp()
        gta.warp(1910.4395,637.4687,10.6719)
    else:
        print("ยังไม่เลือก")

def on_select_escape(choice):
    if choice == "จุดหลบหนี 1":
        gta = GTAWarp()
        gta.warp(-2049.5862,-442.2167,75.2558)
    elif choice == "จุดหลบหนี 2":
        gta = GTAWarp()
        gta.warp(-2353.0305,913.8111,93.6308)
    elif choice == "จุดหลบหนี 3":
        gta = GTAWarp()
        gta.warp(-2846.4185,2878.1990,58.5751)
    elif choice == "จุดหลบหนี 4":
        gta = GTAWarp()
        gta.warp(2733.0503,-1765.0288,43.9820)
    elif choice == "จุดหลบหนี 5":
        gta = GTAWarp()
        gta.warp(-2013.6476,-1045.5072,53.3498)
    elif choice == "จุดหลบหนี 6":
        gta = GTAWarp()
        gta.warp(-2653.7520,657.9871,66.0938)
    else:
        print("ยังไม่เลือก")

CTkLabel(blackjob, text="[ 📢 ] Poon point", font=("Lucida Console", 20)).pack(pady=5,padx=5, fill="x")

CTkComboBox(blackjob, values=["จกปูน 1", "จกปูน 2", "จกปูน 3", "จกปูน 4", "จกปูน 5"],  command=on_select_poon).pack(pady=5,padx=5, fill="x")

CTkLabel(blackjob, text="[ 📢 ] Wire point", font=("Lucida Console", 20)).pack(pady=5,padx=5, fill="x")

CTkComboBox(blackjob, values=["จกสายไฟ 1", "จกสายไฟ 2", "จกสายไฟ 3", "จกสายไฟ 4"],  command=on_select_wire).pack(pady=5,padx=5, fill="x")

CTkLabel(blackjob, text="[ 📢 ] Escape", font=("Lucida Console", 20)).pack(pady=5,padx=5, fill="x")

CTkComboBox(blackjob, values=["จุดหลบหนี 1", "จุดหลบหนี 2", "จุดหลบหนี 3", "จุดหลบหนี 4", "จุดหลบหนี 5", "จุดหลบหนี 6"],  command=on_select_escape).pack(pady=5,padx=5, fill="x")

progress = CTkScrollableFrame(app, width=450, height=250, fg_color="gray14")

def on_select(choice):
    if choice == "Rock [1]":
        gta = GTAWarp()
        gta.warp(684.6171,848.7786,-42.9609)
        time.sleep(4)
        press_n_key_procress()
    elif choice == "Rock [2]":
        gta = GTAWarp()
        gta.warp(-2000.9896,-1490.6853,83.9201)
        time.sleep(4)
        press_n_key_procress()
    else:
        print("ยังไม่เลือก")

def go():
    gta = GTAWarp()
    gta.warp(1474.53,744.71,17.95)
    time.sleep(4)
    press_n_key_procress()

CTkLabel(progress, text="[ 📢 ] Auto Progress", font=("Lucida Console", 20)).pack(pady=5,padx=5, fill="x")

CTkComboBox(progress, values=["Rock [1]", "Rock [2]"],  command=on_select).pack(pady=5,padx=5, fill="x")

CTkButton(progress, text="ไปขาย", command=go, corner_radius=5, fg_color="#0066FF", hover_color="#0066CC",font=("Lucida Console", 15)).pack(pady=10,padx=5, fill="x")
def Kuyrai():
    print("Kuyraira")



