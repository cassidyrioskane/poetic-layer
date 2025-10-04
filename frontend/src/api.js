const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

// --- Motifs ---
export async function getMotifs() {
  const res = await fetch(`${API_BASE}/motifs`);
  return res.json();
}

export async function createMotif(motif) {
  const res = await fetch(`${API_BASE}/motifs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(motif),
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`Failed to create motif: ${msg}`);
  }
  return res.json();
}


// --- Mappings ---
export async function getMappings() {
  const res = await fetch("/api/mappings");
  if (!res.ok) throw new Error("Failed to fetch mappings");
  return res.json();
}

export async function createMapping(mapping) {
  const res = await fetch("/api/mappings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(mapping),
  });
  if (!res.ok) throw new Error("Failed to create mapping");
  return res.json();
}
