// frontend/src/api.js
const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

// -------- Motifs --------
export async function getMotifs() {
  const res = await fetch(`${API_BASE}/motifs`);
  if (!res.ok) throw new Error(`Failed to fetch motifs: ${res.status}`);
  return res.json();
}

export async function createMotif(motif) {
  const res = await fetch(`${API_BASE}/motifs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(motif),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to create motif: ${res.status} ${text}`);
  }
  return res.json();
}

export async function deleteMotif(id) {
  const res = await fetch(`${API_BASE}/motifs/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete motif: ${res.status}`);
  return res.json();
}

// -------- Mappings --------
export async function getMappings() {
  const res = await fetch(`${API_BASE}/mappings`);
  if (!res.ok) throw new Error(`Failed to fetch mappings: ${res.status}`);
  return res.json();
}

export async function createMapping(mapping) {
  const res = await fetch(`${API_BASE}/mappings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(mapping),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to create mapping: ${res.status} ${text}`);
  }
  return res.json();
}

export async function runMapping(runSpec) {
  const res = await fetch(`${API_BASE}/mappings/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(runSpec),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to run mapping: ${res.status} ${text}`);
  }
  return res.json();
}

export async function getRegistryMappings() {
  const res = await fetch(`${API_BASE}/registry/mappings`);
  if (!res.ok) throw new Error(`Failed to fetch registry mappings: ${res.status}`);
  return res.json();
}

