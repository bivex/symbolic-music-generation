import os
from pathlib import Path
from music21 import converter, stream

def merge_midi_files(bass_path, melody_path, output_path):
    print(f"Merging:\n  Bass: {bass_path}\n  Melody: {melody_path}\nTarget: {output_path}")
    
    # Load the MIDI files
    score_bass = converter.parse(bass_path)
    score_melody = converter.parse(melody_path)
    
    # Combine them into a single score
    combined_score = stream.Score()
    
    # Add bass part
    for element in score_bass.elements:
        combined_score.insert(0, element)
        
    # Add melody part
    for element in score_melody.elements:
        combined_score.insert(0, element)
        
    # Write output MIDI
    combined_score.write('midi', fp=output_path)
    print("Success: Merged MIDI saved successfully!")

def main():
    epoch = 400
    bass_dir = Path("samples/chord2sequentialbass_first_samples/generated_midis_400/bass")
    melody_dir = Path("samples/chord2sequentialbass_first_samples/generated_midis_400/melody")
    output_dir = Path("samples/chord2sequentialbass_first_samples/generated_midis_400/combined")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all midi files in bass directory
    bass_files = list(bass_dir.glob("*.mid"))
    
    if not bass_files:
        print("No generated MIDI files found in bass directory.")
        return
        
    for bass_file in bass_files:
        name = bass_file.name
        melody_file = melody_dir / name
        
        if melody_file.exists():
            output_file = output_dir / name
            try:
                merge_midi_files(str(bass_file), str(melody_file), str(output_file))
            except Exception as e:
                print(f"Error merging {name}: {e}")
        else:
            print(f"Warning: Melody file not found for {name}")

if __name__ == "__main__":
    main()
