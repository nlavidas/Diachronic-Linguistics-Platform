

import React from "react";
import axios from "axios";



function App() {
    const [view, setView] = React.useState("home");
    const [results, setResults] = React.useState([]);
    const [pattern, setPattern] = React.useState("");
    const [uploadFile, setUploadFile] = React.useState(null);
    const [uploadStatus, setUploadStatus] = React.useState("");
    const [stats, setStats] = React.useState([]);
    const [auth, setAuth] = React.useState({ user: process.env.REACT_APP_BASIC_AUTH_USER || "admin", pass: process.env.REACT_APP_BASIC_AUTH_PASS || "changeme" });
    const [showAuth, setShowAuth] = React.useState(false);
    const [contrastive, setContrastive] = React.useState({ lang1: "grc", lang2: "lat", pattern: "" });
    const [contrastiveResults, setContrastiveResults] = React.useState(null);
    const basicAuth = "Basic " + btoa(auth.user + ":" + auth.pass);
    const runContrastive = async () => {
        try {
            const params = { lang1: contrastive.lang1, lang2: contrastive.lang2 };
            if (contrastive.pattern) params.pattern = contrastive.pattern;
            const res = await axios.get("/api/contrastive", {
                params,
                headers: { Authorization: basicAuth }
            });
            setContrastiveResults(res.data);
        } catch (e) {
            setContrastiveResults({ error: "Auth failed or backend error" });
            setShowAuth(true);
        }
    };

    // Demo: password prompt if not default
    React.useEffect(() => {
        if (auth.user === "admin" && auth.pass === "changeme") setShowAuth(true);
    }, []);

    const handleAuth = (e) => {
        e.preventDefault();
        setShowAuth(false);
    };

    const search = async () => {
        try {
            const res = await axios.get("/api/valency/search", {
                params: { pattern },
                headers: { Authorization: basicAuth }
            });
            setResults(res.data);
        } catch (e) {
            alert("Auth failed or backend error");
            setShowAuth(true);
        }
    };

    const uploadText = async () => {
        if (!uploadFile) return;
        const formData = new FormData();
        formData.append("file", uploadFile);
        try {
            await axios.post("/api/upload", formData, { headers: { Authorization: basicAuth, "Content-Type": "multipart/form-data" } });
            setUploadStatus("Upload successful!");
        } catch (e) {
            setUploadStatus("Upload failed");
            setShowAuth(true);
        }
    };

    const fetchStats = async () => {
        try {
            const res = await axios.get("/api/valency/changes", { headers: { Authorization: basicAuth } });
            setStats(res.data);
        } catch (e) {
            setShowAuth(true);
        }
    };

    // Demo: 24/7 scrape/proc buttons (simulate)
    const scrapeOpenAccess = () => {
        alert("24/7 open-access scraping started (demo)");
    };
    const proielPreproc = () => {
        alert("PROIEL-style preprocessing started (demo)");
    };
    const aiPreproc = () => {
        alert("AI-enhanced preprocessing started (demo)");
    };

    return (
        <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
            <h1>Diachronic Valency Corpus</h1>
            {/* Navigation Menu */}
            <nav style={{ marginBottom: 20 }}>
                <button onClick={() => setView("home")}>Home</button>
                <button onClick={() => setView("search")}>Search</button>
                <button onClick={() => setView("upload")}>Upload</button>
                <button onClick={() => { setView("stats"); fetchStats(); }}>Statistics</button>
                <button onClick={() => setView("scrape")}>24/7 Scraping/Processing</button>
                <button onClick={() => setView("contrastive")}>Contrastive Analysis</button>
            </nav>
            {view === "contrastive" && (
                <div>
                    <h3>Contrastive Valency Analysis</h3>
                    <form onSubmit={e => { e.preventDefault(); runContrastive(); }}>
                        <label>Language 1: <input value={contrastive.lang1} onChange={e => setContrastive(c => ({ ...c, lang1: e.target.value }))} placeholder="e.g. grc" /></label>
                        <label>Language 2: <input value={contrastive.lang2} onChange={e => setContrastive(c => ({ ...c, lang2: e.target.value }))} placeholder="e.g. lat" /></label>
                        <label>Pattern: <input value={contrastive.pattern} onChange={e => setContrastive(c => ({ ...c, pattern: e.target.value }))} placeholder="e.g. NOM-ACC (optional)" /></label>
                        <button type="submit">Compare</button>
                    </form>
                    {contrastiveResults && (
                        <div style={{ marginTop: 20 }}>
                            {contrastiveResults.error ? (
                                <div style={{ color: 'red' }}>{contrastiveResults.error}</div>
                            ) : (
                                <div style={{ display: 'flex', gap: 40 }}>
                                    <div>
                                        <h4>{contrastive.lang1} Results</h4>
                                        <ul>
                                            {contrastiveResults.lang1 && contrastiveResults.lang1.length === 0 && <li>No data</li>}
                                            {contrastiveResults.lang1 && contrastiveResults.lang1.map((r, i) => (
                                                <li key={i}>{r.verb} - {r.pattern} ({r.year})</li>
                                            ))}
                                        </ul>
                                    </div>
                                    <div>
                                        <h4>{contrastive.lang2} Results</h4>
                                        <ul>
                                            {contrastiveResults.lang2 && contrastiveResults.lang2.length === 0 && <li>No data</li>}
                                            {contrastiveResults.lang2 && contrastiveResults.lang2.map((r, i) => (
                                                <li key={i}>{r.verb} - {r.pattern} ({r.year})</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Password Prompt */}
            {showAuth && (
                <form onSubmit={handleAuth} style={{ marginBottom: 20, background: '#eee', padding: 10 }}>
                    <b>Login required:</b><br />
                    <input placeholder="Username" value={auth.user} onChange={e => setAuth(a => ({ ...a, user: e.target.value }))} />
                    <input placeholder="Password" type="password" value={auth.pass} onChange={e => setAuth(a => ({ ...a, pass: e.target.value }))} />
                    <button type="submit">Login</button>
                </form>
            )}

            {/* Views */}
            {view === "home" && (
                <div>
                    <p>Welcome! This platform collects, processes, and analyzes diachronic valency data 24/7.<br />
                        Use the menu to search, upload, view statistics, or trigger scraping/processing tasks.</p>
                </div>
            )}
            {view === "search" && (
                <div>
                    <input value={pattern} onChange={e => setPattern(e.target.value)} placeholder="Valency pattern (e.g. NOM-ACC)" />
                    <button onClick={search}>Search</button>
                    <ul>
                        {results.map((r, i) => (
                            <li key={i}>{r.verb} - {r.pattern} ({r.year})</li>
                        ))}
                    </ul>
                </div>
            )}
            {view === "upload" && (
                <div>
                    <input type="file" onChange={e => setUploadFile(e.target.files[0])} />
                    <button onClick={uploadText}>Upload Text</button>
                    <div>{uploadStatus}</div>
                </div>
            )}
            {view === "stats" && (
                <div>
                    <h3>Valency Patterns by Year</h3>
                    <ul>
                        {stats.map((s, i) => (
                            <li key={i}>Year: {s.year} — Patterns: {s.count}</li>
                        ))}
                    </ul>
                </div>
            )}
            {view === "scrape" && (
                <div>
                    <button onClick={scrapeOpenAccess}>Start 24/7 Open-Access Scraping</button>
                    <button onClick={proielPreproc}>Start PROIEL-style Preprocessing</button>
                    <button onClick={aiPreproc}>Start AI-Enhanced Preprocessing</button>
                    <p>(These are demo buttons. The real 24/7 agents run in the background and can be monitored in Grafana.)</p>
                </div>
            )}
        </div>
    );
}

export default App;
