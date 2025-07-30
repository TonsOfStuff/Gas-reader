import serial
import time
import matplotlib.pyplot as plt;
import csv

ser = serial.Serial('COM3', 9600, timeout=1)

xData = []
yData = []

instance = 0

with open("pressureLog.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Instnace", "Pressure (torr)"])
    try:
        while True:
            instance += 1
            
            ser.write(b'?V913\r')
            time.sleep(0.1)
            gaugePressureTorr = float(ser.read_all().decode().strip()[6:16])
            gaugePressure = gaugePressureTorr / 133.3
            print("Gauge 1 Pressure: ", gaugePressure)

            yData.append(instance)
            xData.append(gaugePressure)

            writer.writerow([instance, gaugePressure])

            plt.clf()
            plt.plot(yData, xData, color='skyblue')
            plt.xlabel("Instance")
            plt.ylabel("Pressure (torr)")
            plt.title("Pressure")
            plt.pause(0.1)

    except KeyboardInterrupt:
        print("Stopped")

    finally:
        plt.show()
        ser.close()
