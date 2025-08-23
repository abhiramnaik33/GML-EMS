# GM League - Sports Bidding & Management System

## 📌 Project Overview
The **GM League Management System** is a web-based platform developed for managing sports leagues at **GM University**.  

It provides:  
- ✅ Team Owner registration and login  
- ✅ Player registration with details (name, branch, year, skill level, etc.)  
- ✅ Player bidding system (team owners can bid for players)  
- ✅ Dynamic budget management for teams (remaining balance shown after each bid)  
- ✅ Admin monitoring of bidding & player allocations  

This system is designed to organize tournaments like:  
⚽ Football | 🏏 Cricket | 🏀 Basketball | 🏐 Volleyball | 🤼 Kabaddi | 🤾 Throwball | 🏸 Shuttle Badminton | 🏃 Kho-Kho  

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS (Tailwind), JavaScript  
- **Backend:** Python (Flask)  
- **Database:** SQLite / MySQL  
- **Tools:** SQLAlchemy ORM, Jinja2 Templates  

---

## 🚀 Features
1. **Player Management** – Players can register with details like name, age, branch, year of study, and skill level.  
2. **Bidding System** – Team owners can bid for players in real-time.  
3. **Budget Tracking** – Each team has a fixed budget. The system automatically deducts bid prices and shows the **remaining balance**.  
4. **Admin Dashboard** – Admin can monitor registrations, bids, and manage teams/players.  
5. **Tournament Ready** – Supports multiple sports seasons with different games.  

---

## 📂 Project Structure
/GM-League
│── app.py # Main Flask application
│── /templates # HTML templates
│── /static # CSS, JS, Images
│── /database # Database files
│── /uploads # Player photos
│── README.md # Documentation


---

## 👨‍💻 Contributors
- **Abhiram Girish Naik** – Project Lead & Developer  

---

## ⚡ How to Run
1. Clone this repository  
   ```bash
   git clone https://github.com/your-username/gm-league.git
   cd gm-league
2.pip install -r requirements.txt
3.python app.py
4.Open in browser: http://127.0.0.1:xxxx/
