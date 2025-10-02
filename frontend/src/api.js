const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function getMotifs() {
  try {
    const res = await fetch(`${BASE_URL}/motifs`);
    if (!res.ok) throw new Error(`Failed to fetch motifs: ${res.statusText}`);
    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}

export async function createMotif(motif) {
  try {
    const res = await fetch(`${BASE_URL}/motifs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(motif),
    });
    if (!res.ok) {
      const text = await res.text(); // backend might send error text
      throw new Error(`Failed to create motif: ${res.status} ${text}`);
    }
    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}