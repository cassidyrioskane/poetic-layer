import React, { useEffect, useState } from "react";
import { getMotifs, createMotif, deleteMotif } from "../api";

export default function MotifManager({ onRefresh }) {
  const [motifs, setMotifs] = useState([]);
  const [name, setName] = useState("");
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");
  const [expanded, setExpanded] = useState({}); // track which motifs are expanded

  // --- Load motifs ---
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
  }, []);

  // --- Create a new motif ---
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

  // --- Delete motif ---
  const handleDelete = async (id) => {
    try {
      await deleteMotif(id);
      await load();
    } catch (e) {
      setMessage(`❌ ${e.message}`);
    }
  };

  // --- Toggle expand/collapse ---
  const toggleExpand = (id) => {
    setExpanded((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
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
        <table
          border="1"
          cellPadding="6"
          style={{
            width: "100%",
            marginTop: 8,
            borderCollapse: "collapse",
            tableLayout: "fixed",
          }}
        >
          <thead>
            <tr>
              <th style={{ width: "15%" }}>Name</th>
              <th style={{ width: "70%" }}>Text</th>
              <th style={{ width: "15%" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {motifs.map((m) => (
              <tr key={m.id}>
                <td style={{ verticalAlign: "top" }}>{m.name}</td>
                <td
                  style={{
                    textAlign: "left",
                    verticalAlign: "top",
                    cursor: "pointer",
                    maxHeight: expanded[m.id] ? "none" : "3.5em",
                    overflow: expanded[m.id] ? "visible" : "hidden",
                    whiteSpace: expanded[m.id] ? "pre-wrap" : "nowrap",
                    textOverflow: expanded[m.id] ? "unset" : "ellipsis",
                    borderLeft: "4px solid #ccc",
                    paddingLeft: 6,
                    userSelect: "text",
                  }}
                  title={
                    expanded[m.id]
                      ? "Click to collapse text"
                      : "Click to expand full text"
                  }
                  onClick={() => toggleExpand(m.id)}
                >
                  {m.text}
                </td>
                <td style={{ verticalAlign: "top" }}>
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
