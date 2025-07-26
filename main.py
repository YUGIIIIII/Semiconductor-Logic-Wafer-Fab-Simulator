import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

# ############################################################################
# PART 1: LOGIC GATE SIMULATION
# ############################################################################

def gate_and(a, b): return a and b
def gate_or(a, b): return a or b
def gate_not(a): return int(not a)
def gate_nand(a, b): return not (a and b)
def gate_nor(a, b): return not (a or b)
def gate_xor(a, b): return a ^ b

# ############################################################################
# PART 2: WAFER FABRICATION SIMULATION
# ############################################################################

class Wafer:
    def __init__(self, wafer_id):
        self.id = wafer_id
        self.layers = ['Silicon Substrate']
        self.current_step = 'Not Started'
        self.location = 'Stock'

    def __str__(self):
        layer_str = ' -> '.join(self.layers)
        return (
            f"Wafer ID: {self.id}\n"
            f"  Location: {self.location}\n"
            f"  Status: {self.current_step}\n"
            f"  Layers: {layer_str}"
        )

def process_deposition(wafer, material):
    wafer.layers.append(f'{material} Layer')
    wafer.current_step = f'Deposition of {material}'
    return f"Deposited {material} onto Wafer {wafer.id}."

def process_lithography(wafer):
    wafer.layers.append('Photoresist')
    wafer.current_step = 'Lithography (Patterned)'
    return f"Applied and patterned photoresist on Wafer {wafer.id}."

def process_etching(wafer):
    if len(wafer.layers) > 2:
        etched_layer = wafer.layers.pop(-2)
        wafer.layers.pop(-1)
        wafer.layers.append(f'Patterned {etched_layer.split(" ")[0]}')
        wafer.current_step = 'Etching Complete'
        return f"Etched {etched_layer} from Wafer {wafer.id} and stripped resist."
    else:
        return f"Skipped Etch on Wafer {wafer.id}: No material layer to etch."

def process_inspection(wafer):
    wafer.current_step = 'Quality Inspection'
    if random.random() < 0.15:  # 15% chance to fail
        return f"Wafer {wafer.id} FAILED quality inspection!"
    else:
        return f"Wafer {wafer.id} passed quality inspection."

# ############################################################################
# PART 3: MAIN APPLICATION UI
# ############################################################################

class SemiconductorSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Semiconductor Software Simulator")
        self.geometry("750x580")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=('Helvetica', 10, 'bold'))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        self.logic_gate_tab = ttk.Frame(self.notebook, padding="10")
        self.fab_sim_tab = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.logic_gate_tab, text='Logic Gate Simulator')
        self.notebook.add(self.fab_sim_tab, text='Wafer Fab Simulator')

        self.create_logic_gate_widgets()
        self.create_fab_sim_widgets()

    def create_logic_gate_widgets(self):
        main_frame = ttk.LabelFrame(self.logic_gate_tab, text="Inputs and Operations", padding=15)
        main_frame.pack(fill="x", expand=True)

        self.input_a = tk.IntVar(value=0)
        self.input_b = tk.IntVar(value=0)

        ttk.Checkbutton(main_frame, text="Input A", variable=self.input_a).grid(row=0, column=0, padx=10, pady=10)
        ttk.Checkbutton(main_frame, text="Input B", variable=self.input_b).grid(row=0, column=1, padx=10, pady=10)

        results_frame = ttk.LabelFrame(self.logic_gate_tab, text="Results", padding=15)
        results_frame.pack(fill="both", expand=True, pady=10)
        self.results_label = ttk.Label(results_frame, text="Click a gate to see the result.", font=('Courier', 12))
        self.results_label.pack()

        ttk.Button(main_frame, text="Test Gates", command=self.run_gate_simulation).grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        main_frame.grid_columnconfigure(2, weight=1)

    def create_fab_sim_widgets(self):
        control_frame = ttk.LabelFrame(self.fab_sim_tab, text="Control Panel", padding=10)
        control_frame.pack(fill="x", pady=5)

        ttk.Label(control_frame, text="Wafer ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.wafer_id_entry = ttk.Entry(control_frame)
        self.wafer_id_entry.insert(0, f"W-2025-{random.randint(1,99):02d}")
        self.wafer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(control_frame, text="▶ Run Fab Simulation", command=self.run_fab_simulation).grid(row=0, column=2, padx=10, pady=5)
        ttk.Button(control_frame, text="💾 Save Log to File", command=self.save_log_to_file).grid(row=0, column=3, padx=5, pady=5)
        control_frame.grid_columnconfigure(1, weight=1)

        log_frame = ttk.LabelFrame(self.fab_sim_tab, text="Fabrication Process Log", padding=10)
        log_frame.pack(fill="both", expand=True, pady=5)
        self.fab_log = scrolledtext.ScrolledText(log_frame, height=20, font=('Courier', 10), wrap=tk.WORD)
        self.fab_log.pack(fill="both", expand=True)
        self.fab_log.config(state='disabled')

    def run_gate_simulation(self):
        a = self.input_a.get()
        b = self.input_b.get()

        result_text = (
            f"Inputs: A={a}, B={b}\n"
            f"--------------------\n"
            f"  A AND B  = {int(gate_and(a, b))}\n"
            f"   A OR B  = {int(gate_or(a, b))}\n"
            f"    NOT A  = {int(gate_not(a))}\n"
            f" A NAND B  = {int(gate_nand(a, b))}\n"
            f"  A NOR B  = {int(gate_nor(a, b))}\n"
            f"  A XOR B  = {int(gate_xor(a, b))}"
        )
        self.results_label.config(text=result_text)

    def run_fab_simulation(self):
        wafer_id = self.wafer_id_entry.get().strip()
        if not wafer_id:
            messagebox.showwarning("Input Error", "Please enter a Wafer ID.")
            return

        self.fab_log.config(state='normal')
        self.fab_log.delete('1.0', tk.END)

        wafer = Wafer(wafer_id)
        self.log_message("--- Simulation Started ---")
        self.log_message(str(wafer))

        materials = ['Silicon Dioxide', 'Polysilicon', 'Silicon Nitride', 'Tungsten', 'Aluminum']
        process_flow = []

        for i in range(2):
            material = random.choice(materials)
            process_flow.extend([
                {'step': process_deposition, 'params': {'material': material}, 'location': f'Deposition Bay {i+1}'},
                {'step': process_lithography, 'params': {}, 'location': 'Lithography Bay'},
                {'step': process_etching, 'params': {}, 'location': f'Etch Bay {i+1}'},
                {'step': process_inspection, 'params': {}, 'location': 'Metrology Lab'},
            ])

        for i, process in enumerate(process_flow):
            self.log_message(f"\n--- Step {i+1}: {process['step'].__name__.replace('process_', '').capitalize()} ---")
            wafer.location = process['location']
            self.log_message(f"Moving wafer to: {wafer.location}")
            log_entry = process['step'](wafer, **process['params'])
            self.log_message(f"Action: {log_entry}")
            self.log_message(str(wafer))

        wafer.location = 'Finished Goods Inventory'
        wafer.current_step = 'Process Complete'
        self.log_message("\n--- Simulation Finished ---")
        self.log_message(str(wafer))

        self.fab_log.config(state='disabled')

    def log_message(self, message):
        self.fab_log.insert(tk.END, message + "\n")
        self.fab_log.see(tk.END)

    def save_log_to_file(self):
        content = self.fab_log.get('1.0', tk.END).strip()
        if not content:
            messagebox.showinfo("No Log", "There is no log to save.")
            return

        filename = f"{self.wafer_id_entry.get()}_log.txt"
        try:
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Log saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {e}")

if __name__ == "__main__":
    app = SemiconductorSimulatorApp()
    app.mainloop()
