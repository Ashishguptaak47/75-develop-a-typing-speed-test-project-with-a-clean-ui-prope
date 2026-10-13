"""Application entry point supporting both GUI and interactive CLI modes."""
import argparse
import sys
import time
from speedtest.engine import TypingEngine
from speedtest.texts import get_random_prompt


def run_cli_test(difficulty: str = "medium") -> None:
    """Run an interactive terminal typing test."""
    prompt = get_random_prompt(difficulty)
    print("=" * 60)
    print(f"TYPING SPEED TEST (Difficulty: {difficulty.upper()})")
    print("=" * 60)
    print("Type the following text exactly as shown. Press ENTER when finished:\n")
    print(f">>> {prompt}\n")
    input("Press ENTER to begin...")
    print("\nTimer started! Type now:\n")

    start = time.perf_counter()
    typed = input()
    end = time.perf_counter()

    engine = TypingEngine(prompt)
    engine.start_time = start
    engine.end_time = end
    engine.typed_text = typed
    engine.is_completed = True

    metrics = engine.calculate_metrics()
    print("\n" + "=" * 60)
    print("RESULTS:")
    print(f"- Net Speed:        {metrics.net_wpm} WPM")
    print(f"- Gross Speed:      {metrics.gross_wpm} WPM")
    print(f"- Accuracy:         {metrics.accuracy_percentage}%")
    print(f"- Time:             {metrics.duration_seconds}s")
    print(f"- Keystrokes:       {metrics.total_keystrokes}")
    print(f"- Errors:           {metrics.error_chars}")
    print("=" * 60)


def run_gui() -> None:
    """Launch Tkinter GUI with graceful fallback if display unavailable."""
    try:
        import tkinter as tk
        from speedtest.ui import TypingTestUI

        root = tk.Tk()
        app = TypingTestUI(root)
        root.mainloop()
    except tk.TclError as exc:
        print(f"Unable to initialize graphical environment: {exc}")
        print("Falling back to CLI mode...\n")
        run_cli_test()


def main() -> None:
    parser = argparse.ArgumentParser(description="Speed Typing Test")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode instead of GUI")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Prompt difficulty level",
    )
    args = parser.parse_args()

    if args.cli:
        run_cli_test(args.difficulty)
    else:
        run_gui()


if __name__ == "__main__":
    main()
