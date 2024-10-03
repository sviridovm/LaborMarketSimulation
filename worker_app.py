import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk
import constants


class WorkerApp:
    def __init__(self, root, workers):
        self.root = root
        self.root.title("Worker Salary Dashboard")
        self.workers = workers

        # Create Treeview
        self.tree = ttk.Treeview(root, columns=(
            'ID', 'Education Level', 'Salary'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Education Level', text='Education Level')
        self.tree.heading('Salary', text='Salary')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create a frame for buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(fill=tk.X)

        # Canvas to display plots
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Update Treeview with worker data
        self.update_treeview()

        self.avg_salary_button = tk.Button(
            self.buttons_frame, text='Show Average Salaries by Education Level', command=self.plot_avg_salaries)
        self.avg_salary_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_worker_select)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for worker in self.workers:
            self.tree.insert('', tk.END, iid=worker.id, values=(
                worker.id, worker.education_level.name, f'${int(worker.salary_history[-1])}'))

    def calculate_average_salaries(self):
        avg_salaries = {}
        salaries_by_edu = {edu: [] for edu in constants.education}

        for worker in self.workers:
            # if worker.education_level not in salaries_by_edu:
            # salaries_by_edu[worker.education_level] = []
            salaries_by_edu[worker.education_level].append(
                worker.salary_history[-1])

        for edu_level, salaries in salaries_by_edu.items():
            avg_salaries[edu_level] = np.mean(salaries)

        return avg_salaries

    def on_worker_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        worker_id = self.tree.item(selected_item[0])['values'][0]

        worker = next(w for w in self.workers if w.id == worker_id)

        # Clear previous plot
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Plot salary history for the selected worker
        self.plot_salary_history(worker)

    def plot_salary_history(self, worker):
        plt.close('all')  # Close any existing figures
        plt.figure(figsize=(10, 5))
        times = range(len(worker.salary_history))
        plt.plot(times, worker.salary_history,
                 marker='o', label=f'Worker {worker.id}')
        plt.xlabel('Time')
        plt.ylabel('Salary')
        plt.title(f'Salary History for Worker {worker.id}')
        plt.legend()
        plt.grid(True)

        # Display the plot in Tkinter window
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def plot_avg_salaries(self):
        avg_salaries = self.calculate_average_salaries()

        plt.close('all')  # Close any existing figures
        plt.figure(figsize=(10, 5))

        # Extract keys and values
        edu_levels = [edu.name for edu in avg_salaries.keys()]
        salaries = [salary for salary in avg_salaries.values()]

        # Create bar plot
        plt.bar(edu_levels, salaries, color='skyblue')
        plt.xlabel('Education Level')
        plt.ylabel('Average Salary')
        plt.title('Average Salary by Education Level')
        # Rotate labels for better readability
        plt.xticks(ha='center')
        plt.grid(True)

        # Clear previous canvas if exists
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Display the plot in Tkinter window
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def on_close(self):
        self.root.quit()  # Stops the Tkinter mainloop
        self.root.destroy()  # Destroys the Tkinter window
