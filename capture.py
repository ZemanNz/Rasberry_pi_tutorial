import cv2, os, time, argparse

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def capture_loop(output_dir):
    ensure_dir(output_dir)
    cap = cv2.VideoCapture(2)
    print("[INFO] Stiskni F pro uložení snímku, Q pro ukončení.")
    a= 0  # Counter for saved images
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Live", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('f'):  # F = save
            fname = f"{int(time.time())}.jpg"
            cv2.imwrite(os.path.join(output_dir, fname), frame)
            print(f"[SAVED] {fname}")
            a += 1
            print("ulozeno : ", a)

        if key == ord('q'):  # Q = quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dataset/raw_images",
                        help="Složka pro uložení snímků")
    args = parser.parse_args()
    capture_loop(args.output)
