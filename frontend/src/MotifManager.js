import React, { useState, useEffect } from "react";

function MotifManager() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [message, setMessage] = useState("");
  const [motifs, setMotifs] = useState([]);

  useEffect(() => { fetchMotifs(); }, []);

  const fetchMotifs = async () => {
    try {
      const res = await fetch("http://localhost:8000/motifs");
      if (!res.ok) throw new Error("Failed to fetch motifs");
      const data = await res.json();
      setMotifs(data);
    } catch (err) {
      setMessage(`❌ Error: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const motif = {
      name,
      description,
      metadata: { category, source: "UI form" },
    };

    try {
      const res = await fetch("http://localhost:8000/motifs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(motif),
      });
      if (!res.ok) throw new Error("Failed to add motif");
      setName(""); setDescription(""); setCategory("");
      setMessage("✅ Motif added!");
      fetchMotifs();
    } catch (err) {
      setMessage(`❌ Error: ${err.message}`);
    }
  };

  return (
    <div className="motif-manager">
      <h2>Add a New Motif</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
        <br/>
        <textarea placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} required />
        <br/>
        <input placeholder="Category" value={category} onChange={e => setCategory(e.target.value)} />
        <br/>
        <button type="submit">Submit</button>
      </form>

      {message && <p>{message}</p>}

      <h2>Existing Motifs</h2>
      {motifs.length === 0 ? <p>No motifs yet</p> : (
        <table border="1" cellPadding="6" style={{ width: "100%", marginTop: "1rem" }}>
          <thead>
            <tr><th>Name</th><th>Description</th><th>Category</th><th>Source</th></tr>
          </thead>
          <tbody>
            {motifs.map((m, idx) => (
              <tr key={idx}>
                <td>{m.name}</td>
                <td>{m.description}</td>
                <td>{m.metadata?.category || "-"}</td>
                <td>{m.metadata?.source || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default MotifManager;
