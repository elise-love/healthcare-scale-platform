import React, { useState } from "react";
import api from "../services/api";

export default function RegisterPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            // backend registers + auto-logs in (sets httpOnly cookie)
            await api.post("/auth/register", { email, password });
            window.location.href = "/";
        } catch (err) {
            setError(err?.response?.data?.detail || "Register failed");
        }
    };

    return (
        <div style={{ maxWidth: 420, margin: "40px auto" }}>
            <h2>Register</h2>
            {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
            <form onSubmit={onSubmit}>
                <div style={{ marginBottom: 12 }}>
                    <label>Email</label>
                    <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required style={{ width: "100%" }} />
                </div>
                <div style={{ marginBottom: 12 }}>
                    <label>Password</label>
                    <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required style={{ width: "100%" }} />
                </div>
                <button type="submit">Create account</button>
            </form>
        </div>
    );
}