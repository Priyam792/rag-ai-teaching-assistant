# RAG AI Teaching Assistant

A Retrieval-Augmented Generation (RAG) based AI Teaching Assistant for
the Sigma Web Development course.

The project processes course videos into timestamped transcript chunks,
creates vector embeddings, retrieves the most relevant course content
for a user's question, and uses Llama 3.2 to generate a human-friendly
answer with the relevant video and timestamp.

## Project Pipeline

``` text
Course Videos
     ↓
Video → MP3
     ↓
MP3 → Timestamped JSON
     ↓
JSON → Embeddings
     ↓
Chunk Processing / Merging
     ↓
User Query → Query Embedding
     ↓
Cosine Similarity / Top-K Retrieval
     ↓
Relevant Course Chunks
     ↓
Llama 3.2
     ↓
Answer + Video + Timestamp
```

## Features

-   Converts course videos to MP3 using FFmpeg
-   Transcribes audio using Whisper
-   Preserves transcript timestamps
-   Stores video title and video number as metadata
-   Creates embeddings using BGE-M3
-   Performs semantic retrieval using cosine similarity
-   Retrieves the top relevant course chunks
-   Uses Llama 3.2 to generate answers from retrieved course material
-   Identifies the relevant video and timestamp for a topic
-   Guides the learner to the appropriate part of the course
-   Runs locally using Ollama

## Tech Stack

-   Python
-   FFmpeg
-   OpenAI Whisper
-   Pandas
-   NumPy
-   Scikit-learn
-   Joblib
-   BGE-M3
-   Ollama
-   Llama 3.2
-   RAG (Retrieval-Augmented Generation)

## Project Structure

``` text
RAG-based-AI-Teaching-Assistant/
│
├── videos/
├── audios/
├── jsons/
├── newjsons/
│
├── video_to_mp3.py
├── mp3_to_json.py
├── preprocess_json.py
├── process_incoming.py
│
├── embeddings.joblib
├── prompt.txt
├── response.txt
│
└── README.md
```

> Generated data such as videos, audio files, JSON files, and embeddings
> can be kept outside the Git repository to keep the repository
> lightweight.

## How It Works

### Step 1 --- Collect Your Videos

Move all your course video files into the `videos` folder.

### Step 2 --- Convert Videos to MP3

Convert all the video files to MP3 by running:

``` bash
python video_to_mp3.py
```

The script uses FFmpeg to extract the audio from the course videos.

### Step 3 --- Convert MP3 to JSON

Convert all the MP3 files to timestamped JSON transcripts:

``` bash
python mp3_to_json.py
```

Whisper processes the audio and stores information such as:

-   Video number
-   Video title
-   Start timestamp
-   End timestamp
-   Transcript text

Example:

``` json
{
    "number": "21",
    "title": "Creating Embeddings",
    "start": 123.4,
    "end": 156.7,
    "text": "..."
}
```

### Step 4 --- Convert JSON Files to Vectors

Use `preprocess_json.py` to convert the transcript chunks into
embeddings:

``` bash
python preprocess_json.py
```

The script:

1.  Reads the JSON transcript files.
2.  Creates embeddings using the BGE-M3 model.
3.  Assigns a unique `chunk_id` to each chunk.
4.  Stores the embedding with its corresponding metadata.
5.  Creates a Pandas DataFrame.
6.  Saves the DataFrame as `embeddings.joblib`.

### Step 5 --- Prompt Generation and Feeding to the LLM

Run:

``` bash
python process_incoming.py
```

The script:

1.  Loads the saved embeddings.
2.  Takes the user's question.
3.  Creates an embedding for the question.
4.  Calculates cosine similarity between the question and course chunks.
5.  Retrieves the top relevant chunks.
6.  Builds a context-aware prompt.
7.  Sends the prompt to Llama 3.2 through Ollama.
8.  Prints the final response.

The response is designed to tell the learner where the requested topic
is covered, including the relevant video and timestamp.

## Example

A user can ask:

``` text
Where is JavaScript functions explained?
```

The system retrieves the most relevant course chunks and generates an
answer such as:

``` text
The topic is covered in Video 24, "JavaScript Functions",
around 12:35.

Go to around 12:35 in that video to find the explanation.
```

The exact response depends on the retrieved course content.

## Local LLM Setup

This project uses Ollama for local embedding and LLM inference.

The project uses:

``` text
Embedding Model: BGE-M3
LLM: Llama 3.2
```

Make sure the required Ollama models are available locally before
running the embedding and inference stages.

## RAG Architecture

``` text
User Question
      ↓
Question Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
      ↓
Context + User Question
      ↓
Llama 3.2
      ↓
Final Human-Friendly Answer
```

The LLM is provided with the retrieved course content rather than being
asked to search the entire course by itself.

## Why This Project?

Finding a particular concept in a long course can require manually
searching through many videos.

This project uses RAG to make the course searchable through
natural-language questions. Instead of only answering a question, the
assistant can point the learner toward the relevant video and timestamp
where the topic is taught.

## Future Improvements

-   Improve chunking and context merging
-   Improve retrieval quality
-   Add better source citation
-   Add a web interface
-   Add clickable video timestamps
-   Add course progress tracking
-   Evaluate retrieval accuracy
-   Improve prompt and response formatting

## How to Use This RAG AI Teaching Assistant on Your Own Data

### Step 1 - Collect your videos

Move all your video files to the `videos` folder.

### Step 2 - Convert to MP3

Convert all the video files to MP3 by running `video_to_mp3.py`.

### Step 3 - Convert MP3 to JSON

Convert all the MP3 files to JSON by running `mp3_to_json.py`.

### Step 4 - Convert the JSON Files to Vectors

Use the file `preprocess_json.py` to convert the JSON files to a
DataFrame with embeddings and save it as a Joblib pickle.

### Step 5 - Prompt Generation and Feeding to LLM

Read the Joblib file and load it into memory. Then create a relevant
prompt according to the user query and feed it to the LLM.

## Disclaimer

This project is built as a learning and portfolio project to explore
Retrieval-Augmented Generation, embeddings, local LLMs, speech-to-text
processing, and semantic search.
