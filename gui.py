import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import requests
import re
import time
import random
import queue
import os
import string
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
        # Residential / rotating proxy sources
        "https://raw.githubusercontent.com/im-razvan/proxy_list/main/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/ObcbO/getproxy/master/http.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/STARTER-X7/Proxy-List/main/http.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
        "https://raw.githubusercontent.com/caliphdev/elite-proxies/master/http.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Finder/master/Proxy%20Lists/http.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
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
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
        "https://raw.githubusercontent.com/caliphdev/elite-proxies/master/socks4.txt",
        "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks4.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Finder/master/Proxy%20Lists/socks4.txt",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all",
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
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
        "https://raw.githubusercontent.com/caliphdev/elite-proxies/master/socks5.txt",
        "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks5.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Finder/master/Proxy%20Lists/socks5.txt",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
    ],
}

PROXY_TYPE_OPTIONS = ["All", "HTTP/HTTPS", "SOCKS4", "SOCKS5"]

PROXIES_DIR = "Proxies_txt"
GOOD_PROXY_FILE = os.path.join(PROXIES_DIR, "good_proxy.txt")
SCRAPED_PROXY_FILE = os.path.join(PROXIES_DIR, "scraped_proxies.txt")

# ─── Realistic Browser Fingerprints ──────────────────────────────────────────

CHROME_VERSIONS = [
    "120.0.0.0", "121.0.0.0", "122.0.0.0", "123.0.0.0", "124.0.0.0",
    "125.0.0.0", "126.0.0.0", "127.0.0.0", "128.0.0.0", "129.0.0.0",
]

OS_STRINGS = [
    "Windows NT 10.0; Win64; x64",
    "Windows NT 10.0; WOW64",
    "Macintosh; Intel Mac OS X 10_15_7",
    "Macintosh; Intel Mac OS X 13_6_1",
    "X11; Linux x86_64",
    "X11; Ubuntu; Linux x86_64",
]

SCREEN_RESOLUTIONS = [
    (1920, 1080), (2560, 1440), (1366, 768), (1536, 864),
    (1440, 900), (1280, 720), (3840, 2160), (1680, 1050),
]

LANGUAGES = [
    "en-US,en;q=0.9", "en-US,en;q=0.9,es;q=0.8",
    "en-GB,en;q=0.9", "en-US,en;q=0.9,fr;q=0.8",
    "en-US,en;q=0.9,de;q=0.8", "en,en-US;q=0.9",
]

TWITCH_CLIENT_IDS = [
    "kimne78kx3ncx6brgo4mv6wki5h1ko",  # Main web client
    "ue6666qo983tsx6so1t0vnawi233wa",   # Alternate web client
]


def generate_device_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))


def generate_browser_fingerprint():
    """Generate a unique, realistic browser fingerprint for each viewer."""
    chrome_ver = random.choice(CHROME_VERSIONS)
    os_str = random.choice(OS_STRINGS)
    screen = random.choice(SCREEN_RESOLUTIONS)
    lang = random.choice(LANGUAGES)
    device_id = generate_device_id()

    user_agent = (
        f"Mozilla/5.0 ({os_str}) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"
    )

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/vnd.apple.mpegurl, application/x-mpegURL, */*",
        "Accept-Language": lang,
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.twitch.tv",
        "Referer": "https://www.twitch.tv/",
        "Sec-Ch-Ua": f'"Chromium";v="{chrome_ver.split(".")[0]}", "Google Chrome";v="{chrome_ver.split(".")[0]}", "Not?A_Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"' if "Windows" in os_str else '"macOS"' if "Mac" in os_str else '"Linux"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Connection": "keep-alive",
    }

    return {
        "headers": headers,
        "user_agent": user_agent,
        "device_id": device_id,
        "client_id": random.choice(TWITCH_CLIENT_IDS),
        "screen": screen,
        "lang": lang,
    }


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
        self.channel_var = tk.StringVar(value="toony69")
        ttk.Entry(row, textvariable=self.channel_var, width=30).pack(side="left", padx=(8, 0))

        # Threads
        row2 = ttk.Frame(frame)
        row2.pack(fill="x", padx=16, pady=4)
        ttk.Label(row2, text="Threads:").pack(side="left")
        self.threads_var = tk.IntVar(value=100)
        ttk.Spinbox(row2, from_=1, to=5000, textvariable=self.threads_var,
                     width=8).pack(side="left", padx=(8, 0))

        # Proxy type
        row3 = ttk.Frame(frame)
        row3.pack(fill="x", padx=16, pady=4)
        ttk.Label(row3, text="Proxy Type:").pack(side="left")
        self.bot_proxy_type_var = tk.StringVar(value="All")
        ttk.Combobox(row3, textvariable=self.bot_proxy_type_var,
                     values=PROXY_TYPE_OPTIONS, state="readonly", width=15).pack(side="left", padx=(8, 0))

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

        # ── Twitch Live Views section ──
        viewer_frame = ttk.Frame(frame)
        viewer_frame.pack(fill="x", padx=16, pady=(16, 4))

        ttk.Label(viewer_frame, text="Twitch Live Views",
                  style="Header.TLabel").pack(anchor="w")

        # Viewer count label
        self.viewer_count_var = tk.StringVar(value="0 viewers connected")
        ttk.Label(viewer_frame, textvariable=self.viewer_count_var,
                  font=("Segoe UI", 11, "bold"), foreground="#58a6ff",
                  background="#1a1a2e").pack(anchor="w", pady=(4, 2))

        # Progress bar (indeterminate = loading animation when active)
        style = ttk.Style()
        style.configure("Viewer.Horizontal.TProgressbar",
                        troughcolor="#16213e", background="#e94560",
                        thickness=25)
        self.viewer_progress = ttk.Progressbar(
            viewer_frame, style="Viewer.Horizontal.TProgressbar",
            mode="determinate", length=500, maximum=100
        )
        self.viewer_progress.pack(fill="x", pady=(2, 4))

        # Animated loading bar (indeterminate bouncing bar)
        style.configure("Loading.Horizontal.TProgressbar",
                        troughcolor="#16213e", background="#58a6ff",
                        thickness=8)
        self.loading_bar = ttk.Progressbar(
            viewer_frame, style="Loading.Horizontal.TProgressbar",
            mode="indeterminate", length=500
        )
        self.loading_bar.pack(fill="x", pady=(0, 4))

        # Peak / total label
        self.viewer_detail_var = tk.StringVar(value="Peak: 0 | Total sent: 0")
        ttk.Label(viewer_frame, textvariable=self.viewer_detail_var,
                  font=("Segoe UI", 9), foreground="#888",
                  background="#1a1a2e").pack(anchor="w")

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

        self.bot_stop_event.clear()
        self.bot_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.bot_status_var.set("Loading proxies...")
        self.viewer_count_var.set("Starting...")
        self.viewer_progress["value"] = 0
        self.loading_bar.start(15)
        self.log(f"[BOT] Starting bot for #{channel}...")

        t = threading.Thread(target=self._bot_worker, args=(channel,), daemon=True)
        t.start()

    def _stop_bot(self):
        self.bot_stop_event.set()
        self.bot_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.bot_status_var.set("Stopped")
        self.loading_bar.stop()
        self.log("[BOT] Stop signal sent.")

    def _scrape_proxies(self, proxy_type):
        """Scrape proxies from public sources and return them as a list."""
        sources = self._get_sources_for_type(proxy_type)
        all_proxies = set()
        for src in sources:
            if self.bot_stop_event.is_set():
                break
            try:
                self.log(f"[BOT] Scraping: {src[:60]}...")
                resp = requests.get(src, timeout=15)
                if resp.status_code == 200:
                    for line in resp.text.strip().splitlines():
                        proxy = line.strip().split()[0]
                        if proxy and ":" in proxy and self._is_valid_proxy_format(proxy):
                            all_proxies.add(proxy)
            except Exception:
                pass
        return list(all_proxies)

    def _check_proxies(self, proxies):
        """Check proxies can sustain a connection for at least 10 seconds."""
        good = []
        lock = threading.Lock()
        checked = {"count": 0}
        total = len(proxies)

        def check_one(proxy):
            if self.bot_stop_event.is_set():
                return
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            try:
                # Test 1: Basic connectivity
                start = time.time()
                resp = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=5)
                if resp.status_code != 200:
                    return
                latency = time.time() - start

                # Test 2: Sustained connection - download data over ~10 seconds
                # Use a streaming endpoint to verify the proxy stays alive
                start2 = time.time()
                resp2 = requests.get(
                    "http://httpbin.org/drip?duration=10&numbytes=100&code=200&delay=0",
                    proxies=proxy_dict, timeout=15, stream=True
                )
                for chunk in resp2.iter_content(chunk_size=64):
                    if self.bot_stop_event.is_set():
                        return
                held = time.time() - start2

                if resp2.status_code == 200 and held >= 8:
                    with lock:
                        good.append(proxy)
                    self.log(f"[CHECK] GOOD ({latency:.1f}s latency, held {held:.0f}s): {proxy}")
            except Exception:
                pass
            finally:
                with lock:
                    checked["count"] += 1
                    if checked["count"] % 50 == 0 or checked["count"] == total:
                        self.bot_status_var.set(
                            f"Checked {checked['count']}/{total} | Good: {len(good)}"
                        )

        self.log(f"[CHECK] Testing {total} proxies for sustained connections (10s hold)...")
        with ThreadPoolExecutor(max_workers=200) as pool:
            futures = {pool.submit(check_one, p): p for p in proxies}
            for f in as_completed(futures):
                if self.bot_stop_event.is_set():
                    pool.shutdown(wait=False, cancel_futures=True)
                    break

        self.log(f"[CHECK] {len(good)} / {total} proxies can hold 10s+ connections")
        return good

    def _bot_worker(self, channel):
        try:
            channel_url = f"https://www.twitch.tv/{channel}"
            max_threads = self.threads_var.get()

            # Prefer already checked proxies from Proxies_txt/good_proxy.txt
            proxies = []
            if os.path.isfile(GOOD_PROXY_FILE):
                try:
                    with open(GOOD_PROXY_FILE, "r", encoding="utf-8") as f:
                        loaded = [line.strip() for line in f if line.strip()]
                    valid_loaded = [p for p in loaded if self._is_valid_proxy_format(p)]
                    proxies = list(dict.fromkeys(valid_loaded))
                    if proxies:
                        self.log(f"[BOT] Loaded {len(proxies)} proxies from {GOOD_PROXY_FILE}")
                except (OSError, UnicodeDecodeError) as e:
                    self.log(f"[BOT] Could not read {GOOD_PROXY_FILE}: {e}")

            # Fallback path if no good_proxy file (or empty file)
            if not proxies:
                self.log(f"[BOT] No valid proxies in {GOOD_PROXY_FILE}. Falling back to scrape/check...")
                proxy_type = self.bot_proxy_type_var.get()
                raw_proxies = self._scrape_proxies(proxy_type)

                if not raw_proxies:
                    self.log("[BOT] No proxies scraped!")
                    self.bot_status_var.set("Failed - no proxies")
                    return

                self.log(f"[BOT] Scraped {len(raw_proxies)} proxies. Now checking quality...")
                self.bot_status_var.set(f"Checking {len(raw_proxies)} proxies...")
                proxies = self._check_proxies(raw_proxies)

                if not proxies:
                    self.log("[BOT] No working proxies found!")
                    self.bot_status_var.set("Failed - no working proxies")
                    return

                self.log(f"[BOT] {len(proxies)} high-quality proxies ready")

            # Get the HLS master playlist URL via Streamlink
            self.bot_status_var.set("Fetching stream...")
            self.log("[BOT] Getting stream playlist URL...")

            master_url = None
            for attempt in range(3):
                if self.bot_stop_event.is_set():
                    return
                try:
                    sl_session = Streamlink()
                    sl_session.set_option("http-headers", {
                        "Client-ID": random.choice(TWITCH_CLIENT_IDS),
                        "User-Agent": generate_browser_fingerprint()["user_agent"],
                    })
                    streams = sl_session.streams(channel_url)
                    if "audio_only" in streams:
                        master_url = streams["audio_only"].url
                    elif "worst" in streams:
                        master_url = streams["worst"].url
                    if master_url:
                        self.log(f"[BOT] Got stream URL")
                        break
                except Exception as e:
                    self.log(f"[BOT] Stream attempt {attempt+1} failed: {e}")
                    time.sleep(3)

            if not master_url:
                self.log("[BOT] Could not get stream URL. Make sure the channel is LIVE.")
                self.bot_status_var.set("Failed - channel not live")
                return

            # Ensure each proxy is only used by one viewer at a time
            used_proxies = set()
            proxy_lock = threading.Lock()
            active_viewers = {"count": 0, "peak": 0, "total_sent": 0}
            viewer_lock = threading.Lock()
            total_proxies = len(proxies)

            def update_viewer_count(delta):
                with viewer_lock:
                    active_viewers["count"] += delta
                    if delta > 0:
                        active_viewers["total_sent"] += 1
                    if active_viewers["count"] > active_viewers["peak"]:
                        active_viewers["peak"] = active_viewers["count"]
                    count = active_viewers["count"]
                    peak = active_viewers["peak"]
                    total = active_viewers["total_sent"]
                self.bot_status_var.set(
                    f"Running on #{channel} | Viewers: {count} | Proxies: {total_proxies}"
                )
                self.viewer_count_var.set(f"{count} viewers connected")
                self.viewer_progress["maximum"] = max(total_proxies, 1)
                self.viewer_progress["value"] = count
                self.viewer_detail_var.set(f"Peak: {peak} | Total sent: {total}")

            def simulate_viewer(proxy_str):
                """Simulate a real browser viewer using HLS segment downloading."""
                # Claim this proxy
                with proxy_lock:
                    if proxy_str in used_proxies:
                        return
                    used_proxies.add(proxy_str)

                connected = False
                try:
                    # Each viewer gets a unique browser fingerprint
                    fp = generate_browser_fingerprint()
                    proxy_dict = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}

                    session = requests.Session()
                    session.proxies = proxy_dict
                    session.headers.update(fp["headers"])
                    session.timeout = 15

                    # Step 1: Fetch the HLS master playlist (like a real player does)
                    try:
                        playlist_resp = session.get(master_url, timeout=15)
                        if playlist_resp.status_code != 200:
                            return
                    except Exception:
                        return

                    connected = True
                    update_viewer_count(1)
                    connect_time = time.time()
                    self.log(f"[BOT] VIEWER connected: {proxy_str}")

                    # Random watch duration: 3-10 minutes like a real viewer
                    watch_minutes = random.uniform(3, 10)
                    watch_duration = watch_minutes * 60
                    end_time = time.time() + watch_duration
                    segment_count = 0
                    min_watch_secs = 15  # Must hold at least 15s for Twitch to count

                    # Step 2: Parse playlist and download segments like a real HLS player
                    while not self.bot_stop_event.is_set() and time.time() < end_time:
                        try:
                            # Re-fetch the playlist periodically (HLS players do this)
                            playlist_resp = session.get(master_url, timeout=10)
                            if playlist_resp.status_code != 200:
                                # Don't bail immediately - retry after a pause
                                time.sleep(random.uniform(2, 4))
                                continue

                            playlist_text = playlist_resp.text

                            # Extract .ts segment URLs from the playlist
                            segment_urls = re.findall(
                                r'(https?://[^\s]+\.ts[^\s]*)', playlist_text
                            )

                            if not segment_urls:
                                # If no full URLs, look for relative paths
                                lines = playlist_text.strip().split('\n')
                                segment_urls = [
                                    l.strip() for l in lines
                                    if l.strip() and not l.strip().startswith('#')
                                ]

                            if segment_urls:
                                # Download the latest segments (like a real video player)
                                for seg_url in segment_urls[-3:]:
                                    if self.bot_stop_event.is_set() or time.time() > end_time:
                                        break
                                    try:
                                        seg_resp = session.get(seg_url, timeout=10, stream=True)
                                        for chunk in seg_resp.iter_content(chunk_size=16384):
                                            if self.bot_stop_event.is_set():
                                                break
                                        segment_count += 1
                                    except Exception:
                                        pass
                                    # Small random delay between segments
                                    time.sleep(random.uniform(0.3, 1.5))
                            else:
                                # Fallback: stream the playlist URL directly
                                try:
                                    stream_resp = session.get(
                                        master_url, timeout=10, stream=True
                                    )
                                    bytes_read = 0
                                    for chunk in stream_resp.iter_content(chunk_size=8192):
                                        bytes_read += len(chunk) if chunk else 0
                                        if self.bot_stop_event.is_set() or time.time() > end_time:
                                            break
                                    segment_count += 1
                                except Exception:
                                    pass

                            # Wait before refreshing playlist (HLS standard ~2-6s)
                            # Real players poll every target duration (~2-4s)
                            time.sleep(random.uniform(2.0, 5.0))

                        except Exception:
                            time.sleep(random.uniform(2, 5))

                    watched_secs = time.time() - connect_time
                    counted = "COUNTED" if watched_secs >= min_watch_secs else "TOO SHORT"
                    self.log(
                        f"[BOT] VIEWER done: {proxy_str} | "
                        f"{watched_secs:.0f}s ({watch_minutes:.1f}min) | "
                        f"{segment_count} segments | {counted}"
                    )

                except Exception:
                    pass
                finally:
                    if connected:
                        update_viewer_count(-1)
                    with proxy_lock:
                        used_proxies.discard(proxy_str)
                    try:
                        session.close()
                    except Exception:
                        pass

            # Main loop: keep spawning viewers
            self.bot_status_var.set(f"Running on #{channel} | Starting viewers...")
            self.log(f"[BOT] Launching viewers with {max_threads} threads...")

            with ThreadPoolExecutor(max_workers=max_threads) as pool:
                while not self.bot_stop_event.is_set():
                    shuffle(proxies)
                    futures = []
                    for proxy in proxies:
                        if self.bot_stop_event.is_set():
                            break
                        with proxy_lock:
                            if proxy in used_proxies:
                                continue
                        futures.append(pool.submit(simulate_viewer, proxy))
                        # Stagger viewer launches (real users trickle in)
                        time.sleep(random.uniform(0.3, 1.5))

                    # Wait for current batch with periodic stop checks
                    for f in futures:
                        if self.bot_stop_event.is_set():
                            break
                        try:
                            f.result(timeout=2)
                        except Exception:
                            pass

                    # Brief pause before cycling
                    if not self.bot_stop_event.is_set():
                        time.sleep(random.uniform(1, 3))

        except Exception as e:
            self.log(f"[BOT] Error: {e}")
        finally:
            self.log("[BOT] Bot stopped.")
            self.bot_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.bot_status_var.set("Idle")
            self.loading_bar.stop()
            self.viewer_count_var.set("0 viewers connected")

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
        self.log(f"[CHECKER] Good proxies ready for use.")

    def _update_checker_progress(self, checked, total, good_count, bad_count):
        self.check_progress["value"] = checked
        self.check_status_var.set(
            f"Checked {checked}/{total} | Good: {good_count} | Bad: {bad_count}"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
