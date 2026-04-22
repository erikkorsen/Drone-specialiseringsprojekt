import cv2
import webbrowser
import qrcode


def scanQR():
    Key = "dronePassword"
    cap = cv2.VideoCapture(0)

    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        
        data, bbox, _ = detector.detectAndDecode(img)

        if data:
            a = data
            break

        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    return (a == Key)

def generateQRObject(data):
    qrCode = qrcode.QRCode()
    qrcode.add_data(data)
    return qrcode

def generateImage(QRCode):
    image = QRCode.make_image(fill_color = "Black", back_color = "White")
    return image

if scanQR():
    print("Code works!!!!")
else:
    print("Fail")