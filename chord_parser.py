import torch

ROOT_MAP = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
    "Fm": 5,  # Fallback: treat Fm:maj as F major
}


def chord_to_chroma(chord_str):
    """
    Converts a single chord string (e.g., 'C:min', 'G:maj/3', 'Ab:maj') into a 12-dimensional chroma vector.
    """
    chroma = [0.0] * 12
    if not chord_str:
        return chroma

    chord_str = chord_str.strip()
    if chord_str in [
        "[PAD]",
        "[UNK]",
        "[CLS]",
        "[SEP]",
        "[MASK]",
        "NA",
        "N",
        "pad",
        "unk",
        "",
    ]:
        return chroma

    # Split root and quality
    if ":" in chord_str:
        root, quality = chord_str.split(":", 1)
    else:
        root = chord_str
        quality = "maj"  # default to major

    # Handle slash chords like G:maj/3
    if "/" in quality:
        quality = quality.split("/", 1)[0]

    root_val = ROOT_MAP.get(root, None)
    if root_val is None:
        return chroma

    # Determine intervals based on quality
    q = quality.lower()
    if q in ["min", "m", "minor"]:
        intervals = [0, 3, 7]
    elif q in ["dim", "diminished"]:
        intervals = [0, 3, 6]
    elif q in ["aug", "augmented"]:
        intervals = [0, 4, 8]
    elif q in ["maj7", "major7"]:
        intervals = [0, 4, 7, 11]
    elif q in ["min7", "minor7"]:
        intervals = [0, 3, 7, 10]
    elif q in ["7", "dom7"]:
        intervals = [0, 4, 7, 10]
    else:
        # Default fallback to major
        intervals = [0, 4, 7]

    for interval in intervals:
        chroma[(root_val + interval) % 12] = 1.0

    return chroma


def parse_chord_progression(chord_prog_str, max_length=128):
    """
    Parses a full chord progression string (e.g., 'C:min G:maj C:min')
    and returns padded chroma vectors and attention mask.
    """
    if not isinstance(chord_prog_str, str):
        chord_prog_str = ""

    tokens = chord_prog_str.strip().split()

    chromas = []
    attn_mask = []

    for token in tokens:
        chromas.append(chord_to_chroma(token))
        attn_mask.append(1.0)

    # Pad or truncate
    if len(chromas) < max_length:
        pad_len = max_length - len(chromas)
        chromas += [[0.0] * 12] * pad_len
        attn_mask += [0.0] * pad_len
    else:
        chromas = chromas[:max_length]
        attn_mask = attn_mask[:max_length]

    return chromas, attn_mask
