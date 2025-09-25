import { useEffect, useState } from "react";

function App() {
  const [motifs, setMotifs] = useState([]);
  const [mappings, setMappings] = useState([]);

  useEffect(() => {
    // Fetch example motif
    fetch("http://localhost:8000/motifs/twinned_lullaby")
      .then((res) => res.json())
      .then(setMotifs);

    // Fetch example mapping
    fetch("http://localhost:8000/mappings/coupled_oscillators")
      .then((res) => res.json())
      .then(setMappings);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Poetic-Layer Dashboard</h1>

      <section>
        <h2>Motifs</h2>
        <pre>{JSON.stringify(motifs, null, 2)}</pre>
      </section>

      <section>
        <h2>Mappings</h2>
        <pre>{JSON.stringify(mappings, null, 2)}</pre>
      </section>
    </div>
  );
}

export default App;
