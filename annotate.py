

#  116 z 123 val





import cv2, os, glob

# Zmáčknutím levého tlačítka myši začni kreslit box,
# tažením + puštěním tlačítka ukonči a automaticky uloží koordináty.

classes = {
    ord('r'): 0,   # červená kostka
    ord('g'): 1,   # zelená kostka
    ord('b'): 2,   # modrá kostka
    ord('z'): 3,   # zone_red (červený čtverec)
}
class_names = ['cube_red','cube_green','cube_blue','zone_red']

IMG_DIR = 'dataset/images/val'   # nebo val
LBL_DIR = 'dataset/labels/val'   # odpovídající labels

os.makedirs(LBL_DIR, exist_ok=True)

current_img = None
boxes = []
current_class = None
drawing = False
ix, iy = -1, -1

def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, boxes, current_img
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1, x2, y2 = ix, iy, x, y
        # seřaď rohy
        x_min, x_max = sorted([x1, x2])
        y_min, y_max = sorted([y1, y2])
        boxes.append((current_class, x_min, y_min, x_max, y_max))
        cv2.rectangle(current_img, (x_min, y_min), (x_max, y_max), (0,255,0), 2)

cv2.namedWindow('Annotator')
cv2.setMouseCallback('Annotator', mouse_callback)

files = sorted(glob.glob(f"{IMG_DIR}/*.jpg"))
idx = 0

while 0 <= idx < len(files):
    img_path = files[idx]
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    current_img = img.copy()
    boxes = []
    print(f"\n[IMAGE {idx+1}/{len(files)}] {os.path.basename(img_path)}")
    print("Stiskni R/G/B/Z pro výběr třídy, kresli boxy, S = uložit & další, N = další bez uložení, P = předchozí, Q = konec")
    
    while True:
        disp = current_img.copy()
        if drawing:
            cv2.rectangle(disp, (ix, iy), cv2.getWindowImageRect('Annotator')[:2], (255,0,0), 1)
        cv2.imshow('Annotator', disp)
        key = cv2.waitKey(10) & 0xFF
        
        if key in classes:
            current_class = classes[key]
            print(f"> Třída setnuta na: {class_names[current_class]}")
        elif key == ord('s'):  # save
            # uložit YOLO txt
            txt_path = os.path.join(LBL_DIR, os.path.basename(img_path).replace('.jpg','.txt'))
            with open(txt_path, 'w') as f:
                for cls, x1,y1,x2,y2 in boxes:
                    # YOLO normalizace
                    x_c = (x1 + x2) / 2 / w
                    y_c = (y1 + y2) / 2 / h
                    bw = (x2 - x1) / w
                    bh = (y2 - y1) / h
                    f.write(f"{cls} {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}\n")
            print(f"[SAVED] {txt_path} ({len(boxes)} boxes)")
            idx += 1
            break
        elif key == ord('n'):  # next image, skip saving
            idx += 1
            break
        elif key == ord('p'):  # previous
            idx = max(0, idx-1)
            break
        elif key == ord('q'):  # quit
            idx = len(files)
            break

cv2.destroyAllWindows()
