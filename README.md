# Meeting Transcriber Exercise

Homework for the Budapest University of Technology and Economics: Prompt Engineering (VITMAV82) subject

## Homework Listing

**Homework ID:** 1

**Description:** 
Web application that allows a moderator to record the speeches of people present at a live meeting and formats speeches using a large language model to generate a note highlights.

## Authors

- Hegedűs András (BCFU8E)): \[nomad-at-you\] Transcription and web application
- Farkas Martin (GV2RF8): \[BlackLight54\] Transcription enhancement and prompting research

## Description of Solution

Our solution is available on GitHub: https://github.com/BlackLight54/meeting-transcriber-exercise


We created a web application that allows a moderator to record the speeches of people present at a live meeting. The application uses a large language model to transcribe the speeches and generate meeting notes. The notes are formatted to highlight key points discussed during the meeting, such as decisions made and action items assigned. The application leverages advanced prompting techniques to enhance the accuracy and coherence of the generated meeting minutes.




### Architecture

We planned the architecture and data flow for our solution to efficiently manage meeting transcriptions and speaker prioritization.

1. **Audio Recording and Transcription:** 
   - The meeting audio is recorded by the moderator recording the speeches of each participant in the meeting individually.
   - The audio files are converted to text using a text-to-speech model.

2. **Text Processing:**
   - The transcribed text is processed by a language model to correct any errors and format the text into a standardized form suitable for prompting.

3. **Meeting Minutes Generation:**
   - The corrected and formatted text, along with optional meeting data, is fed to a language model with a prompt to generate meeting minutes.
   - The minutes are structured based on a methodology we have successfully used in past projects.

4. **Meeting decisions and action items:**
   - The generated minutes are analyzed to identify decisions made and action items assigned during the meeting.
   - These are extracted and presented in a structured format for easy reference.

### Evaluating speech-to-text solutions that support diarization

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

#### Faster-Whisper

**Repository:** https://github.com/SYSTRAN/faster-whisper

Faster-Whisper is a highly efficient implementation of OpenAI's Whisper model, optimized for speed and performance. This model is specifically designed to handle speech-to-text conversion tasks with an emphasis on real-time processing. We used Faster-Whisper in the final implementation.

- **Model Size:** We used the "medium" model, which balances accuracy and speed, making it suitable for our application where prompt transcription is essential.
- **Device:** The model runs on CUDA-enabled devices using float16 precision to leverage GPU acceleration for faster processing.
- **Beam Size:** We configured the model with a beam size of 7, enhancing the quality of the transcription by considering multiple hypotheses during decoding.


#### OpenAI

**API:** https://openai.com/api/

OpenAI's language models, specifically those in the GPT-4 series, are employed for text enhancement and summarization tasks in our application. These models are known for their powerful natural language understanding and generation capabilities, making them ideal for processing and refining meeting transcripts.

- **Model Used:** We utilized the "gpt-4o" model, which is tailored for conversational contexts and capable of understanding complex inputs to generate detailed and coherent outputs.
- **API Integration:** The OpenAI API allows us to send transcribed text and receive enhanced summaries in real-time, facilitating the creation of structured meeting minutes.

*Warning:* The OpenAI API is a paid service, and users must have an API key to access the model. Add it as an environment variable to run the application.



### Prompting Techniques

- **Prompting Notebook:** `./prompting.ipynb`
- **Techniques Used:**
  - One- and Few-shot prompting
  - System and user prompts
  - Separation of actions (Prompt-chaining, Chain-of-thought prompting)


   

### Key Components

1. **Flask Application:**
   - Handles file uploads and processes audio data.
   - Provides endpoints for transcription and enhancement of meeting notes.

2. **Whisper Model:**
   - Utilized for transcribing audio files into text with speaker identification.

3. **OpenAI Integration:**
   - Used to enhance transcriptions by summarizing topics, decisions, and action items.

4. **File Handling:**
   - Transcriptions are stored in a text file (`notes.txt`), which is updated with each new upload.


### UI


<img src="img.png" alt="ui" width="400"/>

<div style="page-break-after: always;"></div>


### Example Workflow

1. **Recording of Speeches:**
   - The moderator records the speeches of participants in the meeting, adding their names to the list of speakers and ensuring each speaker is captured separately.
3. **Transcription Storage:**
   - The transcriptions are appended to `notes.txt` with the speaker's name.

3. **Enhance Notes:**
   - The transcriptions are formatted and sent to the OpenAI model to generate summaries of topics, decisions, and action items.

4. **Output:**
   - The enhanced notes are returned in an easy-to-read format, highlighting key points discussed during the meeting.


## Learnings

Through this project, we gained practical experience in integrating speech-to-text solutions with diarization capabilities and leveraging language models for text correction, formatting, and summarization. Additionally, we applied advanced prompting techniques to enhance the accuracy and coherence of the generated meeting minutes.

Generating Hungarian language support for the Faster-Whisper model required additional prompting to ensure accurate transcription results.

We learned how to utilize local models and cloud-based APIs to enhance the transcription process and generate advanced meeting enhancement. 

## Future Enhancements Opportunities

- Subscribable moderation list for group members to receive notifications when their turn is up
- More enhancement features for the meeting notes, such as sentiment analysis and keyword extraction


