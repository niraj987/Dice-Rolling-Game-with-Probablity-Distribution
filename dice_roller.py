import tkinter as tk
from tkinter import ttk
import random


class DiceRoller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎲 Ultimate Dice Roller")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)

        # Variables
        self.num_dice_var = tk.IntVar(value=2)
        self.sides_var = tk.IntVar(value=6)
        self.history = []

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4")

        self.create_ui()

    def create_ui(self):
        # ====================== HEADER ======================
        header = tk.Frame(self.root, bg="#1e1e2e")
        header.pack(fill="x", pady=20)

        title = tk.Label(header, text="🎲 ULTIMATE DICE ROLLER", 
                        font=("Helvetica", 28, "bold"), 
                        fg="#89b4fa", bg="#1e1e2e")
        title.pack()

        subtitle = tk.Label(header, text="Roll like a pro • D&D • Tabletop • Fun", 
                           font=("Helvetica", 12), fg="#a6adc8", bg="#1e1e2e")
        subtitle.pack()

        # ====================== CONTROLS ======================
        controls = tk.Frame(self.root, bg="#1e1e2e")
        controls.pack(pady=15)

        # Number of dice
        tk.Label(controls, text="Number of Dice:", font=("Helvetica", 14), 
                fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, padx=15, sticky="e")
        spin = ttk.Spinbox(controls, from_=1, to=20, width=5, 
                          textvariable=self.num_dice_var, font=("Helvetica", 14))
        spin.grid(row=0, column=1, padx=10)

        # Sides
        tk.Label(controls, text="Dice Type:", font=("Helvetica", 14), 
                fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=2, padx=15, sticky="e")
        sides_menu = ttk.OptionMenu(controls, self.sides_var, 6, 4, 6, 8, 10, 12, 20, 100)
        sides_menu.config(width=8)
        sides_menu.grid(row=0, column=3, padx=10)

        # Roll button
        roll_btn = ttk.Button(controls, text="ROLL THE DICE! 🎲", 
                             command=self.roll_dice, style="TButton")
        roll_btn.grid(row=0, column=4, padx=30)

        # Quick roll buttons
        quick_frame = tk.Frame(self.root, bg="#1e1e2e")
        quick_frame.pack(pady=10)

        quick_dice = [
            ("1d4", 1, 4), ("1d6", 1, 6), ("1d8", 1, 8),
            ("1d10", 1, 10), ("1d12", 1, 12), ("1d20", 1, 20),
            ("2d6", 2, 6), ("3d6", 3, 6), ("4d6", 4, 6), ("1d100", 1, 100)
        ]

        for text, num, sides in quick_dice:
            btn = ttk.Button(quick_frame, text=text, width=8,
                            command=lambda n=num, s=sides: self.quick_roll(n, s))
            btn.pack(side="left", padx=4)

        # ====================== DICE DISPLAY ======================
        self.dice_container = tk.Frame(self.root, bg="#1e1e2e")
        self.dice_container.pack(pady=30, fill="both", expand=True)

        # Total display
        self.total_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.total_frame.pack(pady=10)

        self.total_label = tk.Label(self.total_frame, text="TOTAL: 0", 
                                   font=("Helvetica", 48, "bold"), 
                                   fg="#f9e2af", bg="#1e1e2e")
        self.total_label.pack()

        # ====================== HISTORY ======================
        history_frame = tk.LabelFrame(self.root, text=" Roll History ", 
                                    font=("Helvetica", 12, "bold"),
                                    fg="#cba6f7", bg="#1e1e2e", bd=2)
        history_frame.pack(fill="both", expand=True, padx=40, pady=10)

        self.history_text = tk.Text(history_frame, height=12, bg="#313244", 
                                   fg="#cdd6f4", font=("Consolas", 11), 
                                   relief="flat", padx=10, pady=10)
        self.history_text.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", 
                                 command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set)

        # Clear history button
        clear_btn = ttk.Button(self.root, text="Clear History", 
                              command=self.clear_history)
        clear_btn.pack(pady=8)

    def draw_die(self, canvas, value, sides):
        """Draw a beautiful die on the canvas"""
        canvas.delete("all")
        
        # Die body with nice shadow
        canvas.create_rectangle(8, 8, 92, 92, fill="#f9e2af", outline="#11111b", width=6)
        canvas.create_rectangle(12, 12, 88, 88, fill="#fff", outline="#1e1e2e", width=3)
        
        if sides == 6 and 1 <= value <= 6:
            # Classic pips for d6
            positions = {
                1: [(50, 50)],
                2: [(30, 30), (70, 70)],
                3: [(30, 30), (50, 50), (70, 70)],
                4: [(30, 30), (30, 70), (70, 30), (70, 70)],
                5: [(30, 30), (30, 70), (50, 50), (70, 30), (70, 70)],
                6: [(30, 30), (30, 50), (30, 70), (70, 30), (70, 50), (70, 70)]
            }
            
            pip_color = "#11111b"
            for x, y in positions[value]:
                canvas.create_oval(x-14, y-14, x+14, y+14, fill=pip_color, outline="#000")
        else:
            # Big number for other dice
            font_size = 52 if value < 10 else 42
            canvas.create_text(50, 50, text=str(value), 
                             font=("Helvetica", font_size, "bold"), 
                             fill="#11111b")

    def animate_roll(self, frame, num_dice, sides, max_frames=12):
        """Smooth rolling animation"""
        if frame < max_frames:
            # Show random values during animation
            temp_rolls = [random.randint(1, sides) for _ in range(num_dice)]
            
            for i, canvas in enumerate(self.dice_canvases):
                self.draw_die(canvas, temp_rolls[i], sides)
            
            # Schedule next frame
            self.root.after(45, lambda: self.animate_roll(frame + 1, num_dice, sides, max_frames))
        else:
            # Final roll
            self.final_rolls = [random.randint(1, sides) for _ in range(num_dice)]
            
            for i, canvas in enumerate(self.dice_canvases):
                self.draw_die(canvas, self.final_rolls[i], sides)
            
            total = sum(self.final_rolls)
            self.total_label.config(text=f"TOTAL: {total}")
            
            # Add to history
            roll_str = f"→ {num_dice}d{sides} → {self.final_rolls} = {total}"
            self.history.append(roll_str)
            self.update_history()

    def roll_dice(self):
        """Main roll function"""
        num_dice = self.num_dice_var.get()
        sides = self.sides_var.get()
        
        # Clear old dice
        for widget in self.dice_container.winfo_children():
            widget.destroy()
        
        # Create new dice canvases
        self.dice_canvases = []
        cols = min(num_dice, 6)  # max 6 per row
        for i in range(num_dice):
            canvas = tk.Canvas(self.dice_container, width=110, height=110, 
                             bg="#1e1e2e", highlightthickness=0)
            row = i // cols
            col = i % cols
            canvas.grid(row=row, column=col, padx=12, pady=12)
            self.dice_canvases.append(canvas)
        
        # Start animation
        self.animate_roll(0, num_dice, sides)

    def quick_roll(self, num, sides):
        """Quick preset rolls"""
        self.num_dice_var.set(num)
        self.sides_var.set(sides)
        self.roll_dice()

    def update_history(self):
        """Update history text widget"""
        self.history_text.delete(1.0, tk.END)
        for entry in self.history[-15:]:  # keep last 15
            self.history_text.insert(tk.END, entry + "\n\n")

    def clear_history(self):
        """Clear roll history"""
        self.history.clear()
        self.history_text.delete(1.0, tk.END)


if __name__ == "__main__":
    app = DiceRoller()
    app.root.mainloop()