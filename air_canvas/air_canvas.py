import cv2
import numpy as np
import mediapipe as mp
import time
import math

# ==========================================
# 1. AYARLAR VE BAŞLATMA
# ==========================================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85, min_tracking_confidence=0.90)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

success, frame = cap.read()
h_cam, w_cam, _ = frame.shape

# ==========================================
# 2. DÜZ RENK PALETİ VE DEĞİŞKENLER
# ==========================================
colors = {
    "blue": (255, 0, 0),       # Saf Mavi
    "green": (0, 255, 0),      # Saf Yeşil
    "red": (0, 0, 255),        # Saf Kırmızı
    "yellow": (0, 255, 255),   # Saf Sarı
    "purple": (255, 0, 255),   # Saf Mor
    "eraser": (0, 0, 0)
}
current_color_name = "blue"
draw_color = colors[current_color_name]

current_tool = "free"
shape_start_x, shape_start_y = 0, 0
is_drawing_shape = False

brush_thickness = 15
eraser_thickness = 80
xp, yp = 0, 0
canvas = np.zeros((h_cam, w_cam, 3), np.uint8)
pTime = 0

def draw_rounded_rect(img, pt1, pt2, color, thickness=-1, r=10):
    x1, y1 = pt1
    x2, y2 = pt2
    cv2.circle(img, (x1 + r, y1 + r), r, color, thickness)
    cv2.circle(img, (x2 - r, y1 + r), r, color, thickness)
    cv2.circle(img, (x1 + r, y2 - r), r, color, thickness)
    cv2.circle(img, (x2 - r, y2 - r), r, color, thickness)
    cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r), color, thickness)
    return img

# --- ÜST MENÜ HESAPLAMALARI ---
btn_w = 110
btn_h = 80
btn_gap = 20
y_start = 20
y_end = y_start + btn_h

button_names = ["clear", "blue", "green", "red", "yellow", "purple", "eraser"]
total_menu_w = (len(button_names) * btn_w) + ((len(button_names) - 1) * btn_gap)
start_x = int((w_cam - total_menu_w) / 2) 

top_buttons = {}
for i, name in enumerate(button_names):
    x_pos = start_x + (btn_w + btn_gap) * i
    top_buttons[name] = {"x1": x_pos, "x2": x_pos + btn_w, "y1": y_start, "y2": y_end}

# --- SAĞ MENÜ HESAPLAMALARI ---
right_panel_x1 = w_cam - 180
right_panel_x2 = w_cam - 20
btn_h_right = 80
gap_right = 30
y_start_right = 200

right_tools = {}
for i, t_name in enumerate(["free", "rect", "circle"]):
    y_pos = y_start_right + (btn_h_right + gap_right) * i
    right_tools[t_name] = {"x1": right_panel_x1, "x2": right_panel_x2, "y1": y_pos, "y2": y_pos + btn_h_right}

def draw_clean_ui(img, active_color, active_tool, brush_size):
    """Arayüzü Çizen Fonksiyon (Kamera ve Tuval birleştikten SONRA çalışacak)"""
    overlay = img.copy()
    
    # Arka plan panelleri (Yarı saydam)
    draw_rounded_rect(overlay, (start_x - 20, y_start - 10), (start_x + total_menu_w + 20, y_end + 10), (30, 30, 30))
    draw_rounded_rect(overlay, (right_panel_x1 - 10, y_start_right - 20), (right_panel_x2 + 10, right_tools["circle"]["y2"] + 20), (30, 30, 30))
    draw_rounded_rect(overlay, (20, h_cam - 100), (320, h_cam - 20), (30, 30, 30))
    
    img = cv2.addWeighted(overlay, 0.85, img, 0.15, 0)

    # 1. ÜST MENÜYÜ ÇİZ
    for name, coords in top_buttons.items():
        x1, x2, y1, y2 = coords["x1"], coords["x2"], coords["y1"], coords["y2"]
        
        if name == "clear":
            draw_rounded_rect(img, (x1, y1), (x2, y2), (60, 60, 220)) 
            cv2.putText(img, "TEMIZLE", (x1+10, y1+45), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        elif name == "eraser":
            draw_rounded_rect(img, (x1, y1), (x2, y2), (220, 220, 220))
            cv2.putText(img, "SILGI", (x1+25, y1+45), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        else:
            draw_rounded_rect(img, (x1, y1), (x2, y2), colors[name])

        if name == active_color:
            draw_rounded_rect(img, (x1-3, y1-3), (x2+3, y2+3), (255, 255, 255), 3)

    # 2. SAĞ MENÜYÜ ÇİZ (Araçlar)
    for t_name, coords in right_tools.items():
        x1, x2, y1, y2 = coords["x1"], coords["x2"], coords["y1"], coords["y2"]
        
        box_color = (60, 60, 60)
        text_color = (200, 200, 200)
        
        if t_name == active_tool:
            box_color = (255, 255, 255)
            text_color = (0, 0, 0)
            
        draw_rounded_rect(img, (x1, y1), (x2, y2), box_color)
        
        if t_name == "free":
            cv2.putText(img, "SERBEST", (x1 + 15, y1 + 45), cv2.FONT_HERSHEY_DUPLEX, 0.6, text_color, 1, cv2.LINE_AA)
        elif t_name == "rect":
            cv2.putText(img, "KUTU", (x1 + 30, y1 + 45), cv2.FONT_HERSHEY_DUPLEX, 0.6, text_color, 1, cv2.LINE_AA)
        elif t_name == "circle":
            cv2.putText(img, "CEMBER", (x1 + 18, y1 + 45), cv2.FONT_HERSHEY_DUPLEX, 0.6, text_color, 1, cv2.LINE_AA)

    # 3. ALT SOL BİLGİ PANELİ
    tool_text = "Serbest Cizim" if active_tool == "free" else ("Dikdortgen" if active_tool == "rect" else "Cember")
    mode_color = (255, 255, 255) if active_color == "eraser" else draw_color
    
    cv2.putText(img, f"Arac: {tool_text}", (40, h_cam - 60), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img, f"Kalinlik: {brush_size}px", (40, h_cam - 35), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.circle(img, (270, h_cam - 60), 18, mode_color, cv2.FILLED)
    cv2.circle(img, (270, h_cam - 60), 18, (255, 255, 255), 2, cv2.LINE_AA)
            
    return img

# ==========================================
# 3. PENCERE AYARLARI 
# ==========================================
window_name = "Air Canvas - Ultra (Arda Irmak)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ==========================================
# 4. ANA DÖNGÜ VE YAPAY ZEKA MANTIĞI
# ==========================================
while True:
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime

    current_thickness = eraser_thickness if current_color_name == "eraser" else brush_thickness

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w_cam), int(lm.y * h_cam)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                x1, y1 = lm_list[8][1:]  
                x2, y2 = lm_list[12][1:] 

                fingers = []
                fingers.append(1 if lm_list[4][2] < lm_list[5][2] else 0) 
                fingers.append(1 if lm_list[8][2] < lm_list[6][2] else 0) 
                fingers.append(1 if lm_list[12][2] < lm_list[10][2] else 0) 
                fingers.append(1 if lm_list[16][2] < lm_list[14][2] else 0) 

                # --- DİNAMİK FIRÇA ---
                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                    x_thumb, y_thumb = lm_list[4][1:]
                    length = math.hypot(x1 - x_thumb, y1 - y_thumb)
                    cx, cy = (x1 + x_thumb) // 2, (y1 + y_thumb) // 2

                    brush_thickness = int(np.interp(length, [30, 200], [5, 50]))
                    cv2.circle(frame, (cx, cy), brush_thickness, draw_color, cv2.FILLED)
                    cv2.circle(frame, (cx, cy), brush_thickness + 2, (255,255,255), 2, cv2.LINE_AA)
                    cv2.putText(frame, f"{brush_thickness}px", (cx+40, cy), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                    
                    xp, yp = 0, 0
                    is_drawing_shape = False

                # --- MOD 1: SEÇİM (İşaret ve Orta Havada) ---
                elif fingers[1] == 1 and fingers[2] == 1:
                    xp, yp = 0, 0
                    
                    if is_drawing_shape:
                        if current_tool == "rect":
                            cv2.rectangle(canvas, (shape_start_x, shape_start_y), (x1, y1), draw_color, current_thickness, cv2.LINE_AA)
                        elif current_tool == "circle":
                            radius = int(math.hypot(x1 - shape_start_x, y1 - shape_start_y))
                            cv2.circle(canvas, (shape_start_x, shape_start_y), radius, draw_color, current_thickness, cv2.LINE_AA)
                        is_drawing_shape = False

                    # Seçim İmleci
                    cv2.circle(frame, (x1, y1), 15, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.circle(frame, (x1, y1), 5, draw_color, cv2.FILLED)

                    buffer = 30 # Aim Assist
                    
                    # 1. Üst Menü
                    for name, coords in top_buttons.items():
                        if coords["x1"] - buffer < x1 < coords["x2"] + buffer and coords["y1"] - buffer < y1 < coords["y2"] + buffer:
                            if name == "clear":
                                canvas = np.zeros((h_cam, w_cam, 3), np.uint8)
                            else:
                                current_color_name = name
                                draw_color = colors[name]
                                
                    # 2. Sağ Menü
                    for t_name, coords in right_tools.items():
                        if coords["x1"] - buffer < x1 < coords["x2"] + buffer and coords["y1"] - buffer < y1 < coords["y2"] + buffer:
                            current_tool = t_name

                # --- MOD 2: ÇİZİM ---
                elif fingers[1] == 1 and fingers[2] == 0:
                    
                    # YENİ EKLENEN GÜVENLİ BÖLGE (SAFE ZONE) MANTIĞI:
                    # Parmak üst menüde (y < 130) veya sağ menüde (x > sağ_panel) ise çizim YAPMA!
                    is_in_safe_zone = (y1 > 130) and (x1 < right_panel_x1 - 20)

                    if current_color_name == "eraser":
                        cv2.circle(frame, (x1, y1), eraser_thickness, (255,255,255), 2, cv2.LINE_AA)
                        cv2.circle(frame, (x1, y1), 2, (255,255,255), cv2.FILLED)
                    else:
                        cv2.circle(frame, (x1, y1), current_thickness, draw_color, cv2.FILLED)

                    if is_in_safe_zone: # Sadece güvenli bölgedeysek çiz!
                        if current_tool == "free":
                            if xp == 0 and yp == 0:
                                xp, yp = x1, y1
                            cv2.line(frame, (xp, yp), (x1, y1), draw_color, current_thickness, cv2.LINE_AA)
                            cv2.line(canvas, (xp, yp), (x1, y1), draw_color, current_thickness, cv2.LINE_AA)
                            xp, yp = x1, y1
                            is_drawing_shape = False

                        elif current_tool == "rect":
                            if not is_drawing_shape:
                                shape_start_x, shape_start_y = x1, y1
                                is_drawing_shape = True
                            cv2.rectangle(frame, (shape_start_x, shape_start_y), (x1, y1), draw_color, current_thickness, cv2.LINE_AA)

                        elif current_tool == "circle":
                            if not is_drawing_shape:
                                shape_start_x, shape_start_y = x1, y1
                                is_drawing_shape = True
                            radius = int(math.hypot(x1 - shape_start_x, y1 - shape_start_y))
                            cv2.circle(frame, (shape_start_x, shape_start_y), radius, draw_color, current_thickness, cv2.LINE_AA)
                    else:
                        # Menüye girince çizgiyi kopar (arkaya çizilmesini engeller)
                        xp, yp = 0, 0
                        is_drawing_shape = False

    else:
        xp, yp = 0, 0
        is_drawing_shape = False

    # 1. ADIM: KAMERA VE TUVALİ BİRLEŞTİR
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask)
    final_frame = cv2.bitwise_or(frame_bg, canvas)

    # 2. ADIM: ARAYÜZÜ EN ÜSTE ÇİZ (Katmanlama Sihri)
    final_frame = draw_clean_ui(final_frame, current_color_name, current_tool, current_thickness)

    # FPS Metnine Gölge Eklendi (Okunabilirliği Artırmak İçin)
    cv2.putText(final_frame, f"FPS: {int(fps)}", (22, 42), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(final_frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow(window_name, final_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()