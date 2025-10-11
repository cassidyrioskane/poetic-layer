import React, { useEffect, useState } from "react";
import { getMotifs, createMotif, deleteMotif } from "../api";

export default function MotifManager({ onRefresh }) {
  const [motifs, setMotifs] = useState([]);
  const [name, setName] = useState("");
  const [text, setText] = useState("");
  const [type, setType] = useState("text"); // text | image
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState("");
  const [expanded, setExpanded] = useState({});

  // --- Load motifs from backend ---
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

  // --- File selection handler ---
  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result);
    reader.readAsDataURL(f);
  };

  const resetForm = () => {
    setName("");
    setText("");
    setType("text");
    setFile(null);
    setPreview(null);
  };

  // --- Create new motif (text or image) ---
  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      let motifData = { name: name || "Untitled", tags: [] };

      if (type === "image" && file) {
        const reader = new FileReader();
        reader.onload = async () => {
          const base64 = reader.result.split(",")[1];
          motifData.type = "image";
          motifData.content = base64;
          await createMotif(motifData);
          resetForm();
          await load();
          setMessage("✅ Image motif uploaded");
        };
        reader.readAsDataURL(file);
        return;
      } else {
        motifData.type = "text";
        motifData.content = text || "";
        await createMotif(motifData);
        resetForm();
        await load();
        setMessage("✅ Text motif created");
      }
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

  const toggleExpand = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  // --- Split motifs by type ---
  const textMotifs = motifs.filter((m) => m.type !== "image");
  const imageMotifs = motifs.filter((m) => m.type === "image");

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

        {/* Type toggle */}
        <div style={{ marginBottom: 8 }}>
          <label>
            <input
              type="radio"
              name="motif-type"
              value="text"
              checked={type === "text"}
              onChange={() => setType("text")}
            />
            Text
          </label>
          <label style={{ marginLeft: 16 }}>
            <input
              type="radio"
              name="motif-type"
              value="image"
              checked={type === "image"}
              onChange={() => setType("image")}
            />
            Image
          </label>
        </div>

        {type === "text" && (
          <textarea
            placeholder="Text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={4}
            style={{ width: "100%", marginBottom: 8 }}
          />
        )}

        {type === "image" && (
          <div style={{ marginBottom: 8 }}>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            {preview && (
              <div style={{ marginTop: 8 }}>
                <img
                  src={preview}
                  alt="Preview"
                  style={{
                    maxWidth: "100%",
                    maxHeight: 200,
                    border: "1px solid #ccc",
                    borderRadius: 6,
                  }}
                />
              </div>
            )}
          </div>
        )}

        <button type="submit">Add Motif</button>
      </form>

      {message && <p>{message}</p>}

      {/* ---------- TEXT MOTIFS ---------- */}
      {textMotifs.length > 0 && (
        <>
          <h3>Text Motifs</h3>
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
              {textMotifs.map((m) => {
                const body = m.content ?? m.text ?? "";
                return (
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
                      {body}
                    </td>
                    <td style={{ verticalAlign: "top" }}>
                      <button onClick={() => handleDelete(m.id)}>Delete</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      )}

      {/* ---------- IMAGE MOTIFS ---------- */}
      {imageMotifs.length > 0 && (
        <>
          <h3 style={{ marginTop: 20 }}>Image Motifs</h3>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
              gap: 12,
              marginTop: 8,
            }}
          >
            {imageMotifs.map((m) => (
              <div
                key={m.id}
                style={{
                  position: "relative",
                  border: "1px solid #ddd",
                  borderRadius: 6,
                  overflow: "hidden",
                  background: "#f9f9f9",
                  textAlign: "center",
                  paddingBottom: 6,
                }}
              >
                <img
                  src={`data:image/png;base64,${m.content}`}
                  alt={m.name}
                  style={{
                    width: "100%",
                    height: 120,
                    objectFit: "cover",
                    display: "block",
                  }}
                />
                <div style={{ fontSize: 12, marginTop: 4 }}>{m.name}</div>
                <button
                  onClick={() => handleDelete(m.id)}
                  style={{
                    position: "absolute",
                    top: 4,
                    right: 4,
                    background: "rgba(255,255,255,0.8)",
                    border: "1px solid #ccc",
                    borderRadius: 4,
                    fontSize: 10,
                    padding: "2px 4px",
                    cursor: "pointer",
                  }}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
