// frontend/src/components/MotifManager.js
import React, { useEffect, useState } from "react";
import { getMotifs, createMotif, deleteMotif } from "../api";

export default function MotifManager({ onRefresh }) {
  const [motifs, setMotifs] = useState([]);
  const [name, setName] = useState("");
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");

  const load = async () => {
    try {
      const data = await getMotifs();
      setMotifs(data);
      onRefresh?.(data);
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  useEffect(() => {
    load();
  }, []); // ✅ no refreshSignal here

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const created = await createMotif({
        name: name || "Untitled",
        text: text || "",
        tags: [],
      });
      setName("");
      setText("");
      await load();
      setMessage("✅ Motif created");
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteMotif(id);
      await load();
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  return (
    <div style={{ padding: 12 }}>
      <h2>Motifs</h2>

      <form onSubmit={handleCreate} style={{ marginBottom: 12 }}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: "100%", marginBottom: 8 }}
        />
        <textarea
          placeholder="Text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={4}
          style={{ width: "100%", marginBottom: 8 }}
        />
        <button type="submit">Add Motif</button>
      </form>

      {message && <p>{message}</p>}

      {motifs.length === 0 ? (
        <p>No motifs yet</p>
      ) : (
        <table border="1" cellPadding="6" style={{ width: "100%", marginTop: 8 }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Preview</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {motifs.map((m) => (
              <tr key={m.id}>
                <td>{m.name}</td>
                <td
                  style={{
                    maxWidth: 600,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {m.text}
                </td>
                <td>
                  <button onClick={() => handleDelete(m.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
