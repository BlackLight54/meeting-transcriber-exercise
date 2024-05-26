from flask import Flask, render_template, request, jsonify
from faster_whisper import WhisperModel
from openai import OpenAI
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the model
model_size = "medium"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

hf_token = "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"

client = OpenAI()


def transcribe_chunk(file_path):
    segments, info = model.transcribe(file_path, language="hu", beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    #load existing notes from notes.txt
    exising_notes_file = 'notes.txt'
    existing_notes = ""
    if os.path.exists(exising_notes_file):
        with open(exising_notes_file, 'r', encoding="utf-8") as file:
            existing_notes = file.read()
    if 'audio_data' in request.files and 'name' in request.form:
        audio_data = request.files['audio_data']
        name = request.form['name']
        file_path = os.path.join(UPLOAD_FOLDER, 'recorded_audio.wav')
        audio_data.save(file_path)

        # Transcribe the uploaded audio file
        transcription = transcribe_chunk(file_path)
        transcription_with_name = f"{name}: {transcription}\n"
        existing_notes += transcription_with_name
        # save to notes.txt
        with open(exising_notes_file, 'w', encoding="utf-8") as file:
            file.write(existing_notes)
        return jsonify({"transcribed_text": existing_notes})
    return 'No audio file uploaded or name not provided', 400

@app.route('/enhance_notes', methods=['GET'])
def enhance_notes():
    exising_notes_file = 'notes.txt'
    existing_notes = ""
    if os.path.exists(exising_notes_file):
        with open(exising_notes_file, 'r', encoding="utf-8") as file:
            existing_notes = file.read()

    formatted_conversation = ""
    # make speaker data from a text file with lines: "speaker: text"
    speaker_data = []
    for line in existing_notes.split("\n"):
        if line:
            speaker, text = line.split(":")
            speaker_data.append({"speaker": speaker, "text": text})
    for speaker in speaker_data:
        formatted_conversation += f"{speaker['speaker']}: {speaker['text']}\n"

    # Enhance notes using OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "The following is the transcript of a meeting. Please write a bulleted list of the topics discussed. Ignore greetings. Only write in hungarian."},
            {"role": "user", "content": formatted_conversation + "\nTopics discussed:"}
        ])
    topics_discussed = map(lambda x: x.strip(" -"), completion.choices[0].message.content.split("\n"))
    # add to enhanced notes "Topics discussed: in new lines"
    enhanced_notes = f"Felmerülő témák:\n -" + "\n -".join(topics_discussed)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "The following is the transcript of a meeting. Please write a bulleted list of the decisions made. Ignore greetings. Only write in hungarian."},
            {"role": "user", "content": formatted_conversation + "\nDecisions made:"}
        ])
    decisions_made = map(lambda x: x.strip(" -"), completion.choices[0].message.content.split("\n"))

    # add to enhanced notes "Decisions made: in new lines"
    enhanced_notes += f"\n\nMeghozott döntések:\n -" + "\n -".join(decisions_made)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """The following is the transcript of a meeting. Please write a bulleted list of the action items, responsibilities assigned, or commitments made. Ignore greetings. Only write in hungarian.
            Farkas Martin: I will prepare the presentation for the next meeting.

            The output should be:
            - Farkas Martin: Prepare the presentation for the next meeting.
            """},
            {"role": "user", "content": formatted_conversation + "\nAction items:"}
        ])

    def split_action_item(x):
        responsible_party = x.split(":")[0].strip()
        action = x.split(":")[1].strip()
        action_item = {
            "responsible_party": responsible_party,
            "action": action
        }
        return action_item

    action_items = map(split_action_item,map(lambda x: x.strip(" -"), completion.choices[0].message.content.split("\n")))

    # add to enhanced notes "Action items: in new lines"

    enhanced_notes += f"\n\nBevállalt feladatok:\n" + "\n -".join(map(lambda x: f"- {x['responsible_party']}: {x['action']}", action_items))





    return jsonify({"enhanced_notes": enhanced_notes})

if __name__ == '__main__':
    app.run(debug=True)
