# LLMJazzImprovEvaluation
This repository accompanies the research paper "Computational Analysis of Jazz Improvisation: Integrating CREPE Pitch Detection with Language Model Feedback." This research prototype generates structured feedback for jazz improvisations by combining automatic pitch estimation with LLM feedback.
The system converts an uploaded audio recording into a symbolic representation of notes using the CREPE pitch estimation model, aligns the transcription with a user-provided chord progression, and uses a large language model to analyze phrase structure, harmonic alignment, motif development, and opportunities for improvement.


Pipeline

Audio Recording
      ->
CREPE Pitch Detection
      ->
Note Segmentation
      ->
Chord Timeline Construction
      ->
Symbolic Representation
      ->
LLM Analysis
      ->
Structured Feedback

Features
1. Monophonic pitch transcription using CREPE
2. Automatic note segmentation
3. Harmonic alignment using user-defined chord progressions
4. LLM-generated feedback on:
      -Phrase structure
      -Motif development
      -Harmonic alignment
      -Actionable suggestions for improvement

Repository Contents
1. Pitch extraction and note segmentation
2. Chord timeline generation
3. LLM Prompt
4. Example Response
5. Citation

If you use this repository in academic work, please cite the accompanying paper once it becomes available.
