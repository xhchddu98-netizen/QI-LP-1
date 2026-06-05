import tkinter as tk
import hashlib

class ExclusionBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exclusion Box - Zero Trust")
        self.root.geometry("450x450")
        self.root.configure(padx=10, pady=10)
        self.whitelist = set()

        self.wl_frame = tk.Frame(root)
        self.wl_frame.pack(fill=tk.X, pady=(0, 10))
        self.wl_entry = tk.Entry(self.wl_frame, font=("Consolas", 11))
        self.wl_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Button(self.wl_frame, text="写入信任特征", command=self.add_trust).pack(side=tk.RIGHT)

        self.wl_listbox = tk.Listbox(root, height=6, font=("Consolas", 10))
        self.wl_listbox.pack(fill=tk.X, pady=(0, 20))

        self.test_frame = tk.Frame(root)
        self.test_frame.pack(fill=tk.X, pady=(0, 10))
        self.test_entry = tk.Entry(self.test_frame, font=("Consolas", 11))
        self.test_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        tk.Button(self.test_frame, text="信息注入测试", command=self.process_data).pack(side=tk.RIGHT)

        self.log = tk.Text(root, state=tk.DISABLED, font=("Consolas", 10), bg="#f4f4f4")
        self.log.pack(fill=tk.BOTH, expand=True)

    def add_trust(self):
        data = self.wl_entry.get().strip()
        if data:
            fingerprint = hashlib.md5(data.encode()).hexdigest()[:12]
            self.whitelist.add(fingerprint)
            self.wl_listbox.insert(tk.END, f" {fingerprint} | {data}")
            self.wl_entry.delete(0, tk.END)

    def process_data(self):
        data = self.test_entry.get().strip()
        if data:
            fingerprint = hashlib.md5(data.encode()).hexdigest()[:12]
            if fingerprint in self.whitelist:
                self.append_log(f"[ 放行 ] {fingerprint} <- {data}")
            else:
                self.append_log(f"[ 排斥 ] {fingerprint} <- {data}")
            self.test_entry.delete(0, tk.END)

    def append_log(self, msg):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExclusionBoxApp(root)
    root.mainloop()