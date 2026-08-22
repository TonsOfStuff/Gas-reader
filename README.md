# Gas Reader

Real-time pressure monitoring tool for a Thermal Ionization Cathode (TIC) gas gauge connected via a DAQ (data acquisition) unit, built for the same physics research setup as [Cryotweezer](https://github.com/TonsOfStuff/Cryotweezer) at Northwestern's [Geraci Lab](https://faculty.wcas.northwestern.edu/andrew-geraci/experiments.html).

## What this does
Reads live pressure data from a TIC gauge over USB via a DAQ interface and plots it in real time, letting researchers monitor vacuum/pressure conditions during an experiment without needing separate lab software.

## Stack
- **Python** — data acquisition and processing
- **Tkinter** — GUI
- **Matplotlib** — Live-updating pressure-vs-time plot

## How to run
1. Plug in the TIC gauge via USB to the DAQ
2. Run the executable (or `python gas_reader.py` from source)
3. Window will pop up, giving live pressure data

**Note:** If your antivirus flags or deletes the executable, add the folder as an exception

## Related
Built alongside [Cryotweezer](https://github.com/TonsOfStuff/Cryotweezer) for the same lab setup
