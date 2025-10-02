import React, { useEffect, useState } from "react";
import { getMotifs, createMotif } from "../api";

export default function MotifManager() {
  const [motifs, setMotifs] = useState([]);
  const [form, setForm] = useState({
    id: "",
    name: "",
    text: "",
    tags: "",
    ethics: "",
    version: "1.0.0",
    provenance: {"author": "system", "source": "seed"},
  });
  const [error, setError] = useState("");

  // Load motifs on mount
  useEffect(() => {
    getMotifs()
      .then(setMotifs)
      .catch((err) => setError(err.message));
  }, []);

  // Handle form changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Basic validation for required fields
    if (!form.id || !form.name || !form.text || !form.version || !form.provenance) {
      setError("Please fill out all required fields.");
      return;
    }

    try {
      // Parse provenance and ethics JSON if provided
      const provenanceObj = JSON.parse(form.provenance || "{}");
      const ethicsObj = form.ethics ? JSON.parse(form.ethics) : {};

      const motif = {
        id: form.id,
        name: form.name,
        text: form.text,
        tags: form.tags ? form.tags.split(",").map((t) => t.trim()) : [],
        ethics: ethicsObj,
        version: form.version,
        provenance: provenanceObj,
      };

      const saved = await createMotif(motif);
      setMotifs([...motifs, saved]);

      // Reset form
      setForm({
        id: "",
        name: "",
        text: "",
        tags: "",
        ethics: "",
        version: "",
        provenance: "",
      });
    } catch (err) {
      setError("Failed to save motif: " + err.message);
    }
  };

  return (
    <div>
      <h2>Motif Manager</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          name="id"
          placeholder="ID (required)"
          value={form.id}
          onChange={handleChange}
        />
        <input
          name="name"
          placeholder="Name (required)"
          value={form.name}
          onChange={handleChange}
        />
        <textarea
          name="text"
          placeholder="Text (required)"
          value={form.text}
          onChange={handleChange}
        />
        <input
          name="tags"
          placeholder="Tags (comma-separated)"
          value={form.tags}
          onChange={handleChange}
        />
        <textarea
          name="ethics"
          placeholder='Ethics JSON (optional, e.g. {"safety":["rule1"]})'
          value={form.ethics}
          onChange={handleChange}
        />
        <input
          name="version"
          placeholder="Version (required)"
          value={form.version}
          onChange={handleChange}
        />
        <textarea
          name="provenance"
          placeholder='Provenance JSON (required, e.g. {"source":"manual"})'
          value={form.provenance}
          onChange={handleChange}
        />
        <button type="submit">Add Motif</button>
      </form>

      <h3>Existing Motifs</h3>
      <ul>
        {motifs.map((m) => (
          <li key={m.id}>
            <strong>{m.name}</strong>: {m.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
