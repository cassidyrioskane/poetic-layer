import React, { useState, useEffect } from "react";
import { getMotifs, createMotif } from "../api";
import { v4 as uuidv4 } from "uuid"; // you'll need to install this: npm install uuid

export default function MotifManager() {
  const [motifs, setMotifs] = useState([]);
  const [name, setName] = useState("");
  const [text, setText] = useState("");
  const [tags, setTags] = useState("");

  useEffect(() => {
    loadMotifs();
  }, []);

  async function loadMotifs() {
    const data = await getMotifs();
    setMotifs(data);
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const motifData = {
      id: uuidv4(), // auto-generate unique ID
      name,
      text,
      tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
      ethics: {}, // empty since we're not using it now
      version: "1.0.0", // fixed default
      provenance: {
        source: "user",
        method: "manual-entry",
      },
    };

    await createMotif(motifData);
    await loadMotifs();

    // clear form
    setName("");
    setText("");
    setTags("");
  }

  return (
    <div>
      <h2>Motif Manager</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Name</label><br />
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>

        <div>
          <label>Text</label><br />
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows="4"
            required
          />
        </div>

        <div>
          <label>Tags (comma-separated)</label><br />
          <input value={tags} onChange={(e) => setTags(e.target.value)} />
        </div>

        <button type="submit">Create Motif</button>
      </form>

      <h3>Existing Motifs</h3>
      <ul>
        {motifs.map((m) => (
          <li key={m.id}>
            <strong>{m.name}</strong> — {m.text.slice(0, 50)}...
          </li>
        ))}
      </ul>
    </div>
  );
}
