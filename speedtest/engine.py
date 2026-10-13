"""Core typing performance metrics calculation engine."""
from dataclasses import dataclass
import time
from typing import List, Tuple


@dataclass
class TestResult:
    target_text: str
    typed_text: str
    duration_seconds: float
    gross_wpm: float
    net_wpm: float
    accuracy_percentage: float
    correct_chars: int
    error_chars: int
    total_keystrokes: int


class TypingEngine:
    """Tracks typing sessions and produces rigorous speed/accuracy metrics."""

    def __init__(self, target_text: str):
        self.target_text: str = target_text
        self.typed_text: str = ""
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.is_active: bool = False
        self.is_completed: bool = False

    def start(self) -> None:
        """Begin tracking typing session."""
        self.start_time = time.perf_counter()
        self.end_time = 0.0
        self.is_active = True
        self.is_completed = False
        self.typed_text = ""

    def update(self, current_text: str) -> None:
        """Record current typed text buffer."""
        if not self.is_active and not self.is_completed:
            self.start()
        self.typed_text = current_text
        if len(self.typed_text) >= len(self.target_text):
            self.finish()

    def finish(self) -> None:
        """Stop tracking typing session."""
        if self.is_active:
            self.end_time = time.perf_counter()
            self.is_active = False
            self.is_completed = True
        elif not self.is_completed:
            self.end_time = self.start_time
            self.is_completed = True

    def get_elapsed_seconds(self) -> float:
        """Get elapsed duration in seconds."""
        if self.start_time == 0.0:
            return 0.0
        if self.is_active:
            return max(0.001, time.perf_counter() - self.start_time)
        if self.end_time > 0.0:
            return max(0.001, self.end_time - self.start_time)
        return 0.001

    def evaluate_characters(self) -> Tuple[int, int]:
        """Return tuple of (correct_count, error_count) based on current typed text."""
        correct = 0
        errors = 0
        for i, typed_char in enumerate(self.typed_text):
            if i < len(self.target_text):
                if typed_char == self.target_text[i]:
                    correct += 1
                else:
                    errors += 1
            else:
                errors += 1
        return correct, errors

    def get_character_status(self) -> List[Tuple[str, str]]:
        """
        Return list of tuples (char, status) for rendering target text.
        Status can be 'correct', 'error', 'current', or 'pending'.
        """
        status_list: List[Tuple[str, str]] = []
        typed_len = len(self.typed_text)

        for i, ch in enumerate(self.target_text):
            if i < typed_len:
                status = "correct" if self.typed_text[i] == ch else "error"
            elif i == typed_len:
                status = "current"
            else:
                status = "pending"
            status_list.append((ch, status))
        return status_list

    def calculate_metrics(self) -> TestResult:
        """Calculate standardized gross WPM, net WPM, and accuracy metrics."""
        elapsed = self.get_elapsed_seconds()
        minutes = elapsed / 60.0 if elapsed > 0 else 1.0 / 60.0

        correct, errors = self.evaluate_characters()
        total_keystrokes = len(self.typed_text)

        # Standard convention: 1 word = 5 keystrokes
        gross_wpm = (total_keystrokes / 5.0) / minutes
        net_wpm = max(0.0, ((total_keystrokes / 5.0) - errors) / minutes)

        accuracy = (correct / total_keystrokes * 100.0) if total_keystrokes > 0 else 100.0

        return TestResult(
            target_text=self.target_text,
            typed_text=self.typed_text,
            duration_seconds=round(elapsed, 2),
            gross_wpm=round(gross_wpm, 1),
            net_wpm=round(net_wpm, 1),
            accuracy_percentage=round(accuracy, 1),
            correct_chars=correct,
            error_chars=errors,
            total_keystrokes=total_keystrokes,
        )
