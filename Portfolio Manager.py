import tkinter as tk
from math import pi, cos, sin

class Trade:
    def __init__(self, instrument, quantity):
        self.instrument = instrument
        self.quantity = quantity

class TradeJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Journal")
        self.root.configure(bg="black")

        self.trades = []
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="black")
        self.canvas.pack()

        self.load_trades()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Instrument:", bg="black", fg="white").pack()
        self.instrument_entry = tk.Entry(self.root)
        self.instrument_entry.pack()
        tk.Label(self.root, text="Quantity:", bg="black", fg="white").pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        self.add_trade_button = tk.Button(self.root, text="Trade hinzufügen", command=self.add_trade, bg="black", fg="white")
        self.add_trade_button.pack()

        self.plot_button = tk.Button(self.root, text="Trades plotten", command=self.plot_trades, bg="black", fg="white")
        self.plot_button.pack()

        self.clear_button = tk.Button(self.root, text="Alle Trades löschen", command=self.clear_trades, bg="black", fg="white")
        self.clear_button.pack()

    def add_trade(self):
        instrument = self.instrument_entry.get()
        quantity = int(self.quantity_entry.get())
        trade = Trade(instrument, quantity)
        self.trades.append(trade)
        self.save_trades()

    def plot_trades(self):
        self.canvas.delete("all")
        total_quantity = sum(trade.quantity for trade in self.trades)
        start_angle = 0
        for trade in self.trades:
            angle = 360 * trade.quantity / total_quantity
            self.draw_arc(start_angle, start_angle + angle, trade.quantity, trade.instrument)
            start_angle += angle

    def draw_arc(self, start_angle, end_angle, quantity, instrument):
        x = 200
        y = 150
        radius = 100
        start_x = x + radius * cos(start_angle * pi / 180)
        start_y = y - radius * sin(start_angle * pi / 180)
        end_x = x + radius * cos(end_angle * pi / 180)
        end_y = y - radius * sin(end_angle * pi / 180)
        self.canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=start_angle, extent=end_angle - start_angle, fill="blue")
        text_x = x + (radius + 20) * cos((start_angle + end_angle) / 2 * pi / 180)
        text_y = y - (radius + 20) * sin((start_angle + end_angle) / 2 * pi / 180)
        self.canvas.create_text(text_x, text_y, text=f"{instrument}: {quantity}", fill="white")

    def clear_trades(self):
        self.trades = []
        self.instrument_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.canvas.delete("all")
        self.save_trades()

    def save_trades(self):
        with open("trades.txt", "w") as f:
            for trade in self.trades:
                f.write(f"{trade.instrument},{trade.quantity}\n")

    def load_trades(self):
        try:
            with open("trades.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        instrument, quantity = parts
                        self.trades.append(Trade(instrument, int(quantity)))
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = TradeJournalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


