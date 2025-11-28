import axios from "axios";

export const API_BASE = "https://nl2sqlx.onrender.com";

export const api = axios.create({
    baseURL: API_BASE,
});
