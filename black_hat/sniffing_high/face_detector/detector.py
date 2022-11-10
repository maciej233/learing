import cv2
import os

PICTUTES = '/home/maciej/learing/black_hat/sniffing_high/face_detector/pictures'
FACES = '/home/maciej/learing/black_hat/sniffing_high/face_detector/faces'
TRAINS = '/home/maciej/learing/black_hat/sniffing_high/face_detector/trains'

def detect(source_dir=PICTUTES, target_dir=FACES, train_dir=TRAINS):
    for fname in os.listdir(source_dir):
        if not fname.upper().endswith('.JPG') == '.JPG':
            continue
        fullname = os.path.join(source_dir, fname)
        newname = os.path.join(target_dir, fname)
        img = cv2.imread(fullname)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_dir, "haarcascade_frontalface_alt.xml")
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            if rects.any():
                print("got Face!")
                rects[:,2:] += rects[:, :2]
        except AttributeError:
            print(f"No face found {fname}")
            continue

        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y2), (17, 255, 0), 2)
        cv2.imwrite(newname, img)

if __name__ == "__main__":
    detect()
