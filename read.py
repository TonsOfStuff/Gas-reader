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



xData = [] #X-axis data plotting every instance
yData = [] #Y-axis data plotting pressure values in torr

instance = 0 #The number of instances of checking the pressure value on the device
running = False #A flag used within the loop to start and stop

class App(tk.Tk): #Main app object that contains the pages
    def __init__(self):
        super().__init__()
        self.title("Pressure Logger")

        container = tk.Frame(self) #Create a Frame object to add Matplotlib graph inside
        container.pack(fill="both", expand=True)

        self.page = MainPage(container, self) #MainPage object referenced here, to add more pages, simply do the same for the others
        self.page.pack(fill="both", expand=True)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        #Create labels, buttons, etc for TKinter GUI
        self.label = tk.Label(self, text="Pressure (torr):", font=("Arial", 14))
        self.label.pack(pady=5)

        self.pressureLabel = tk.Label(self, text="N/A", font=("Arial", 18))
        self.pressureLabel.pack()

        self.startButton = tk.Button(self, text="Start", font=("Arial", 14), command=self.startPlot)
        self.startButton.pack()
        self.stopButton = tk.Button(self, text="Stop", font=("Arial", 14), command=self.stopPlot)
        self.stopButton.pack()

        #Figure, adjust size with figsize
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.canvas.toolbar = None 

        #Restart data GUI
        self.restartButton = tk.Button(self, text="Restart", font=("Arial", 14), command=self.restartData)
        self.restartButton.pack()

        #Save data into CSV of fluctuating pressure
        self.saveButton = tk.Button(self, text="Save to CSV", font=("Arial", 14), command=self.writeCSV)
        self.saveButton.pack()

        #Main animation loop, built-in method from Matplotlib
        self.ani = animation.FuncAnimation(self.fig, self.updatePlot, interval = 200)

    def startPlot(self): #Method run by the start button
        global running
        running = True
        self.startButton.config(state=tk.DISABLED)
        self.stopButton.config(state=tk.NORMAL)
        threading.Thread(target=self.logPlot, daemon=True).start() #Threading so that things can be run in parallel

    def stopPlot(self): #Method run by the stop button
        global running
        running = False #Sets running to false which is read and then stops the loop
        self.startButton.config(state=tk.NORMAL)
        self.stopButton.config(state=tk.DISABLED)


    def updatePlot(self, i): #Updates the plot with live data
        self.ax.clear()
        self.ax.plot(yData, xData, color='skyblue')
        self.ax.set_title("Live Pressure (torr)")
        self.ax.set_xlabel("Instance")
        self.ax.set_ylabel("Pressure")

    
    def logPlot(self): #Master loop that connects to the pressure reader
        global instance

        ser = serial.Serial('COM3', 9600, timeout=1) #Connection here
        while running:
            instance += 1
            
            ser.write(b'?V913\r') #Writes to the device with built-in command that takes the pressure value in Pa
            time.sleep(0.1)
            gaugePressureTorr = float(ser.read_all().decode().strip()[6:16])
            gaugePressure = gaugePressureTorr / 133.3 #Conversion from Pa to Torr
            #print("Gauge 1 Pressure: ", gaugePressure)

            yData.append(instance)
            xData.append(gaugePressure)

            self.after(0, lambda: self.pressureLabel.config(text=str(gaugePressure) + " torr")) #Using after due to threading issues

        ser.close() #Close the connection when the loop ends
    
    def restartData(self): #Clears existing data on the graph
        xData.clear()
        yData.clear()

        self.ax.clear()

    def writeCSV(self): #Creates a CSV file with yData and xData
        with open("pressureLog.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Instance", "Pressure (torr)"])
            for instance, pressure in zip(yData, xData):
                writer.writerow([instance, pressure])




if __name__ == "__main__": #Main loop, used for running things in parallel
    root = App()
    root.mainloop() #TKinter function that runs everything