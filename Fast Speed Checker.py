import tkinter as tk
import threading
import speedtest
from datetime import datetime

class FastSpeedChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fast Speed Checker")
        self.configure(bg="#0d1117")
        self.geometry("400x500")
        self.resizable(False, False)

        tk.Label(self, text="Fast Speed Checker", fg="white", bg="#0d1117",
                 font=("Helvetica", 16, "bold")).pack(pady=15)

       
        self.speed_label = tk.Label(self, text="0", fg="white", bg="#0d1117",
                                    font=("Helvetica", 56, "bold"))
        
        self.speed_label.pack(pady=10)
        tk.Label(self, text="Mbps (Download)", fg="#a3a3a3", bg="#0d1117",
                 font=("Helvetica", 14)).pack()

        
        self.ping_label = tk.Label(self, text="Ping: -- ms", fg="#8b949e", bg="#0d1117", font=("Helvetica", 12))
        self.ping_label.pack(pady=10)
        self.upload_label = tk.Label(self, text="Upload: -- Mbps", fg="#8b949e", bg="#0d1117", font=("Helvetica", 12))
        self.upload_label.pack()

        
        self.status = tk.Label(self, text="Press START to begin", fg="#58a6ff",
                               bg="#0d1117", font=("Helvetica", 11))
        self.status.pack(pady=20)

        
        self.start_btn = tk.Button(self, text="START TEST", command=self.start_test,
                                   bg="#238636", fg="white", font=("Helvetica", 13, "bold"),
                                   activebackground="#2ea043", width=14)
        self.start_btn.pack(pady=10)

        tk.Label(self, text="Made by Debmalya Dutta Teertha", fg="#666", bg="#0d1117",
                 font=("Helvetica", 9)).pack(side="bottom", pady=10)

    def start_test(self):
        """Run speed test in background thread so UI doesn’t freeze."""
        self.start_btn.config(state="disabled")
        self.status.config(text="Testing... please wait", fg="#facc15")
        self.speed_label.config(text="0")
        threading.Thread(target=self.run_speedtest, daemon=True).start()

    def run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            ping = st.results.ping
            self.update_label(self.ping_label, f"Ping: {ping:.0f} ms")

            self.status.config(text="Measuring download speed...", fg="#facc15")
            download = st.download() / 1_000_000
            self.update_label(self.speed_label, f"{download:.1f}")

            self.status.config(text="Measuring upload speed...", fg="#facc15")
            upload = st.upload() / 1_000_000
            self.update_label(self.upload_label, f"Upload: {upload:.1f} Mbps")

            self.status.config(text="✅ Test Complete", fg="#10b981")
            self.start_btn.config(state="normal")

        except Exception as e:
            self.status.config(text=f"❌ Error: {e}", fg="#ef4444")
            self.start_btn.config(state="normal")

    def update_label(self, label, text):
        """Update label safely from thread."""
        self.after(0, lambda: label.config(text=text))


if __name__ == "__main__":
    app = FastSpeedChecker()
    app.mainloop()
