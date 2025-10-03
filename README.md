# 🎯 CareerMatch ✨

**CareerMatch** is a full-stack personality quiz app that helps users discover career paths based on their personal traits, work preferences, and motivations.

🌐 **Live Frontend** (Vercel): [https://career-match-rho.vercel.app/](https://career-match-rho.vercel.app/)  
🔗 **Live Backend** (Render): [Deployed Python API Endpoint] – (https://career-match-0pw6.onrender.com)

---

## 🌟 Features

- ✨ Clean, responsive UI with TailwindCSS
- 🧠 Quiz spans 6 categories: personality, weekend style, problem-solving, work environment, collaboration, and motivation
- 🧩 Interactive quiz cards with selection feedback
- 🔁 Form data submitted to backend API via POST request
- 💬 Easily extendable to provide career suggestions based on responses

---

## 📁 Project Structure

```
.
├── backend/
│   └── main.py                # Flask API endpoint for processing quiz submissions
├── frontend/
│   └── start.html             # HTML page styled with TailwindCSS
├── README.md
```

---

## 🛠 Tech Stack

| Layer     | Tech                  |
|-----------|------------------------|
| Frontend  | HTML, JS, TailwindCSS |
| Backend   | Python (Flask)        |
| Hosting   | Vercel (Frontend) + Render (Backend) |

---

## 🚀 Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd frontend
open start.html  # or use a local server
```

---

## ☁️ Deployment

- **Frontend** hosted on [Vercel](https://vercel.com)
  - Deployed from `/frontend/start.html`
- **Backend** deployed to [Render](https://render.com)
  - Flask app hosted with public API endpoint

---

## 👩‍💻 Author

**Jane Park**  
