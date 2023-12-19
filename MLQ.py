import heapq
import random
import tkinter as tk
from tkinter import ttk

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0

    def __lt__(self, other):
        return self.priority < other.priority

class MultilevelQueue:
    def __init__(self, num_queues):
        self.queues = [[] for _ in range(num_queues)]
        self.time_quantum = 2  # Time quantum for each queue
        self.clock = 0

    def add_process(self, process):
        self.queues[process.priority].append(process)

    def run_scheduler(self):
        while any(queue for queue in self.queues):  # Continue until all queues are empty
            for i, queue in enumerate(self.queues):
                if queue:
                    current_process = heapq.heappop(queue)
                    self.update_ui(f"Clock: {self.clock}, Running Process: P{current_process.pid}, Priority: {current_process.priority}")
                    current_process.waiting_time += self.clock - current_process.arrival_time

                    if len(queue) == 0 and current_process.priority < len(self.queues) - 1:
                        current_process.priority += 1  # Increase priority if the queue is empty

                    if current_process.burst_time > self.time_quantum:
                        current_process.burst_time -= self.time_quantum
                        self.clock += self.time_quantum
                        current_process.arrival_time = self.clock
                        heapq.heappush(self.queues[current_process.priority], current_process)
                    else:
                        self.clock += current_process.burst_time
                        current_process.burst_time = 0

                    self.update_table(current_process)

    def update_ui(self, message):
        result_text.insert(tk.END, message + "\n")
        result_text.see(tk.END)

    def update_table(self, process):
        process_data = [f"P{process.pid}", process.arrival_time, process.priority,
                        process.burst_time, process.waiting_time]
        result_table.insert("", "end", values=process_data)

def run_simulation():
    result_text.delete(1.0, tk.END)
    result_table.delete(*result_table.get_children())

    num_queues = 3
    scheduler = MultilevelQueue(num_queues)

    # Get manual input for processes
    num_processes = int(num_processes_entry.get())
    processes = []
    for pid in range(num_processes):
        arrival_time = int(arrival_entry.get())
        burst_time = int(burst_entry.get())
        priority = int(priority_entry.get())
        process = Process(pid, arrival_time, burst_time, priority)
        scheduler.add_process(process)
        processes.append(process)

    scheduler.run_scheduler()

    total_waiting_time = sum(process.waiting_time for process in processes)
    average_waiting_time = total_waiting_time / num_processes

    result_text.insert(tk.END, f"\nAverage Waiting Time: {average_waiting_time:.2f}\n")
    result_text.see(tk.END)

# GUI
root = tk.Tk()
root.title("Multilevel Queue CPU Scheduling Simulation")

# Input fields for manual entry
num_processes_label = ttk.Label(root, text="Number of Processes:")
num_processes_label.pack(pady=5)
num_processes_entry = ttk.Entry(root)
num_processes_entry.pack(pady=5)

arrival_label = ttk.Label(root, text="Arrival Time:")
arrival_label.pack(pady=5)
arrival_entry = ttk.Entry(root)
arrival_entry.pack(pady=5)

burst_label = ttk.Label(root, text="Burst Time:")
burst_label.pack(pady=5)
burst_entry = ttk.Entry(root)
burst_entry.pack(pady=5)

priority_label = ttk.Label(root, text="Priority:")
priority_label.pack(pady=5)
priority_entry = ttk.Entry(root)
priority_entry.pack(pady=5)

# Text widget for general messages
result_text = tk.Text(root, wrap=tk.WORD, height=10, width=60)
result_text.pack(padx=10, pady=5)

# Treeview widget for the result table
columns = ["Process", "Arrival Time", "Priority", "Burst Time", "Waiting Time"]
result_table = ttk.Treeview(root, columns=columns, show="headings")

# Configure column headings
for col in columns:
    result_table.heading(col, text=col)
    result_table.column(col, width=80, anchor=tk.CENTER)

result_table.pack(padx=10, pady=5)

# Run Simulation button
run_button = ttk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=10)

root.mainloop()
