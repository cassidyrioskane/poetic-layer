const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function getMotifs() {
  const res = await fetch(`${API_BASE}/motifs`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function createMotif(motif) {
  const res = await fetch(`${API_BASE}/motifs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(motif),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
