import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import requests
import time
import random
import queue
import os
from random import shuffle
from fake_useragent import UserAgent
from streamlink import Streamlink
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Proxy Scraper Sources ───────────────────────────────────────────────────

PROXY_SOURCES = {
    "http": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeworken/proxies/main/proxies.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/https.txt",
    ],
    "socks4": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/socks4.txt",
    ],
    "socks5": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/socks5.txt",
    ],
}

PROXY_TYPE_OPTIONS = ["All", "HTTP/HTTPS", "SOCKS4", "SOCKS5"]

PROXIES_DIR = "Proxies_txt"
GOOD_PROXY_FILE = os.path.join(PROXIES_DIR, "good_proxy.txt")
SCRAPED_PROXY_FILE = os.path.join(PROXIES_DIR, "scraped_proxies.txt")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Twitch Viewer Bot")
        self.geometry("900x700")
        self.configure(bg="#1a1a2e")
        self.resizable(True, True)

        self.bot_running = False
        self.bot_stop_event = threading.Event()
        self.checker_running = False
        self.checker_stop_event = threading.Event()
        self.scraper_running = False
        self.log_queue = queue.Queue()

        self._build_styles()
        self._build_ui()
        self._poll_log_queue()

    # ── Styles ────────────────────────────────────────────────────────────

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#16213e", foreground="#e0e0e0",
                         padding=[14, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#0f3460")],
                  foreground=[("selected", "#e94560")])

        style.configure("TFrame", background="#1a1a2e")
        style.configure("TLabel", background="#1a1a2e", foreground="#e0e0e0",
                         font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"),
                         foreground="#e94560", background="#1a1a2e")

        style.configure("Accent.TButton", background="#e94560", foreground="white",
                         font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.map("Accent.TButton",
                  background=[("active", "#c73e54"), ("disabled", "#555")])

        style.configure("Stop.TButton", background="#ff6b6b", foreground="white",
                         font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.map("Stop.TButton",
                  background=[("active", "#ee5a5a"), ("disabled", "#555")])

        style.configure("TEntry", fieldbackground="#16213e", foreground="#e0e0e0",
                         insertcolor="#e0e0e0", font=("Segoe UI", 10))
        style.configure("TSpinbox", fieldbackground="#16213e", foreground="#e0e0e0",
                         font=("Segoe UI", 10))

    # ── UI Layout ─────────────────────────────────────────────────────────

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self._build_bot_tab(notebook)
        self._build_scraper_tab(notebook)
        self._build_checker_tab(notebook)

        # Shared log at bottom
        log_frame = ttk.Frame(self)
        log_frame.pack(fill="both", expand=False, padx=8, pady=(0, 8))
        ttk.Label(log_frame, text="Log", style="Header.TLabel").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(
            log_frame, height=10, bg="#0d1117", fg="#58a6ff",
            font=("Consolas", 9), insertbackground="#58a6ff",
            relief="flat", state="disabled"
        )
        self.log_box.pack(fill="both", expand=True)

    def _build_bot_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Viewer Bot  ")

        # Channel
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=16, pady=(16, 4))
        ttk.Label(row, text="Twitch Channel:").pack(side="left")
        self.channel_var = tk.StringVar(value="triixrll")
        ttk.Entry(row, textvariable=self.channel_var, width=30).pack(side="left", padx=(8, 0))

        # Threads
        row2 = ttk.Frame(frame)
        row2.pack(fill="x", padx=16, pady=4)
        ttk.Label(row2, text="Threads:").pack(side="left")
        self.threads_var = tk.IntVar(value=100)
        ttk.Spinbox(row2, from_=1, to=5000, textvariable=self.threads_var,
                     width=8).pack(side="left", padx=(8, 0))

        # Proxy file
        row3 = ttk.Frame(frame)
        row3.pack(fill="x", padx=16, pady=4)
        ttk.Label(row3, text="Proxy File:").pack(side="left")
        self.proxy_file_var = tk.StringVar(value=GOOD_PROXY_FILE)
        ttk.Entry(row3, textvariable=self.proxy_file_var, width=40).pack(side="left", padx=(8, 0))
        ttk.Button(row3, text="Browse", style="Accent.TButton",
                    command=self._browse_proxy_file).pack(side="left", padx=(6, 0))

        # Buttons
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", padx=16, pady=(12, 4))
        self.start_btn = ttk.Button(btn_row, text="Start Bot", style="Accent.TButton",
                                     command=self._start_bot)
        self.start_btn.pack(side="left")
        self.stop_btn = ttk.Button(btn_row, text="Stop Bot", style="Stop.TButton",
                                    command=self._stop_bot, state="disabled")
        self.stop_btn.pack(side="left", padx=(8, 0))

        # Status
        self.bot_status_var = tk.StringVar(value="Idle")
        ttk.Label(frame, textvariable=self.bot_status_var,
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(8, 0))

    def _build_scraper_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Proxy Scraper  ")

        ttk.Label(frame, text="Scrape free proxies from public sources",
                  style="Header.TLabel").pack(anchor="w", padx=16, pady=(16, 4))

        # Proxy type dropdown
        type_row = ttk.Frame(frame)
        type_row.pack(fill="x", padx=16, pady=4)
        ttk.Label(type_row, text="Proxy Type:").pack(side="left")
        self.proxy_type_var = tk.StringVar(value="All")
        type_combo = ttk.Combobox(type_row, textvariable=self.proxy_type_var,
                                   values=PROXY_TYPE_OPTIONS, state="readonly", width=15)
        type_combo.pack(side="left", padx=(8, 0))
        self.source_count_var = tk.StringVar(value=self._get_source_count("All"))
        ttk.Label(type_row, textvariable=self.source_count_var).pack(side="left", padx=(12, 0))
        type_combo.bind("<<ComboboxSelected>>", self._on_proxy_type_changed)

        # Output file
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=16, pady=4)
        ttk.Label(row, text="Save to:").pack(side="left")
        self.scrape_output_var = tk.StringVar(value=SCRAPED_PROXY_FILE)
        ttk.Entry(row, textvariable=self.scrape_output_var, width=40).pack(side="left", padx=(8, 0))

        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", padx=16, pady=(12, 4))
        self.scrape_btn = ttk.Button(btn_row, text="Scrape Proxies", style="Accent.TButton",
                                      command=self._start_scrape)
        self.scrape_btn.pack(side="left")

        self.scrape_status_var = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self.scrape_status_var,
                  font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(8, 0))

    def _build_checker_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Proxy Checker  ")

        ttk.Label(frame, text="Check proxies & keep only working ones",
                  style="Header.TLabel").pack(anchor="w", padx=16, pady=(16, 4))

        # Input file
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=16, pady=4)
        ttk.Label(row, text="Input File:").pack(side="left")
        self.check_input_var = tk.StringVar(value=SCRAPED_PROXY_FILE)
        ttk.Entry(row, textvariable=self.check_input_var, width=40).pack(side="left", padx=(8, 0))
        ttk.Button(row, text="Browse", style="Accent.TButton",
                    command=self._browse_check_input).pack(side="left", padx=(6, 0))

        # Output file
        row2 = ttk.Frame(frame)
        row2.pack(fill="x", padx=16, pady=4)
        ttk.Label(row2, text="Good Proxies:").pack(side="left")
        self.check_output_var = tk.StringVar(value=GOOD_PROXY_FILE)
        ttk.Entry(row2, textvariable=self.check_output_var, width=40).pack(side="left", padx=(8, 0))

        # Timeout & workers
        row3 = ttk.Frame(frame)
        row3.pack(fill="x", padx=16, pady=4)
        ttk.Label(row3, text="Timeout (s):").pack(side="left")
        self.timeout_var = tk.IntVar(value=2)
        ttk.Spinbox(row3, from_=1, to=30, textvariable=self.timeout_var,
                     width=5).pack(side="left", padx=(8, 0))
        ttk.Label(row3, text="Workers:").pack(side="left", padx=(16, 0))
        self.workers_var = tk.IntVar(value=500)
        ttk.Spinbox(row3, from_=1, to=1000, textvariable=self.workers_var,
                     width=6).pack(side="left", padx=(8, 0))

        # Buttons
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", padx=16, pady=(12, 4))
        self.check_btn = ttk.Button(btn_row, text="Check Proxies", style="Accent.TButton",
                                     command=self._start_checker)
        self.check_btn.pack(side="left")
        self.check_stop_btn = ttk.Button(btn_row, text="Stop", style="Stop.TButton",
                                          command=self._stop_checker, state="disabled")
        self.check_stop_btn.pack(side="left", padx=(8, 0))

        # Progress
        self.check_progress = ttk.Progressbar(frame, mode="determinate", length=400)
        self.check_progress.pack(anchor="w", padx=16, pady=(8, 0))
        self.check_status_var = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self.check_status_var,
                  font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(4, 0))

    # ── Proxy Type Helpers ────────────────────────────────────────────────

    def _get_sources_for_type(self, proxy_type):
        if proxy_type == "All":
            sources = []
            for lst in PROXY_SOURCES.values():
                sources.extend(lst)
            return sources
        elif proxy_type == "HTTP/HTTPS":
            return PROXY_SOURCES["http"]
        elif proxy_type == "SOCKS4":
            return PROXY_SOURCES["socks4"]
        elif proxy_type == "SOCKS5":
            return PROXY_SOURCES["socks5"]
        return []

    def _get_source_count(self, proxy_type):
        return f"Sources: {len(self._get_sources_for_type(proxy_type))} lists"

    def _on_proxy_type_changed(self, event=None):
        self.source_count_var.set(self._get_source_count(self.proxy_type_var.get()))

    # ── Logging ───────────────────────────────────────────────────────────

    def log(self, msg):
        self.log_queue.put(msg)

    def _poll_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"{msg}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.after(100, self._poll_log_queue)

    # ── File Browsing ─────────────────────────────────────────────────────

    def _browse_proxy_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.proxy_file_var.set(path)

    def _browse_check_input(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.check_input_var.set(path)

    # ── Viewer Bot ────────────────────────────────────────────────────────

    def _start_bot(self):
        channel = self.channel_var.get().strip()
        if not channel:
            messagebox.showwarning("Warning", "Enter a Twitch channel name.")
            return

        proxy_file = self.proxy_file_var.get().strip()
        if not os.path.isfile(proxy_file):
            messagebox.showwarning("Warning", f"Proxy file not found: {proxy_file}")
            return

        self.bot_stop_event.clear()
        self.bot_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.bot_status_var.set(f"Running on #{channel}")
        self.log(f"[BOT] Starting viewer bot for #{channel}")

        t = threading.Thread(target=self._bot_worker, args=(channel, proxy_file), daemon=True)
        t.start()

    def _stop_bot(self):
        self.bot_stop_event.set()
        self.bot_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.bot_status_var.set("Stopped")
        self.log("[BOT] Stop signal sent.")

    def _bot_worker(self, channel, proxy_file):
        try:
            ua = UserAgent()
            sl_session = Streamlink()
            sl_session.set_option("http-headers", {
                "User-Agent": ua.random,
                "Client-ID": "ewvlchtxgqq88ru9gmfp1gmyt6h2b93"
            })

            channel_url = f"https://www.twitch.tv/{channel}"
            max_threads = self.threads_var.get()

            # Load proxies
            with open(proxy_file) as f:
                proxies = [line.strip() for line in f if line.strip()]

            if not proxies:
                self.log("[BOT] No proxies found in file!")
                return

            self.log(f"[BOT] Loaded {len(proxies)} proxies, using {max_threads} threads")

            all_proxy_data = [{"proxy": p, "time": time.time(), "url": ""} for p in proxies]
            shuffle(all_proxy_data)

            # Get stream URL
            def get_url():
                try:
                    streams = sl_session.streams(channel_url)
                    if "audio_only" in streams:
                        return streams["audio_only"].url
                    elif "worst" in streams:
                        return streams["worst"].url
                except Exception:
                    pass
                return ""

            def send_request(proxy_data):
                try:
                    if proxy_data["url"] == "":
                        proxy_data["url"] = get_url()
                    if not proxy_data["url"]:
                        return
                    if time.time() - proxy_data["time"] >= random.randint(1, 5):
                        proxy_dict = {"http": proxy_data["proxy"], "https": proxy_data["proxy"]}
                        headers = {"User-Agent": ua.random}
                        with requests.Session() as s:
                            resp = s.head(proxy_data["url"], proxies=proxy_dict,
                                          headers=headers, timeout=10)
                        self.log(f"[BOT] {proxy_data['proxy']} | {resp.status_code}")
                        proxy_data["time"] = time.time()
                except Exception:
                    pass

            while not self.bot_stop_event.is_set():
                threads = []
                for i in range(min(max_threads, len(all_proxy_data))):
                    if self.bot_stop_event.is_set():
                        break
                    pd = all_proxy_data[random.randint(0, len(all_proxy_data) - 1)]
                    t = threading.Thread(target=send_request, args=(pd,), daemon=True)
                    t.start()
                    threads.append(t)
                shuffle(all_proxy_data)
                # Wait with periodic stop checks
                for _ in range(10):
                    if self.bot_stop_event.is_set():
                        break
                    time.sleep(0.5)

        except Exception as e:
            self.log(f"[BOT] Error: {e}")
        finally:
            self.log("[BOT] Bot stopped.")
            self.bot_running = False

    # ── Proxy Scraper ─────────────────────────────────────────────────────

    def _start_scrape(self):
        if self.scraper_running:
            return
        self.scraper_running = True
        self.scrape_btn.configure(state="disabled")
        proxy_type = self.proxy_type_var.get()
        self.scrape_status_var.set(f"Scraping {proxy_type} proxies...")
        self.log(f"[SCRAPER] Starting proxy scrape ({proxy_type})...")
        t = threading.Thread(target=self._scrape_worker, args=(proxy_type,), daemon=True)
        t.start()

    def _scrape_worker(self, proxy_type):
        sources = self._get_sources_for_type(proxy_type)
        all_proxies = set()
        for src in sources:
            try:
                self.log(f"[SCRAPER] Fetching: {src[:60]}...")
                resp = requests.get(src, timeout=15)
                if resp.status_code == 200:
                    lines = resp.text.strip().splitlines()
                    count = 0
                    for line in lines:
                        proxy = line.strip()
                        if proxy and ":" in proxy:
                            # Extract just ip:port (some lists have extra columns)
                            parts = proxy.split()
                            proxy = parts[0]
                            if self._is_valid_proxy_format(proxy):
                                all_proxies.add(proxy)
                                count += 1
                    self.log(f"[SCRAPER] Got {count} proxies from source")
                else:
                    self.log(f"[SCRAPER] HTTP {resp.status_code} from source")
            except Exception as e:
                self.log(f"[SCRAPER] Failed: {e}")

        # Save
        output_path = self.scrape_output_var.get().strip()
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            for proxy in sorted(all_proxies):
                f.write(proxy + "\n")

        self.log(f"[SCRAPER] Done! {len(all_proxies)} unique proxies saved to {output_path}")
        self.scrape_status_var.set(f"Done - {len(all_proxies)} proxies scraped")
        self.scrape_btn.configure(state="normal")
        self.scraper_running = False
        # Auto-load scraped file into checker and start checking
        self.check_input_var.set(output_path)
        self.log(f"[SCRAPER] Auto-starting proxy checker...")
        self.after(500, self._start_checker)

    @staticmethod
    def _is_valid_proxy_format(proxy):
        try:
            host, port = proxy.rsplit(":", 1)
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return False
            parts = host.split(".")
            if len(parts) != 4:
                return False
            for p in parts:
                n = int(p)
                if n < 0 or n > 255:
                    return False
            return True
        except (ValueError, IndexError):
            return False

    # ── Proxy Checker ─────────────────────────────────────────────────────

    def _start_checker(self):
        input_file = self.check_input_var.get().strip()
        if not os.path.isfile(input_file):
            messagebox.showwarning("Warning", f"File not found: {input_file}")
            return

        self.checker_stop_event.clear()
        self.checker_running = True
        self.check_btn.configure(state="disabled")
        self.check_stop_btn.configure(state="normal")
        self.check_status_var.set("Checking...")
        self.log("[CHECKER] Starting proxy check...")

        t = threading.Thread(target=self._checker_worker, args=(input_file,), daemon=True)
        t.start()

    def _stop_checker(self):
        self.checker_stop_event.set()
        self.check_stop_btn.configure(state="disabled")
        self.log("[CHECKER] Stop signal sent.")

    def _checker_worker(self, input_file):
        with open(input_file) as f:
            proxies = [line.strip() for line in f if line.strip()]

        total = len(proxies)
        if total == 0:
            self.log("[CHECKER] No proxies to check.")
            self.checker_running = False
            return

        self.log(f"[CHECKER] Checking {total} proxies...")
        self.check_progress["maximum"] = total
        self.check_progress["value"] = 0

        good = []
        bad = 0
        checked = 0
        timeout_val = self.timeout_var.get()
        workers = self.workers_var.get()
        lock = threading.Lock()

        test_url = "http://httpbin.org/ip"

        def check_one(proxy):
            nonlocal checked, bad
            if self.checker_stop_event.is_set():
                return None
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            try:
                resp = requests.get(test_url, proxies=proxy_dict, timeout=timeout_val)
                if resp.status_code == 200:
                    self.log(f"[CHECKER] GOOD: {proxy}")
                    return proxy
                else:
                    return None
            except Exception:
                return None
            finally:
                with lock:
                    checked += 1
                self._update_checker_progress(checked, total, len(good), bad)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(check_one, p): p for p in proxies}
            for future in as_completed(futures):
                if self.checker_stop_event.is_set():
                    pool.shutdown(wait=False, cancel_futures=True)
                    break
                result = future.result()
                if result:
                    good.append(result)
                else:
                    bad += 1

        # Save good proxies
        output_file = self.check_output_var.get().strip()
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w") as f:
            for proxy in sorted(good):
                f.write(proxy + "\n")

        self.log(f"[CHECKER] Done! {len(good)} good / {bad} bad out of {total}")
        self.log(f"[CHECKER] Good proxies saved to {output_file}")
        self.check_status_var.set(f"Done - {len(good)} good, {bad} bad")
        self.check_btn.configure(state="normal")
        self.check_stop_btn.configure(state="disabled")
        self.checker_running = False
        # Auto-load good proxies into the bot's proxy file
        self.proxy_file_var.set(output_file)
        self.log(f"[CHECKER] Auto-loaded {len(good)} good proxies into Viewer Bot.")

    def _update_checker_progress(self, checked, total, good_count, bad_count):
        self.check_progress["value"] = checked
        self.check_status_var.set(
            f"Checked {checked}/{total} | Good: {good_count} | Bad: {bad_count}"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
