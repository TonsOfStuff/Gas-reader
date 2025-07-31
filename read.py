import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import csv
import tkinter as tk
from tkinter import ttk
import threading
import os



xData = []
yData = []

instance = 0
running = False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pressure Logger")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.page = MainPage(container, self)
        self.page.pack(fill="both", expand=True)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.label = tk.Label(self, text="Pressure (torr):", font=("Arial", 14))
        self.label.pack(pady=5)

        self.pressureLabel = tk.Label(self, text="N/A", font=("Arial", 18))
        self.pressureLabel.pack()

        self.startButton = tk.Button(self, text="Start", font=("Arial", 14), command=self.startPlot)
        self.startButton.pack()
        self.stopButton = tk.Button(self, text="Stop", font=("Arial", 14), command=self.stopPlot)
        self.stopButton.pack()

        #Figure
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.canvas.toolbar = None 

        #Restart data
        self.restartButton = tk.Button(self, text="Restart", font=("Arial", 14), command=self.restartData)
        self.restartButton.pack()

        self.saveButton = tk.Button(self, text="Save to CSV", font=("Arial", 14), command=self.writeCSV)
        self.saveButton.pack()

        self.ani = animation.FuncAnimation(self.fig, self.updatePlot)

    def startPlot(self):
        global running
        running = True
        self.startButton.config(state=tk.DISABLED)
        self.stopButton.config(state=tk.NORMAL)
        threading.Thread(target=self.logPlot, daemon=True).start()

    def stopPlot(self):
        global running
        running = False
        self.startButton.config(state=tk.NORMAL)
        self.stopButton.config(state=tk.DISABLED)


    def updatePlot(self, i):
        self.ax.clear()
        self.ax.plot(yData, xData, color='skyblue')
        self.ax.set_title("Live Pressure (torr)")
        self.ax.set_xlabel("Instance")
        self.ax.set_ylabel("Pressure")

    
    def logPlot(self):
        global instance

        ser = serial.Serial('COM3', 9600, timeout=1)
        while running:
            instance += 1
            
            ser.write(b'?V913\r')
            time.sleep(0.1)
            gaugePressureTorr = float(ser.read_all().decode().strip()[6:16])
            gaugePressure = gaugePressureTorr / 133.3
            print("Gauge 1 Pressure: ", gaugePressure)

            yData.append(instance)
            xData.append(gaugePressure)

            self.after(0, lambda: self.pressureLabel.config(text=str(gaugePressure) + " torr"))

        ser.close()
    
    def restartData(self):
        xData.clear()
        yData.clear()

        self.ax.clear()

    def writeCSV(self):
        with open("pressureLog.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Instance", "Pressure (torr)"])
            for instance, pressure in zip(yData, xData):
                writer.writerow([instance, pressure])




if __name__ == "__main__":
    root = App()
    root.mainloop()