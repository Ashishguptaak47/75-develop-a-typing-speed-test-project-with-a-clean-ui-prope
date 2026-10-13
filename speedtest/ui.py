"""Modern graphical user interface for the Typing Speed Test."""
import tkinter as tk
from tkinter import ttk, messagebox
from speedtest.engine import TypingEngine
from speedtest.texts import get_random_prompt


class TypingTestUI:
    """Modern Dark-Themed GUI using Tkinter."""

    # Color Palette
    BG_COLOR = "#121826"
    CARD_COLOR = "#1E293B"
    TEXT_MUTED = "#64748B"
    TEXT_PENDING = "#94A3B8"
    TEXT_CORRECT = "#10B981"
    TEXT_ERROR = "#EF4444"
    ACCENT_COLOR = "#3B82F6"
    ACCENT_HOVER = "#2563EB"
    TEXT_LIGHT = "#F8FAFC"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("880x620")
        self.root.minsize(720, 520)
        self.root.configure(bg=self.BG_COLOR)

        self.difficulty_var = tk.StringVar(value="medium")
        self.engine: TypingEngine = TypingEngine(get_random_prompt("medium"))
        self.timer_id = None

        self._setup_styles()
        self._build_ui()
        self._reset_test()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=self.CARD_COLOR,
            background=self.CARD_COLOR,
            foreground=self.TEXT_LIGHT,
            darkcolor=self.CARD_COLOR,
            lightcolor=self.CARD_COLOR,
            arrowcolor=self.TEXT_LIGHT,
        )

    def _build_ui(self) -> None:
        # Header Frame
        header = tk.Frame(self.root, bg=self.BG_COLOR)
        header.pack(fill=tk.X, padx=30, pady=(24, 12))

        title = tk.Label(
            header,
            text="⚡ SPEED TYPE MASTER",
            font=("Helvetica", 18, "bold"),
            fg=self.TEXT_LIGHT,
            bg=self.BG_COLOR,
        )
        title.pack(side=tk.LEFT)

        ctrl_box = tk.Frame(header, bg=self.BG_COLOR)
        ctrl_box.pack(side=tk.RIGHT)

        diff_lbl = tk.Label(
            ctrl_box,
            text="Difficulty:",
            font=("Helvetica", 11),
            fg=self.TEXT_MUTED,
            bg=self.BG_COLOR,
        )
        diff_lbl.pack(side=tk.LEFT, padx=(0, 8))

        diff_menu = ttk.Combobox(
            ctrl_box,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=9,
        )
        diff_menu.pack(side=tk.LEFT, padx=(0, 10))
        diff_menu.bind("<<ComboboxSelected>>", lambda e: self._reset_test())

        # Metric Cards
        metrics_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        metrics_frame.pack(fill=tk.X, padx=30, pady=10)
        metrics_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.card_wpm = self._create_card(metrics_frame, 0, "NET WPM", "0")
        self.card_acc = self._create_card(metrics_frame, 1, "ACCURACY", "100%")
        self.card_time = self._create_card(metrics_frame, 2, "TIME", "0.0s")
        self.card_errors = self._create_card(metrics_frame, 3, "ERRORS", "0")

        # Target Text Display (Canvas or Text Box with tags)
        display_container = tk.Frame(self.root, bg=self.CARD_COLOR, padx=16, pady=16)
        display_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        self.text_display = tk.Text(
            display_container,
            wrap=tk.WORD,
            bg=self.CARD_COLOR,
            fg=self.TEXT_PENDING,
            font=("Courier", 15),
            relief=tk.FLAT,
            padx=8,
            pady=8,
            height=5,
            state=tk.DISABLED,
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # Configure Text Tags for Highlighting
        self.text_display.tag_config("correct", foreground=self.TEXT_CORRECT)
        self.text_display.tag_config("error", foreground=self.TEXT_ERROR, underline=True)
        self.text_display.tag_config("current", background="#334155", foreground="#FFFFFF")
        self.text_display.tag_config("pending", foreground=self.TEXT_PENDING)

        # Input Entry Field
        input_box_frame = tk.Frame(self.root, bg=self.CARD_COLOR, padx=16, pady=12)
        input_box_frame.pack(fill=tk.X, padx=30, pady=(6, 12))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            input_box_frame,
            textvariable=self.entry_var,
            font=("Courier", 14),
            bg="#0F172A",
            fg=self.TEXT_LIGHT,
            insertbackground=self.ACCENT_COLOR,
            relief=tk.FLAT,
        )
        self.entry.pack(fill=tk.X, ipady=8)
        self.entry.bind("<KeyRelease>", self._on_key_release)

        # Action Buttons
        action_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        action_frame.pack(fill=tk.X, padx=30, pady=(0, 24))

        btn_restart = tk.Button(
            action_frame,
            text="Restart Test",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white",
            activebackground=self.ACCENT_HOVER,
            activeforeground="white",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self._reset_test,
        )
        btn_restart.pack(side=tk.LEFT)

        btn_new_text = tk.Button(
            action_frame,
            text="New Prompt",
            font=("Helvetica", 11),
            bg="#334155",
            fg=self.TEXT_LIGHT,
            activebackground="#475569",
            activeforeground="white",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=lambda: self._reset_test(change_text=True),
        )
        btn_new_text.pack(side=tk.LEFT, padx=10)

    def _create_card(self, parent: tk.Frame, col: int, label: str, init_val: str) -> tk.Label:
        card = tk.Frame(parent, bg=self.CARD_COLOR, padx=14, pady=10)
        card.grid(row=0, column=col, sticky="nsew", padx=6)

        lbl_title = tk.Label(
            card, text=label, font=("Helvetica", 9, "bold"), fg=self.TEXT_MUTED, bg=self.CARD_COLOR
        )
        lbl_title.pack()

        val_lbl = tk.Label(
            card, text=init_val, font=("Helvetica", 18, "bold"), fg=self.TEXT_LIGHT, bg=self.CARD_COLOR
        )
        val_lbl.pack(pady=(4, 0))
        return val_lbl

    def _reset_test(self, change_text: bool = True) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if change_text or not hasattr(self, "engine"):
            target = get_random_prompt(self.difficulty_var.get())
            self.engine = TypingEngine(target)
        else:
            self.engine = TypingEngine(self.engine.target_text)

        self.entry_var.set("")
        self.entry.config(state=tk.NORMAL)
        self.entry.focus_set()

        self._render_text_display()
        self._update_metric_labels(0.0, 100.0, 0.0, 0)

    def _render_text_display(self) -> None:
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)

        status_list = self.engine.get_character_status()
        for ch, status in status_list:
            self.text_display.insert(tk.END, ch, status)

        self.text_display.config(state=tk.DISABLED)

    def _on_key_release(self, event=None) -> None:
        typed = self.entry_var.get()
        if not self.engine.is_active and not self.engine.is_completed and len(typed) > 0:
            self.engine.start()
            self._tick_timer()

        self.engine.update(typed)
        self._render_text_display()

        metrics = self.engine.calculate_metrics()
        self._update_metric_labels(
            metrics.net_wpm,
            metrics.accuracy_percentage,
            metrics.duration_seconds,
            metrics.error_chars,
        )

        if self.engine.is_completed:
            self._on_completed(metrics)

    def _tick_timer(self) -> None:
        if self.engine.is_active:
            metrics = self.engine.calculate_metrics()
            self._update_metric_labels(
                metrics.net_wpm,
                metrics.accuracy_percentage,
                metrics.duration_seconds,
                metrics.error_chars,
            )
            self.timer_id = self.root.after(100, self._tick_timer)

    def _update_metric_labels(self, wpm: float, acc: float, elapsed: float, errors: int) -> None:
        self.card_wpm.config(text=f"{wpm:.0f}")
        self.card_acc.config(text=f"{acc:.0f}%")
        self.card_time.config(text=f"{elapsed:.1f}s")
        self.card_errors.config(text=str(errors))

    def _on_completed(self, result) -> None:
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.entry.config(state=tk.DISABLED)
        summary = (
            f"🎉 Test Finished!\n\n"
            f"Net Speed: {result.net_wpm:.1f} WPM\n"
            f"Gross Speed: {result.gross_wpm:.1f} WPM\n"
            f"Accuracy: {result.accuracy_percentage:.1f}%\n"
            f"Total Time: {result.duration_seconds:.2f} seconds\n"
            f"Mistakes: {result.error_chars}"
        )
        messagebox.showinfo("Results Summary", summary)
