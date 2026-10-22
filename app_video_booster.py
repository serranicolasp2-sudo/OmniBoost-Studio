"""
OmniBoost Studio — Video Booster Ultra (Universal)
Diseño: Premium Minimalista "Tu Tiendita IA"
Colores oficiales de marca: Birome (#1E3C96), Tinta (#16205A), Malvón (#E0435C),
Yema (#FFD23F), Cinta (#1A1712), Papel (#F6F7FA), Plata (#8B97B0)
Bordes redondeados, estética editorial de alta gama.
"""

import os
import sys
import subprocess
import threading
import queue
import re
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.scrolledtext as scrolledtext

# Asegurar acceso a Herramientas para importar ui_theme
CURRENT_DIR = Path(__file__).resolve().parent
TOOLS_DIR = CURRENT_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# Asegurar ffmpeg/ffprobe en PATH para funcionamiento 100% offline y portable
_bundle_dir = Path(getattr(sys, "_MEIPASS", CURRENT_DIR))
for _cand in [_bundle_dir, _bundle_dir / "bin", Path(sys.executable).parent / "bin", Path(sys.executable).parent]:
    if (_cand / "ffmpeg.exe").exists():
        os.environ["PATH"] = str(_cand) + os.pathsep + os.environ.get("PATH", "")
        break

from ui_theme import (
    COLOR_BIROME, COLOR_BIROME_HOVER, COLOR_TINTA, COLOR_MALVON, COLOR_MALVON_HOVER,
    COLOR_YEMA, COLOR_CINTA, COLOR_PAPEL, COLOR_PLATA, COLOR_PERIWINKLE,
    BG_APP, BG_CARD, CHIP_BG, CHIP_BORDER, BG_CARD_BORDER, BG_INPUT, BG_INPUT_BORDER, BG_CONSOLE, BG_CONSOLE_BORDER,
    TEXT_MAIN, TEXT_MUTED, TEXT_DIM,
    FONT_HERO, FONT_TITLE, FONT_SUB, FONT_LABEL, FONT_BODY, FONT_MONO, FONT_BTN, FONT_BADGE,
    setup_app_theme, PillBadge, PillButton, RoundedCard, SegmentedSwitch, create_header, prompt_rename_dialog,
    ModernSlider, ConsoleText
)


class VideoBoosterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniBoost Studio — Video Booster Ultra")
        self.root.geometry("860x880")
        self.root.minsize(780, 740)
        self.root.configure(bg=BG_APP)

        self.process = None
        self.is_running = False
        self.cancel_requested = False
        self.msg_queue = queue.Queue()
        self.last_output_dir = ""
        self.current_tab_idx = 0

        setup_app_theme(self.root, app_icon="omniboost")
        self._build_ui()
        self.root.after(100, self._process_queue)

    def _build_ui(self):
        # 1. Encabezado con insignias oficiales
        create_header(
            self.root,
            title="OmniBoost Studio",
            subtitle="Mejora y definición con IA, contraste adaptativo CAS, HDR y de-banding para todo tipo de video.",
            badge_text="IA",
            rtx_text="RTX P7 ACTIVE",
            icon="omniboost"
        )

        # 2. Selector segmentado de modo (Pills modernas)
        switch_frame = tk.Frame(self.root, bg=BG_APP)
        switch_frame.pack(fill="x", padx=22, pady=(2, 6))

        self.segmented_switch = SegmentedSwitch(
            switch_frame,
            options=["  🎬 Archivo Individual  ", "  📁 Carpeta en Lote  "],
            on_change=self._on_switch_tab
        )
        self.segmented_switch.pack(anchor="w")

        # 3. Contenedor de origen/destino (Tarjeta redondeada)
        self.card_io = RoundedCard(self.root, radius=14, pad=16, auto_height=True)
        self.card_io.pack(fill="x", padx=22, pady=4)

        self.io_single_frame = tk.Frame(self.card_io.body, bg=BG_CARD)
        self.io_batch_frame = tk.Frame(self.card_io.body, bg=BG_CARD)

        self._build_single_io_content()
        self._build_batch_io_content()
        self.io_single_frame.pack(fill="x")

        # 4. Tarjeta de Parámetros y Calidad (Tarjeta redondeada)
        self.card_opts = RoundedCard(self.root, radius=14, pad=16, auto_height=True)
        self.card_opts.pack(fill="x", padx=22, pady=4)
        self._build_settings_content()

        # 5. Panel de Control y Progreso (Inferior)
        self._build_progress_card()

    def _on_switch_tab(self, idx):
        self.current_tab_idx = idx
        if idx == 0:
            self.io_batch_frame.pack_forget()
            self.io_single_frame.pack(fill="x")
        else:
            self.io_single_frame.pack_forget()
            self.io_batch_frame.pack(fill="x")

    def _build_single_io_content(self):
        f = self.io_single_frame

        tk.Label(f, text="Archivo de entrada (Video MP4/MOV/MKV o Imagen PNG/JPG):", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).pack(anchor="w", pady=(0, 4))

        in_row = tk.Frame(f, bg=BG_CARD)
        in_row.pack(fill="x", pady=(0, 6))

        in_well = tk.Frame(in_row, bg=BG_INPUT, highlightbackground=BG_INPUT_BORDER, highlightthickness=1)
        in_well.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.single_input_var = tk.StringVar()
        self.single_input_entry = tk.Entry(in_well, textvariable=self.single_input_var, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", font=FONT_BODY)
        self.single_input_entry.pack(fill="x", ipady=6, padx=8)

        btn_browse = PillButton(in_row, text="Examinar...", style="secondary", width=120, command=self._browse_single_input)
        btn_browse.pack(side="right")

        self.single_info_var = tk.StringVar(value="Esperando selección de archivo...")
        lbl_info = tk.Label(f, textvariable=self.single_info_var, bg=BG_CARD, fg=COLOR_PERIWINKLE, font=FONT_SUB)
        lbl_info.pack(anchor="w", pady=(0, 6))

        tk.Label(f, text="Archivo de salida personalizado:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).pack(anchor="w", pady=(2, 4))

        out_row = tk.Frame(f, bg=BG_CARD)
        out_row.pack(fill="x")

        out_well = tk.Frame(out_row, bg=BG_INPUT, highlightbackground=BG_INPUT_BORDER, highlightthickness=1)
        out_well.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.single_out_var = tk.StringVar()
        self.single_out_entry = tk.Entry(out_well, textvariable=self.single_out_var, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", font=FONT_BODY)
        self.single_out_entry.pack(fill="x", ipady=6, padx=8)

        btn_browse_out = PillButton(out_row, text="Guardar en...", style="secondary", width=120, command=self._browse_single_output)
        btn_browse_out.pack(side="right")

    def _build_batch_io_content(self):
        f = self.io_batch_frame

        tk.Label(f, text="Carpeta de origen con clips o imágenes:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).pack(anchor="w", pady=(0, 4))

        in_row = tk.Frame(f, bg=BG_CARD)
        in_row.pack(fill="x", pady=(0, 6))

        in_well = tk.Frame(in_row, bg=BG_INPUT, highlightbackground=BG_INPUT_BORDER, highlightthickness=1)
        in_well.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.batch_input_var = tk.StringVar()
        self.batch_input_entry = tk.Entry(in_well, textvariable=self.batch_input_var, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", font=FONT_BODY)
        self.batch_input_entry.pack(fill="x", ipady=6, padx=8)

        btn_browse = PillButton(in_row, text="Elegir Carpeta...", style="secondary", width=130, command=self._browse_batch_input)
        btn_browse.pack(side="right")

        tk.Label(f, text="Carpeta de salida:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).pack(anchor="w", pady=(2, 4))

        out_row = tk.Frame(f, bg=BG_CARD)
        out_row.pack(fill="x", pady=(0, 6))

        out_well = tk.Frame(out_row, bg=BG_INPUT, highlightbackground=BG_INPUT_BORDER, highlightthickness=1)
        out_well.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.batch_out_var = tk.StringVar()
        self.batch_out_entry = tk.Entry(out_well, textvariable=self.batch_out_var, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat", font=FONT_BODY)
        self.batch_out_entry.pack(fill="x", ipady=6, padx=8)

        btn_browse_out = PillButton(out_row, text="Guardar en...", style="secondary", width=130, command=self._browse_batch_output)
        btn_browse_out.pack(side="right")

        self.batch_recursive_var = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(f, text="Buscar recursivamente en subcarpetas", variable=self.batch_recursive_var, style="TCheckbutton")
        chk.pack(anchor="w", pady=(2, 0))

    def _build_settings_content(self):
        opts = self.card_opts.body
        opts.grid_columnconfigure(1, weight=1)

        top_bar = tk.Frame(opts, bg=BG_CARD)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        tk.Label(top_bar, text="Parámetros y Perfiles de Video Boost", bg=BG_CARD, fg=TEXT_MAIN, font=FONT_TITLE).pack(side="left")
        PillBadge(top_bar, text="PRESETS", bg_color=CHIP_BG, fg_color=COLOR_PERIWINKLE, border_color=CHIP_BORDER).pack(side="left", padx=8)

        # Preset selector
        tk.Label(opts, text="Tipo de Video / Perfil:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=4)
        self.preset_var = tk.StringVar(value="🌟 Universal / Equilibrado (Cámaras, Smartphones, Web)")
        preset_cb = ttk.Combobox(opts, textvariable=self.preset_var, state="readonly", width=54)
        preset_cb['values'] = (
            "🌟 Universal / Equilibrado (Cámaras, Smartphones, Web)",
            "🎬 Cine & Películas Reales (Piel natural, preserva grano 35mm)",
            "🎨 Animación 3D & CGI (Pixar, Disney, Gaming, Unreal Engine)",
            "⛩️ Anime & Animación 2D (Líneas definidas, colores limpios)",
            "🤖 Videos de IA (Kling, Runway, Sora — Anti-Banding & Denoise)",
            "📼 Restauración & Grano Fuerte (Limpia compresión severa)",
            "🎛️ Personalizado (Ajuste fino manual con controles inferiores)"
        )
        preset_cb.grid(row=1, column=1, sticky="ew", pady=4)
        preset_cb.bind("<<ComboboxSelected>>", self._on_preset_change)

        # Resolución
        tk.Label(opts, text="Resolución de Salida:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=4)
        self.res_var = tk.StringVar(value="Mantener resolución original")
        self.res_cb = ttk.Combobox(opts, textvariable=self.res_var, state="readonly", width=54)
        self.res_cb['values'] = (
            "Mantener resolución original",
            "Auto-Adaptativo 1080p (Horiz 1920x1080 / Vert 1080x1920)",
            "Auto-Adaptativo 4K UHD (Horiz 3840x2160 / Vert 2160x3840)",
            "Auto-Adaptativo 2K QHD (Horiz 2560x1440 / Vert 1440x2560)",
            "1080x1920 (9:16 Vertical Reels / TikTok / Shorts)",
            "2160x3840 (9:16 Vertical 4K Ultra HD)",
            "Escalar a 4K Ultra HD (3840x2160 — 16:9 Estándar)",
            "Escalar a 2K QHD (2560x1440)",
            "Escalar a 1080p Full HD (1920x1080)",
            "Escalar a 4K Cinema DCI (4096x2160)"
        )
        self.res_cb.grid(row=2, column=1, sticky="ew", pady=4)
        self.res_cb.bind("<<ComboboxSelected>>", self._on_res_change)

        # Aceleración GPU / Motor RTX
        tk.Label(opts, text="Aceleración GPU / Motor:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=4)
        self.hw_var = tk.StringVar(value="NVIDIA GeForce RTX (NVENC p7 + Spatial/Temporal AQ)")
        self.hw_cb = ttk.Combobox(opts, textvariable=self.hw_var, state="readonly", width=54)
        self.hw_cb['values'] = (
            "NVIDIA GeForce RTX (NVENC p7 + Spatial/Temporal AQ)",
            "NVIDIA GeForce RTX — HEVC / H.265 (Ultra Calidad 4K)",
            "AMD Radeon — AMF Hardware (RX 6000 / 7000 Series)",
            "CPU / Software Universal (libx264 — Máxima compatibilidad)"
        )
        self.hw_cb.grid(row=3, column=1, sticky="ew", pady=4)

        # Sliders de ajuste fino
        slider_frame = tk.Frame(opts, bg=BG_CARD)
        slider_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # 1. Nitidez (CAS)
        tk.Label(slider_frame, text="Nitidez (CAS):", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=2)
        self.sharp_var = tk.DoubleVar(value=50)
        self.sharp_scale = ModernSlider(slider_frame, from_=0, to=100, variable=self.sharp_var, length=190)
        self.sharp_scale.grid(row=0, column=1, sticky="w", pady=2)

        # 2. Claridad
        tk.Label(slider_frame, text="Claridad / Micro-contraste:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=0, column=2, sticky="w", padx=(16, 8), pady=2)
        self.clarity_var = tk.DoubleVar(value=40)
        self.clarity_scale = ModernSlider(slider_frame, from_=0, to=100, variable=self.clarity_var, length=190)
        self.clarity_scale.grid(row=0, column=3, sticky="w", pady=2)

        # 3. Denoise
        tk.Label(slider_frame, text="Reducción de Ruido:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=2)
        self.denoise_var = tk.DoubleVar(value=35)
        self.denoise_scale = ModernSlider(slider_frame, from_=0, to=100, variable=self.denoise_var, length=190)
        self.denoise_scale.grid(row=1, column=1, sticky="w", pady=2)

        # 4. De-Banding
        tk.Label(slider_frame, text="De-Banding / Anti-bloques:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=1, column=2, sticky="w", padx=(16, 8), pady=2)
        self.deband_var = tk.DoubleVar(value=30)
        self.deband_scale = ModernSlider(slider_frame, from_=0, to=100, variable=self.deband_var, length=190)
        self.deband_scale.grid(row=1, column=3, sticky="w", pady=2)

        # 5. Color HDR
        tk.Label(slider_frame, text="Color & Rango HDR:", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_LABEL).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=2)
        self.color_var = tk.DoubleVar(value=50)
        self.color_scale = ModernSlider(slider_frame, from_=0, to=100, variable=self.color_var, length=190)
        self.color_scale.grid(row=2, column=1, sticky="w", pady=2)

    def _build_progress_card(self):
        bot = tk.Frame(self.root, bg=BG_APP, padx=22, pady=4)
        bot.pack(fill="both", expand=True)

        btn_box = tk.Frame(bot, bg=BG_APP)
        btn_box.pack(fill="x", pady=(0, 8))

        self.btn_start = PillButton(btn_box, text="INICIAR VIDEO BOOST", style="primary", height=42, command=self._start_processing)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_cancel = PillButton(btn_box, text="Cancelar", style="danger", height=42, width=105, command=self._cancel)
        self.btn_cancel.configure_state("disabled")
        self.btn_cancel.pack(side="left", padx=(0, 8))

        self.btn_open_folder = PillButton(btn_box, text="Abrir Carpeta Destino", style="secondary", height=42, command=self._open_output_dir)
        self.btn_open_folder.pack(side="right")

        # Barra y Estado
        status_box = tk.Frame(bot, bg=BG_APP)
        status_box.pack(fill="x", pady=(2, 4))

        self.status_var = tk.StringVar(value="Listo para iniciar mejora.")
        self.lbl_status = tk.Label(status_box, textvariable=self.status_var, bg=BG_APP, fg=TEXT_MAIN, font=FONT_LABEL)
        self.lbl_status.pack(side="left")

        self.prog_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(bot, variable=self.prog_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 8))

        # Consola de registro con borde redondeado
        self.card_log = RoundedCard(bot, bg_app=BG_APP, card_bg=BG_CONSOLE, border_color=BG_CONSOLE_BORDER, radius=10, pad=10, auto_height=False)
        self.card_log.pack(fill="both", expand=True)

        self.log_area = ConsoleText(self.card_log.body, bg=BG_CONSOLE, fg="#A5B4CD", insertbackground=TEXT_MAIN, relief="flat", font=FONT_MONO)
        self.log_area.pack(fill="both", expand=True)
        self.log_area.insert(tk.END, "OmniBoost Studio iniciado con el tema visual oficial de Tu Tiendita IA (sitio web: tutiendita-ia.store).\nListo para procesar con máxima fidelidad visual y aceleración por hardware.\n")
        self.log_area.configure(state="disabled")

    def _on_preset_change(self, event=None):
        val = self.preset_var.get()
        if "Universal" in val:
            self.sharp_var.set(50)
            self.clarity_var.set(40)
            self.denoise_var.set(35)
            self.deband_var.set(30)
            self.color_var.set(50)
        elif "Cine & Películas Reales" in val:
            self.sharp_var.set(40)
            self.clarity_var.set(30)
            self.denoise_var.set(20)
            self.deband_var.set(40)
            self.color_var.set(50)
        elif "Animación 3D" in val:
            self.sharp_var.set(60)
            self.clarity_var.set(55)
            self.denoise_var.set(30)
            self.deband_var.set(45)
            self.color_var.set(65)
        elif "Anime & Animación 2D" in val:
            self.sharp_var.set(75)
            self.clarity_var.set(45)
            self.denoise_var.set(50)
            self.deband_var.set(60)
            self.color_var.set(60)
        elif "Videos de IA" in val:
            self.sharp_var.set(55)
            self.clarity_var.set(50)
            self.denoise_var.set(45)
            self.deband_var.set(75)
            self.color_var.set(55)
        elif "Restauración" in val:
            self.sharp_var.set(35)
            self.clarity_var.set(30)
            self.denoise_var.set(85)
            self.deband_var.set(70)
            self.color_var.set(45)

    def _on_res_change(self, event=None):
        res = self.res_var.get()
        tag = "4k_boosted" if "4K" in res else ("2k_boosted" if "2K" in res else ("1080p_boosted" if "1080p" in res else "boosted"))
        folder = "Videos_4K_Boosted" if "4K" in res else ("Videos_2K_Boosted" if "2K" in res else "Videos_Boosted")

        inp = self.single_input_var.get().strip()
        if inp:
            p = Path(inp)
            out_name = f"{p.stem}_{tag}{p.suffix}"
            self.single_out_var.set(os.path.normpath(str(p.parent / folder / out_name)))

        b_in = self.batch_input_var.get().strip()
        if b_in:
            self.batch_out_var.set(os.path.normpath(os.path.join(b_in, folder)))

    def _browse_single_input(self):
        f = filedialog.askopenfilename(
            title="Seleccionar Video o Imagen",
            filetypes=[("Videos e Imágenes", "*.mp4;*.mov;*.mkv;*.avi;*.webm;*.png;*.jpg;*.jpeg;*.webp"), ("Todos los archivos", "*.*")]
        )
        if f:
            self.single_input_var.set(os.path.normpath(f))
            p = Path(f)
            res_choice = self.res_var.get()
            tag = "4k_boosted" if "4K" in res_choice else ("2k_boosted" if "2K" in res_choice else ("1080p_boosted" if "1080p" in res_choice else "boosted"))
            folder = "Videos_4K_Boosted" if "4K" in res_choice else ("Videos_2K_Boosted" if "2K" in res_choice else "Videos_Boosted")
            out_name = f"{p.stem}_{tag}{p.suffix}"
            out_path = p.parent / folder / out_name
            self.single_out_var.set(os.path.normpath(str(out_path)))

            info = self._probe_media(f)
            if info:
                w, h = info.get('width', 0), info.get('height', 0)
                orient = "Vertical 9:16" if (w and h and h > w) else ("Cuadrado 1:1" if (w and h and w == h) else "Horizontal 16:9")
                if info.get("is_video"):
                    self.single_info_var.set(f"Video: {w}x{h} ({orient}) | {info['fps']} fps | {info['duration']}s")
                else:
                    self.single_info_var.set(f"Imagen: {w}x{h} ({orient})")
            else:
                self.single_info_var.set("Archivo seleccionado.")

    def _browse_single_output(self):
        f = filedialog.asksaveasfilename(
            title="Guardar archivo mejorado como",
            defaultextension=".mp4",
            filetypes=[("Video MP4", "*.mp4"), ("Imagen PNG", "*.png"), ("Todos los archivos", "*.*")]
        )
        if f:
            self.single_out_var.set(os.path.normpath(f))

    def _browse_batch_input(self):
        d = filedialog.askdirectory(title="Seleccionar Carpeta")
        if d:
            res_choice = self.res_var.get()
            folder = "Videos_4K_Boosted" if "4K" in res_choice else ("Videos_2K_Boosted" if "2K" in res_choice else "Videos_Boosted")
            self.batch_input_var.set(os.path.normpath(d))
            self.batch_out_var.set(os.path.normpath(os.path.join(d, folder)))

    def _browse_batch_output(self):
        d = filedialog.askdirectory(title="Seleccionar Carpeta Destino")
        if d:
            self.batch_out_var.set(os.path.normpath(d))

    def _open_output_dir(self):
        target = self.last_output_dir
        if not target or not os.path.exists(target):
            if self.current_tab_idx == 0:
                p = self.single_out_var.get().strip()
                target = os.path.dirname(p) if p else ""
            else:
                target = self.batch_out_var.get().strip()

        if target and os.path.exists(target):
            os.startfile(target)
        else:
            messagebox.showinfo("Aviso", "Aún no se ha generado una carpeta de destino válida.")

    def _log(self, text):
        self.msg_queue.put(("log", text))

    def _set_status(self, text, progress=None):
        self.msg_queue.put(("status", (text, progress)))

    def _process_queue(self):
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()
                if msg_type == "log":
                    self.log_area.configure(state="normal")
                    self.log_area.insert(tk.END, data + "\n")
                    self.log_area.see(tk.END)
                    self.log_area.configure(state="disabled")
                elif msg_type == "status":
                    txt, prog = data
                    self.status_var.set(txt)
                    if prog is not None:
                        self.prog_var.set(prog)
                elif msg_type == "finished":
                    self._on_finished(data)
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(100, self._process_queue)

    def _probe_media(self, file_path):
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,r_frame_rate,duration,codec_type",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1",
                file_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            lines = res.stdout.strip().splitlines()
            data = {}
            for l in lines:
                if "=" in l:
                    k, v = l.split("=", 1)
                    data[k] = v

            try:
                width = int(data.get("width", 0))
            except (ValueError, TypeError):
                width = 0

            try:
                height = int(data.get("height", 0))
            except (ValueError, TypeError):
                height = 0
            duration_val = float(data.get("duration", 0))
            is_video = duration_val > 0.1 or Path(file_path).suffix.lower() in {".mp4", ".mov", ".mkv", ".avi", ".webm"}

            r_fps = data.get("r_frame_rate", "24/1")
            if "/" in r_fps:
                num, den = r_fps.split("/")
                fps_val = round(float(num) / float(den), 2)
            else:
                fps_val = round(float(r_fps), 2)

            return {"width": width, "height": height, "fps": fps_val, "duration": round(duration_val, 2), "is_video": is_video}
        except Exception:
            return None

    def _build_vf_filter(self, in_w=0, in_h=0):
        sharp = self.sharp_var.get() / 100.0
        clarity = self.clarity_var.get() / 100.0
        denoise = self.denoise_var.get() / 100.0
        deband = self.deband_var.get() / 100.0
        color = self.color_var.get() / 100.0

        filters = []
        if deband > 0.05:
            strength = round(0.8 + deband * 2.2, 2)
            filters.append(f"gradfun={strength}:16")

        if denoise > 0.05:
            spatial = round(0.5 + denoise * 2.0, 2)
            temporal = round(1.0 + denoise * 3.5, 2)
            filters.append(f"hqdn3d={spatial}:{spatial}:{temporal}:{temporal}")

        res_choice = self.res_var.get()
        is_vert = (in_h > in_w) if (in_w > 0 and in_h > 0) else False
        is_square = (abs(in_w - in_h) < 10) if (in_w > 0 and in_h > 0) else False

        if "Auto-Adaptativo 1080p" in res_choice:
            scale_part = "-2:1920" if is_vert else ("1080:1080" if is_square else "1920:-2")
            filters.append(f"scale={scale_part}:flags=lanczos+accurate_rnd+full_chroma_int")
        elif "Auto-Adaptativo 4K" in res_choice:
            scale_part = "-2:3840" if is_vert else ("2160:2160" if is_square else "3840:-2")
            filters.append(f"scale={scale_part}:flags=lanczos+accurate_rnd+full_chroma_int")
        elif "Auto-Adaptativo 2K" in res_choice:
            scale_part = "-2:2560" if is_vert else ("1440:1440" if is_square else "2560:-2")
            filters.append(f"scale={scale_part}:flags=lanczos+accurate_rnd+full_chroma_int")
        elif "1080x1920" in res_choice:
            filters.append("scale=-2:1920:flags=lanczos+accurate_rnd+full_chroma_int")
        elif "2160x3840" in res_choice:
            filters.append("scale=-2:3840:flags=lanczos+accurate_rnd+full_chroma_int")
        elif "4K Ultra HD" in res_choice:
            filters.append("scale=3840:2160:force_original_aspect_ratio=decrease:flags=lanczos+accurate_rnd+full_chroma_int,pad=3840:2160:(ow-iw)/2:(oh-ih)/2")
        elif "4K Cinema" in res_choice:
            filters.append("scale=4096:2160:force_original_aspect_ratio=decrease:flags=lanczos+accurate_rnd+full_chroma_int,pad=4096:2160:(ow-iw)/2:(oh-ih)/2")
        elif "2K" in res_choice:
            filters.append("scale=2560:1440:force_original_aspect_ratio=decrease:flags=lanczos+accurate_rnd+full_chroma_int,pad=2560:1440:(ow-iw)/2:(oh-ih)/2")
        elif "1080p" in res_choice:
            filters.append("scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos+accurate_rnd+full_chroma_int,pad=1920:1080:(ow-iw)/2:(oh-ih)/2")

        if clarity > 0.05:
            amount = round(clarity * 0.9, 2)
            filters.append(f"unsharp=5:5:{amount}:5:5:0.0")

        if sharp > 0.05:
            cas_val = round(0.2 + sharp * 0.65, 2)
            filters.append(f"cas={cas_val}")

        if color > 0.05:
            contrast_val = round(1.0 + (color - 0.5) * 0.16, 3)
            saturation_val = round(1.0 + (color - 0.5) * 0.30, 3)
            gamma_val = round(1.0 + (color - 0.5) * 0.06, 3)
            filters.append(f"eq=contrast={contrast_val}:brightness=0.01:saturation={saturation_val}:gamma={gamma_val}")

        return ",".join(filters) if filters else "null"

    def _start_processing(self):
        if self.is_running:
            return

        res_choice = self.res_var.get()
        tag = "4k_boosted" if "4K" in res_choice else ("2k_boosted" if "2K" in res_choice else ("1080p_boosted" if "1080p" in res_choice else "boosted"))
        folder = "Videos_4K_Boosted" if "4K" in res_choice else ("Videos_2K_Boosted" if "2K" in res_choice else "Videos_Boosted")

        is_single = (self.current_tab_idx == 0)

        if is_single:
            inp = self.single_input_var.get().strip()
            out = self.single_out_var.get().strip()
            if not inp or not os.path.exists(inp):
                messagebox.showerror("Error", "Selecciona un archivo de entrada válido.")
                return
            p = Path(inp)
            default_name = Path(out).name if out else f"{p.stem}_{tag}{p.suffix}"
            out_folder = Path(out).parent if out else (p.parent / folder)

            chosen_name = prompt_rename_dialog(
                self.root,
                title="Confirmar / Renombrar Salida",
                prompt="¿Qué nombre deseas asignarle al archivo de salida?",
                default_val=default_name,
                subtext=f"Origen: {p.name}  |  Carpeta destino: {out_folder}"
            )
            if not chosen_name:
                return

            if not os.path.splitext(chosen_name)[1]:
                chosen_name += p.suffix

            out = str(out_folder / chosen_name)
            self.single_out_var.set(out)
            targets = [(inp, out)]
            self.last_output_dir = str(out_folder)
        else:
            in_dir = self.batch_input_var.get().strip()
            out_dir = self.batch_out_var.get().strip()
            if not in_dir or not os.path.exists(in_dir):
                messagebox.showerror("Error", "Selecciona una carpeta de origen válida.")
                return
            if not out_dir:
                out_dir = os.path.join(in_dir, folder)
                self.batch_out_var.set(out_dir)

            self.last_output_dir = out_dir
            raw_targets = self._find_batch_files(in_dir, out_dir, self.batch_recursive_var.get(), tag)
            if not raw_targets:
                messagebox.showwarning("Atención", "No se encontraron archivos compatibles en la carpeta.")
                return

            sample_file = Path(raw_targets[0][0])
            chosen_suffix = prompt_rename_dialog(
                self.root,
                title="Asignar Sufijo para el Lote",
                prompt=f"Se procesarán {len(raw_targets)} archivos.\n¿Qué sufijo deseas agregar al nombre de los archivos procesados?",
                default_val=f"_{tag}",
                subtext=f"Ejemplo: '{sample_file.name}' -> '{sample_file.stem}_{tag}{sample_file.suffix}'"
            )
            if chosen_suffix is None:
                return

            targets = []
            for src, dst in raw_targets:
                p_src = Path(src)
                d_dst = Path(dst).parent
                new_fname = f"{p_src.stem}{chosen_suffix}{p_src.suffix}"
                targets.append((src, str(d_dst / new_fname)))

        preset_name = self.preset_var.get()

        self.is_running = True
        self.cancel_requested = False
        self.btn_start.configure_state("disabled")
        self.btn_cancel.configure_state("normal")
        self.prog_var.set(0)

        self._log(f"\n🚀 Iniciando Video Boost: {len(targets)} archivo(s) en cola...")
        self._log(f"Perfil: {preset_name} | Resolución: {res_choice}")
        self._log(f"Acelerador: {self.hw_var.get()}")

        t = threading.Thread(target=self._worker_thread, args=(targets,), daemon=True)
        t.start()

    def _find_batch_files(self, in_dir, out_dir, recursive, tag="boosted"):
        exts = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".png", ".jpg", ".jpeg", ".webp"}
        targets = []
        in_path = Path(in_dir)

        iterator = in_path.rglob("*") if recursive else in_path.glob("*")

        for p in iterator:
            if p.is_file() and p.suffix.lower() in exts:
                if "videos_boosted" in str(p).lower() or "videos_4k_boosted" in str(p).lower() or f"_{tag}" in p.name.lower():
                    continue
                rel = p.relative_to(in_path)
                dest = Path(out_dir) / rel.parent / f"{p.stem}_{tag}{p.suffix}"
                targets.append((str(p), str(dest)))

        return targets

    def _cancel(self):
        if self.is_running:
            self.cancel_requested = True
            if self.process:
                try:
                    self.process.terminate()
                except Exception:
                    pass
            self._log("⚠️ Cancelación solicitada por el usuario.")
            self._set_status("Cancelando proceso...")

    def _get_encoder_args(self, hw_choice):
        if "NVIDIA" in hw_choice:
            codec = "hevc_nvenc" if "HEVC" in hw_choice else "h264_nvenc"
            return [
                "-c:v", codec,
                "-preset", "p7",
                "-tune", "hq",
                "-multipass", "fullres",
                "-rc", "vbr",
                "-cq", "16",
                "-b:v", "0",
                "-spatial-aq", "1",
                "-temporal-aq", "1",
                "-pix_fmt", "yuv420p"
            ]
        elif "AMD Radeon" in hw_choice:
            codec = "h264_amf"
            return [
                "-c:v", codec,
                "-quality", "quality",
                "-rc", "cqp",
                "-qp_i", "16",
                "-qp_p", "16",
                "-pix_fmt", "yuv420p"
            ]
        else:
            return [
                "-c:v", "libx264",
                "-crf", "16",
                "-preset", "slow",
                "-pix_fmt", "yuv420p"
            ]

    def _worker_thread(self, targets):
        total = len(targets)
        img_exts = {".png", ".jpg", ".jpeg", ".webp"}
        success_count = 0
        start_time = time.time()
        hw_choice = self.hw_var.get()

        for idx, (inp_path, out_path) in enumerate(targets, 1):
            if self.cancel_requested:
                break

            fname = os.path.basename(inp_path)
            self._set_status(f"Mejorando [{idx}/{total}]: {fname}", progress=((idx - 1) / total) * 100)
            self._log(f"\n▶ [{idx}/{total}] Procesando: {fname}")

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            is_image = Path(inp_path).suffix.lower() in img_exts

            info = self._probe_media(inp_path)
            in_w = info["width"] if info else 0
            in_h = info["height"] if info else 0
            duration = info["duration"] if info else 0

            if in_w > 0 and in_h > 0:
                orient_tag = "📱 Vertical (9:16)" if in_h > in_w else ("⏹ Cuadrado (1:1)" if in_w == in_h else "🖥 Horizontal (16:9)")
                self._log(f"  Geometría origen: {in_w}x{in_h} [{orient_tag}]")

            vf = self._build_vf_filter(in_w, in_h)

            if is_image:
                cmd = [
                    "ffmpeg", "-y", "-hide_banner",
                    "-i", inp_path,
                    "-vf", vf,
                    "-frames:v", "1",
                    "-update", "1",
                    out_path
                ]
            else:
                enc_args = self._get_encoder_args(hw_choice)

                cmd = [
                    "ffmpeg", "-y", "-hide_banner",
                    "-i", inp_path,
                    "-vf", vf
                ] + enc_args + [
                    "-map", "0:v:0",
                    "-map", "0:a?",
                    "-c:a", "copy",
                    out_path
                ]

            try:
                creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True, creationflags=creation_flags)

                time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

                while True:
                    line = self.process.stderr.readline()
                    if not line and self.process.poll() is not None:
                        break
                    if line and not is_image and duration > 0:
                        m = time_pattern.search(line)
                        if m:
                            hours, mins, secs = float(m.group(1)), float(m.group(2)), float(m.group(3))
                            curr_time = hours * 3600 + mins * 60 + secs
                            clip_pct = min(curr_time / duration, 1.0)
                            overall_pct = ((idx - 1 + clip_pct) / total) * 100
                            self._set_status(f"Mejorando [{idx}/{total}]: {fname} ({int(clip_pct*100)}%)", progress=overall_pct)

                self.process.wait()
                if self.process.returncode == 0:
                    success_count += 1
                    self._log(f"  ✓ Guardado: {os.path.basename(out_path)}")
                else:
                    if not self.cancel_requested and ("NVIDIA" in hw_choice or "AMD" in hw_choice):
                        self._log("  ⚠️ Hardware GPU no compatible en este sistema. Reintentando con CPU de alta fidelidad...")
                        fallback_cmd = [
                            "ffmpeg", "-y", "-hide_banner",
                            "-i", inp_path,
                            "-vf", vf,
                            "-c:v", "libx264",
                            "-crf", "16",
                            "-preset", "slow",
                            "-pix_fmt", "yuv420p",
                            "-map", "0:v:0",
                            "-map", "0:a?",
                            "-c:a", "copy",
                            out_path
                        ]
                        self.process = subprocess.Popen(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True, creationflags=creation_flags)
                        while True:
                            line = self.process.stderr.readline()
                            if not line and self.process.poll() is not None:
                                break
                        self.process.wait()
                        if self.process.returncode == 0:
                            success_count += 1
                            self._log(f"  ✓ Guardado (CPU): {os.path.basename(out_path)}")
                        else:
                            self._log(f"  ✗ Error al procesar {fname}")
                    else:
                        if not self.cancel_requested:
                            self._log(f"  ✗ Error al procesar {fname}")
            except Exception as e:
                self._log(f"  ✗ Excepción: {e}")

        total_time = round(time.time() - start_time, 1)
        self.msg_queue.put(("finished", (success_count, total, total_time, self.cancel_requested)))

    def _on_finished(self, data):
        success_count, total, total_time, was_cancelled = data
        self.is_running = False
        self.btn_start.configure_state("normal")
        self.btn_cancel.configure_state("disabled")

        if was_cancelled:
            self._set_status("Operación cancelada.", progress=0)
            self._log(f"\n⚠️ Proceso interrumpido. Completados: {success_count} de {total}.")
        else:
            self.prog_var.set(100)
            self._set_status(f"¡Completado! {success_count}/{total} archivos potenciados en {total_time}s.", progress=100)
            self._log(f"\n✨ ¡Video Boost finalizado con éxito! {success_count} archivo(s) mejorados en {total_time} segundos.")
            messagebox.showinfo("Proceso Completado", f"Se aplicó Video Boost a {success_count} de {total} archivos con éxito.\n\nTiempo total: {total_time}s")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoBoosterApp(root)
    root.mainloop()
