import tkinter as tk
# Make sure to adjust import based on your file structure
from labor_market import LaborMarket
from worker_app import WorkerApp  # Same here


def main():
    # Example initialization of the LaborMarket
    working_population = 100
    labor_market = LaborMarket(working_population)
    labor_market.match()

    # Create the Tkinter root window
    root = tk.Tk()

    workers = labor_market.workers

    # Pass the generated workers to WorkerApp
    app = WorkerApp(root, workers)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
