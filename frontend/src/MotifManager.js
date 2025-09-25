import React, { useEffect, useState } from "react";
import { getMotifs, createMotif } from "./api";

function MotifManager() {
  const [motifs, setMotifs] = useState([]);
  const [newMotif, setNewMotif] = useState("");

  // Load motifs on component mount
  useEffect(() => {
    getMotifs()
      .then(data => setMotifs(data))
      .catch(err => console.error("Failed to fetch motifs:", err));
  }, []);

  // Handle adding a motif
  const handleAddMotif = async () => {
    try {
      const created = await createMotif({ text: newMotif });
      setMotifs([...motifs, created]);
      setNewMotif(""); // clear input
    } catch (err) {
      console.error("Failed to create motif:", err);
    }
  };

  return (
    <div>
      <h2>Motifs</h2>
      <ul>
        {motifs.map((m, i) => (
          <li key={i}>{m.text}</li>
        ))}
      </ul>

      <input
        value={newMotif}
        onChange={(e) => setNewMotif(e.target.value)}
        placeholder="Enter new motif"
      />
      <button onClick={handleAddMotif}>Add Motif</button>
    </div>
  );
}

export default MotifManager;
