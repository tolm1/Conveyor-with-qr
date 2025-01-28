import tkinter
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import serial

rob = {"data1":0,"data2":0}
n = 2

window = tkinter.Tk()

window.geometry("200x200")

#arduino = serial.Serial('COM3', 9600,timeout=1)
arduino=serial.Serial()
arduino.port = "COM3"
arduino.baudrate = 9600
arduino.timeout = 1
arduino.setDTR(False)
#arduinoSerialData.setRTS(False)
arduino.open()


time.sleep(2)

#arduino.reset_input_buffer()

def click_but(event):
    n = int(entry.get())

    found = set()
    vs = VideoStream(src=1).start()#устанавливаем с какой камеры читаем даныне
    vs2 = VideoStream(src=2).start()
    print(n)
    while True:
        if (rob["data1"] == 0 or rob["data2"] == 0):
            found.clear()
            #print("to")
            while True:
                frame1 = vs.read()#начинаем читаь
                frame2 = vs2.read()

                frame1 = imutils.resize(frame1, width=400)#изменение размера
                frame2 = imutils.resize(frame2, width=400)
                barcodes1 = pyzbar.decode(frame1)
                barcodes2 = pyzbar.decode(frame2)
                for barcode in barcodes1:
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeData = int(barcodeData)
                    if barcodeData not in found:
                        found.clear()
                        found.add(barcodeData)
                        if (barcodeData not in rob):
                            rob["data1"] = barcodeData#нижний
                        #print(barcodeData)

                for barcode2 in barcodes2:
                    barcodeData2 = barcode2.data.decode("utf-8")
                    barcodeData2 = int(barcodeData2)
                    if barcodeData2 not in found:
                        found.clear()
                        found.add(barcodeData2)
                        if (barcodeData2 not in rob):
                            rob["data2"] = int(barcodeData2)#верхний
                        #print(barcodeData2)
                if (len(rob) == n):
                    print(1, rob)
                    break
        if (len(rob) == n):
            break

    cv2.destroyAllWindows()
    vs.stop()

def hell(event):
    arduino.write(b'3')

    datafromUser = 0

    vs = VideoStream(src=0).start()

    found = set()
    _ = 0


    son = list(rob.keys())

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y

                                          + h), (0, 255, 0), 2)
            barcodeData = barcode.data.decode("utf-8")
            cv2.putText(frame, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if time.time() - _ > 21:
                _ = found.clear()
                _ = 0
            if barcodeData not in found and time.time() - _ > 21:

                found.clear()
                found.add(barcodeData)
                barcodeData = int(barcodeData)
                print(barcodeData)

                if (barcodeData == int(rob["data1"])):
                    datafromUser = "1"
                    arduino.write(b'1')
                    time.sleep(0.005)
                    _ = time.time()
                if (barcodeData == int(rob["data2"])):
                    datafromUser = "2"
                    arduino.write(b'2')
                    time.sleep(0.005)
                    _ = time.time()

        cv2.imshow("SORT", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            arduino.write(b'f')
            print("finish")
            break

    cv2.destroyAllWindows()
    vs.stop()

but = tkinter.Button(window,text="данные")
but.bind("<Button-1>",click_but)
but.pack()

but3 = tkinter.Button(window,text="сортировка")
but3.bind("<Button-1>",hell)
but3.pack()

def how():
    n = entry.get()
    print(n)
    #print(type(n))

entry = tkinter.Entry(width=40, bg="white", fg="black")
entry.pack()

but1 = tkinter.Button(window,text="количетсво грузов",command=how)
but1.pack()

print(entry.get())

window.mainloop()
