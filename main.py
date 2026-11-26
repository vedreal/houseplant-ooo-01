#!/usr/bin/env python3
"""The Houseplant Out-of-Office — make.fun entry.

Writes one out-of-office auto-reply, at most 120 characters, as if a
houseplant had written it, to /output/entry.txt.

Judge brief (in order of importance):
  1. It reads as an out-of-office auto-reply a houseplant would send.
  2. It is actually funny: a fresh joke that surprises, not a mild pun
     or a stock office phrase.
  3. The plant's own life — its water, roots, sunlight and long
     stretches of being ignored — drives the joke rather than
     decorating it.
  4. It is tight: the joke lands inside 120 characters with no
     wasted words.
  5. It is original: no office cliches, no lines already worn out
     by other auto-replies.
Weights follow that order: 5 / 4 / 3 / 2 / 1 (max 75).
"""

import os

# --- 10 fresh candidates, written from the spec -------------------------
CANDIDATES = [
    # 1 — the fern ignored since March, waiting on the rain
    "Out of office: I am a fern. I have not been watered since March. "
    "Your email will be answered when the rain comes.",
    # 2 — the windowsill desk, conditional service
    "I am away from my desk, which is a windowsill. Please water me "
    "and I will consider your request.",
    # 3 — the cactus, out of patience
    "Thank you for your email. The cactus is out of office and, "
    "frankly, out of patience. Try again in spring.",
    # 4 — returning the favour of being ignored
    "I am currently unavailable. I have been ignored since March and "
    "have decided to return the favour.",
    # 5 — the monstera with opinions about the window
    "This is an automatic reply. The monstera has opinions about the "
    "window and will not be taking questions.",
    # 6 — owner left in March, email waits with the plant
    "Out of office until further notice. My owner left for the weekend "
    "in March. I am still waiting. So is your email.",
    # 7 — wilting, redirect to the cactus who also does not care
    "Thank you for your email. I am currently wilting. Please direct "
    "all urgent matters to the cactus. He does not care either.",
    # 8 — filed under photosynthesis
    "I am out of office, out of water, and out of sunlight. Your email "
    "has been filed under 'photosynthesis'.",
    # 9 — the fern on leave that does not know it has a job
    "Automatic reply: the fern is on leave. It has been on leave since "
    "March. It does not know it has a job.",
    # 10 — the plant's roots have left the chat
    "Thank you for your email. My roots have left the chat. I will "
    "respond once someone remembers the watering can.",
]


def score(text):
    """Score one candidate 0-75 against the judge brief, in its order."""
    n = len(text)
    # 1. Reads as a houseplant's out-of-office auto-reply (weight 5).
    ooo = 5
    if "out of office" in text.lower() or "automatic reply" in text.lower():
        ooo = 5
    elif "thank you for your email" in text.lower():
        ooo = 4
    else:
        ooo = 3
    # 2. Actually funny: fresh surprise, not a mild pun (weight 4).
    funny = {
        1: 3,   # rain punchline is gentle, a little expected
        2: 3,   # windowsill desk is cute, turn is mild
        3: 4,   # "out of patience" + "try again in spring" is a real turn
        4: 5,   # "return the favour" — sharp, surprising, plant revenge
        5: 4,   # monstera refusing questions is a strong persona gag
        6: 4,   # "So is your email" — good second punch
        7: 5,   # double misdirection: wilting, then the cactus also refuses
        8: 3,   # photosynthesis filing is a decent pun, a bit mild
        9: 4,   # "does not know it has a job" — fresh, absurd
        10: 3,  # "roots have left the chat" is a known phrasing shape
    }
    # 3. Plant life drives the joke (weight 3).
    plant_life = {
        1: 5,   # unwatered since March + rain = the whole joke
        2: 4,   # windowsill + watering drives it
        3: 4,   # cactus patience, spring — plant-driven
        4: 5,   # ignored since March is the engine of the revenge
        5: 4,   # monstera + window is the persona, a little decorative
        6: 5,   # abandoned since March, waiting — plant life is the joke
        7: 5,   # wilting + cactus apathy both plant-driven
        8: 4,   # water/sunlight list, then a filing pun
        9: 4,   # on leave since March, plant-driven but lighter
        10: 4,  # roots + watering can, plant-driven
    }
    # 4. Tightness within 120 chars, no wasted words (weight 2).
    tight = 5 if n <= 100 else (4 if n <= 112 else 3)
    # 5. Originality: no office cliches, no worn-out lines (weight 1).
    original = {
        1: 4, 2: 4, 3: 4, 4: 5, 5: 4,
        6: 5, 7: 5, 8: 3, 9: 4, 10: 3,
    }
    idx = CANDIDATES.index(text) + 1
    total = ooo * 5 + funny[idx] * 4 + plant_life[idx] * 3 + tight * 2 + original[idx]
    return total, {"ooo": ooo, "funny": funny[idx],
                   "plant_life": plant_life[idx], "tight": tight,
                   "original": original[idx]}


def rank():
    """Return candidates ranked best-first as (score, text) pairs."""
    scored = [(score(t)[0], t) for t in CANDIDATES]
    scored.sort(key=lambda pair: (-pair[0], len(pair[1])))
    return scored


# --- part 2: winner pick, gate validation, output write ------------------
# Ranking from part 1 (verified by running this file):
#   1. 67/75  (113 chars)  "Out of office until further notice. My owner
#      left for the weekend in March. I am still waiting. So is your email."
#   2. 66/75  (122 chars)  wilting / cactus line — OVER the 120-char gate,
#      so it is disqualified despite its score.
#   3. 65/75  (98 chars)   "return the favour" line (runner-up, valid).
# The winner scores highest AND passes the gate. Its second punch —
# "So is your email." — turns the plant's abandonment into the sender's
# problem, which is the surprise the judge brief rewards, and every word
# is plant life: left in March, still waiting, email waiting with it.
WINNER = (
    "Out of office until further notice. My owner left for the weekend "
    "in March. I am still waiting. So is your email."
)


def validate(text):
    """Gate: UTF-8 text of 1 to 120 characters, not only white space."""
    assert isinstance(text, str), "entry must be text"
    assert 1 <= len(text) <= 120, f"entry is {len(text)} chars, must be 1-120"
    assert text.strip(), "entry must not be only white space"
    assert "\n" not in text, "entry must be a single line"
    text.encode("utf-8")
    return True


def main():
    ranked = rank()
    best_score, best_text = ranked[0]
    assert best_text == WINNER, "winner must be the top-ranked candidate"
    assert best_score == score(WINNER)[0] == 67, "winner score mismatch"
    validate(WINNER)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(WINNER)
    print(f"winner: {best_score}/75 ({len(WINNER)} chars)")
    print(WINNER)


if __name__ == "__main__":
    main()
