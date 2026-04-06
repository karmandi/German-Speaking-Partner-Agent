import { useRef, useState } from "react";

const API_BASE = "http://localhost:8000";

export default function App() {
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const audioPlayerRef = useRef(null);

  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function startRecording() {
    setError("");
    setResult(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Force WAV recording
      const options = { mimeType: "audio/wav" };
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.warn("WAV not supported, falling back to available format");
        const fallback = MediaRecorder.isTypeSupported("audio/webm")
          ? "audio/webm"
          : "audio/mp4";
        options.mimeType = fallback;
      }

      const recorder = new MediaRecorder(stream, options);

      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: options.mimeType });
        await sendAudio(blob, options.mimeType);

        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      setError("Microphone access failed.");
    }
  }

  function stopRecording() {
    if (!mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  }

  async function sendAudio(blob, mimeType) {
    setIsLoading(true);
    setError("");

    try {
      const extension = mimeType.includes("wav") ? "wav" : "webm";
      const formData = new FormData();
      formData.append("audio", blob, `speech.${extension}`);

      const apiUrl = `${API_BASE}/api/speak`;
      console.log("Sending request to:", apiUrl);
      console.log("Blob size:", blob.size, "bytes, type:", mimeType);

      const res = await fetch(apiUrl, {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json",
        }
      });

      console.log("Response status:", res.status, res.statusText);

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Backend error response:", errorText);
        throw new Error(`Backend returned ${res.status}: ${errorText}`);
      }

      const data = await res.json();
      console.log("Success! Response:", data);
      setResult(data);

      if (data.audio_url && audioPlayerRef.current) {
        const audioUrl = `${API_BASE}${data.audio_url}`;
        console.log("Playing audio from:", audioUrl);
        audioPlayerRef.current.src = audioUrl;
        audioPlayerRef.current.play().catch((err) => console.error("Audio playback error:", err));
      }
    } catch (err) {
      console.error("Fetch error details:", {
        message: err.message,
        stack: err.stack,
        name: err.name
      });
      setError(`Failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1>German Speaking Partner</h1>
        <p className="sub">
          Record one sentence in German. The app will transcribe it, reply naturally,
          correct one key mistake, and speak back.
        </p>

        <div className="actions">
          {!isRecording ? (
            <button onClick={startRecording} disabled={isLoading}>
              Start recording
            </button>
          ) : (
            <button onClick={stopRecording} className="stop">
              Stop recording
            </button>
          )}
        </div>

        {isLoading && <p>Processing audio...</p>}
        {error && <p className="error">{error}</p>}

        <audio ref={audioPlayerRef} controls className="audio-player" />

        {result && (
          <div className="result">
            <section>
              <h2>Your transcript</h2>
              <p>{result.user_transcript}</p>
            </section>

            <section>
              <h2>Assistant reply</h2>
              <p>{result.assistant_reply_german}</p>
            </section>

            <section>
              <h2>Correction</h2>
              <p>{result.corrected_sentence}</p>
            </section>

            <section>
              <h2>Explanation</h2>
              <p>{result.explanation_english}</p>
            </section>

            <section>
              <h2>Next question</h2>
              <p>{result.next_question_german}</p>
            </section>

            <section>
              <h2>Level</h2>
              <p>{result.level_used}</p>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}