# Meeting transcriber exercise

Homework for the Budapest University of Technology and Economics: Prompt Engineering (VITMAV82) subject

## Homework listing

Azonosító: 1

Webapplikáció, amelyben jelezni lehet a felszólalási igényünket egy gyűlésen, súlyozottan sorrendbe állítja a
felszólalókat és nagy nyelvi modell segítségével rögzíti és formázza a felszólalásokat egy jegyzőkönyv formájában.

## Authors

- Hegedűs András: \[nomad-at-you\] Environment setup and documentation
- Farkas Martin: \[BlackLight54\] Prompting and research

## Description of solution

## Solution

Our solution is available on GitHub: https://github.com/BlackLight54/meeting-transcriber-exercise

### Architecture

First we planned the architecture and data flow of our solution.

We decided that the meeting audio is recorded in a single audio file, which is converted to text using a text-to-speech
model which supports diarization(i.e. speaker identification).

The text is then processed by a language model to correct
any errors and to format the text into a more standardized form to be used during prompting.

Then the corrected and formatted text is passed to a language model along with optional data about the meeting, and a
prompt to generate meeting minutes.

The minutes are structured according to a methodology we used successfully in the past, which we will detail later.

### Speech-to-text solutions that support diarization

We researched the available speech-to-text solutions that support diarization, and evaluated them on our own recorded
audio samples, both in English and Hungarian.

#### insanely-fast-whisper

Repository: https://github.com/Vaibhavs10/insanely-fast-whisper
Used models:

- https://huggingface.co/openai/whisper-large-v3
- https://huggingface.co/pyannote/speaker-diarization-3.1
- https://huggingface.co/pyannote/segmentation-3.0

Evaluation: `./text-to-speech-insanely-fast-whisper.ipynb`

We tried English and Hungarian audio samples, and samples with multiple speakers. We found that with low quality audio,
or with speakers with similar voices, it is hard to differentiate between speakers, and the model sometimes fails to
identify speakers correctly. Still, it was above our expectations.

### Language models

We used OpenAI's language model for text correction and formatting, and for generating the minutes, as we already had
access to them through the OpenAI API.

### Prompting techniques

prompting: `./prompting.ipynb`

We used a few prompting techniques that we learned during the course, including:

- One- and Few-shot prompting
- System and user prompts
- Separation of actions ~ Prompt-chaining, Chain-of-thought prompting

## Learnings