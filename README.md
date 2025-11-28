# NL2SQLX — Natural Language → SQL Query Generator  
Convert plain English questions into SQL queries and run them on any uploaded CSV dataset.  
Backend powered by FastAPI + MySQL + RAG.  
Frontend built using React/Next.js.

---

## 🚀 Features

### 🔹 **Upload CSV → Auto-Create SQL Table**
- Upload any `.csv` file
- Backend automatically creates a SQL table in MySQL
- Schema is extracted and piped into RAG

### 🔹 **Ask Natural Language Questions**
Examples:
- “Show total revenue by category”
- “List top 10 customers by spending”
- “Give count of employees in each department”

Backend returns:
- ✔ Generated SQL  
- ✔ Executed result  
- ✔ RAG-improved query understanding

### 🔹 **Secure Session Cleanup**
- Clicking **Finish** drops all temporary uploaded tables
- Keeps database clean for next user

---

## 🏗️ Tech Stack

### **Backend**
- Python 3.12
- FastAPI
- SQLAlchemy
- MySQL (AlwaysData / free hosting)
- OpenAI (or Groq) LLMs
- ChromaDB (RAG embeddings)

### **Frontend**
- React / Next.js
- Axios
- Deployed on Vercel / Render

---

# 📌 Project Structure

NL2SQLX/
├── backend/
│ ├── app.py
│ ├── db.py
│ ├── rag.py
│ ├── schema_extractor.py
│ ├── nl2sql.py
│ ├── requirements.txt
├── frontend/
│ ├── app/
│ ├── components/
│ ├── public/
│ ├── package.json
├── README.md


---

# 🧪 Run Backend Locally

### 1️⃣ Create & activate venv
```bash
cd backend
python -m venv venv
venv/Scripts/activate   # Windows
```
## 🛠️ Run Backend Locally

### 2️⃣ Install requirements
```bash
pip install -r requirements.txt
```
###3️⃣ Create .env file inside backend
```
MYSQL_USER=root
MYSQL_PASSWORD=xxxx
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=mydb
OPENAI_API_KEY=your_key
```
###4️⃣ Run FastAPI
uvicorn app:app --reload
```
###🎨 Run Frontend Locally (React/Next.js)
cd frontend
npm install
npm run dev

```
Frontend runs on:

http://localhost:3000
```
```
Backend runs on:

http://localhost:8000
```
```
Edit API_BASE inside frontend:

export const API_BASE = "http://localhost:8000";

```
```
###👨‍💻 About the Developer

Prathamesh Shivaji Salokhe
B.Tech Computer Engineering (Final Year)
```
