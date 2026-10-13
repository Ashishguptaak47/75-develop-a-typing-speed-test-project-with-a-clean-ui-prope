"""Unit tests for Typing Speed Test logic and metrics."""
import pytest
from speedtest.engine import TypingEngine
from speedtest.texts import get_random_prompt, PROMPTS


def test_get_random_prompt():
    easy_text = get_random_prompt("easy")
    assert easy_text in PROMPTS["easy"]

    medium_text = get_random_prompt("medium")
    assert medium_text in PROMPTS["medium"]

    # Fallback to medium on unknown difficulty
    unknown = get_random_prompt("extreme_unknown")
    assert unknown in PROMPTS["medium"]


def test_engine_perfect_match():
    text = "Hello World"
    engine = TypingEngine(text)
    engine.start_time = 100.0
    engine.end_time = 160.0  # exactly 60 seconds (1 minute)
    engine.typed_text = "Hello World"
    engine.is_completed = True

    metrics = engine.calculate_metrics()
    # 11 keystrokes / 5 = 2.2 words in 1 min => 2.2 WPM
    assert metrics.gross_wpm == 2.2
    assert metrics.net_wpm == 2.2
    assert metrics.accuracy_percentage == 100.0
    assert metrics.error_chars == 0
    assert metrics.correct_chars == 11


def test_engine_errors_calculation():
    text = "Apple"
    engine = TypingEngine(text)
    engine.start_time = 0.0
    engine.end_time = 30.0  # 0.5 minutes
    engine.typed_text = "Appxx"  # 3 correct, 2 errors
    engine.is_completed = True

    metrics = engine.calculate_metrics()
    assert metrics.correct_chars == 3
    assert metrics.error_chars == 2
    assert metrics.accuracy_percentage == 60.0
    # Gross: (5/5) / 0.5 = 2.0 WPM
    # Net: max(0, ((5/5) - 2) / 0.5) = 0.0 WPM
    assert metrics.gross_wpm == 2.0
    assert metrics.net_wpm == 0.0


def test_engine_character_status_highlighting():
    target = "cat"
    engine = TypingEngine(target)
    engine.typed_text = "cz"

    statuses = engine.get_character_status()
    assert statuses == [
        ("c", "correct"),
        ("a", "error"),
        ("t", "current"),
    ]


def test_engine_auto_completion():
    engine = TypingEngine("test")
    engine.update("test")
    assert engine.is_completed is True
    assert engine.end_time > 0
