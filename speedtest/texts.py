"""Curated prompts grouped by category and difficulty."""
import random

PROMPTS = {
    "easy": [
        "The quick brown fox jumps over the lazy dog near the river bank.",
        "Sunlight filtered through the green leaves of the quiet forest.",
        "Early birds catch the morning dew while the city is still asleep.",
        "Simple habits practiced every day bring meaningful progress over time."
    ],
    "medium": [
        "Software engineering is fundamentally about managing complexity and communicating intent.",
        "Resilience is not the absence of difficulty, but the capacity to recover from adversity quickly.",
        "Curiosity fuels discovery, transforming ordinary questions into profound scientific breakthroughs.",
        "Clear typography and balanced whitespace create digital interfaces that feel calm and intuitive."
    ],
    "hard": [
        "Cryptographic protocols depend upon computational hardness assumptions such as discrete logarithms.",
        "Asynchronous event loops multiplex input and output operations without preemptive multithreading overhead.",
        "Quantum entanglement demonstrates non-local statistical correlations that challenge classical intuitions.",
        "Heuristic optimization algorithms balance exploitation of known optima with exploration of search space."
    ]
}

def get_random_prompt(difficulty: str = "medium") -> str:
    """Retrieve a prompt matching difficulty, defaulting to medium."""
    difficulty = difficulty.lower()
    pool = PROMPTS.get(difficulty, PROMPTS["medium"])
    return random.choice(pool)
