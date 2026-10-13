# Speed Type Master (Typing Speed Test)

A clean, modern Typing Speed Test application implemented in Python with both a dark-mode graphical UI (`Tkinter`) and an interactive CLI mode.

## Features

- **Modern Dark UI**: Fluid, card-based interface with real-time target character highlighting (`correct`, `mistake`, `active cursor`).
- **Live Metric Calculations**:
  - Net Words Per Minute (Net WPM)
  - Gross Words Per Minute (Gross WPM)
  - Accuracy Percentage (%)
  - Elapsed Time Counter & Mistake Tracker
- **Multiple Difficulty Tiers**: `easy`, `medium`, and `hard` prompts.
- **Robust Fallback**: Automatically switches to CLI mode if no graphical display server is detected.
- **Modular Design & Testing**: Fully unit-tested typing engine.

## Directory Structure

```text
.
├── speedtest/
│   ├── __init__.py
│   ├── engine.py        # WPM & accuracy metric calculator
│   ├── texts.py         # Curated typing prompts
│   └── ui.py            # Custom styled Tkinter interface
├── tests/
│   └── test_main.py     # Pytest unit tests
├── main.py              # CLI/GUI launcher
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites
Python 3.8 or later.

### Installation
1. Clone or download the repository.
2. Optional: Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

- **GUI Mode (Default)**:
  ```bash
  python main.py
  ```

- **Terminal / CLI Mode**:
  ```bash
  python main.py --cli --difficulty hard
  ```

### Running Tests

```bash
pytest
```
