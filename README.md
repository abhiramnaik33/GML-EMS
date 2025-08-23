
# GM League - Sports Bidding & Management System

## 📌 Project Overview
The **GM League Management System** is a web-based platform developed for managing sports leagues at **GM University**.  

This platform is designed to streamline sports event management, registration, and bidding processes.  

### ✅ Features
- **Team Owner Registration & Login** – Secure authentication for team owners.  
- **Player Registration** – Players can register with details like **Name, Branch, Year, Skill Level, and Sport**.  
- **Player Bidding System** – Team owners can bid for registered players during auctions.  
- **Dynamic Budget Management** – Each team has a predefined budget; the remaining amount is updated after every bid.  
- **Admin Panel** – Admins can monitor bidding, player allocations, and reset or update details if required.  
- **Multi-Sport Support** – Can be used for tournaments like:  
  - 🏏 Cricket  
  - ⚽ Football  
  - 🏀 Basketball  
  - 🏐 Volleyball  
  - 🤾 Kabaddi  
  - 🤸 Throwball  
  - 🏸 Shuttle Badminton  
  - 🏃 Kho-Kho  

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript, Tailwind  
- **Backend**: Python (Flask)  
- **Database**: SQLite (can be upgraded to MySQL/PostgreSQL)  
- **Other Tools**: Jinja2 templating, SQLAlchemy ORM  

---

## 🚀 How It Works
1. **Player Registration**  
   - Players register by filling out a form with their details.  
   - Data is stored in the database.  

2. **Team Owner Registration & Login**  
   - Team owners sign up and receive an initial **budget**.  
   - Owners log in to access the bidding system.  

3. **Bidding System**  
   - A list of available players is displayed.  
   - Team owners place bids within their budget.  
   - The system dynamically updates **remaining budget** after each purchase.  

4. **Admin Panel**  
   - Admin can view all registered teams, players, and bidding history.  
   - Admins have the ability to reset auctions or override allocations if needed.  

---

## 📂 Project Structure
```

GM-League/
│── app.py                # Main Flask application
│── templates/            # HTML Templates (Frontend)
│   ├── index.html
│   ├── register\_player.html
│   ├── register\_owner.html
│   ├── bidding.html
│   ├── dashboard.html
│── static/               # CSS, JS, Images
│── database.db           # SQLite Database (auto-created)
│── README.md             # Project Documentation

````



## ⚡ Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/GM-League.git
   cd GM-League


2. Create a virtual environment & activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open in browser:

   ```
   http://127.0.0.1:5000
   ```

---

## 📊 Future Enhancements

* Live auction updates using WebSockets.
* Export bidding data to Excel/PDF.
* Notifications for team owners.
* Multi-admin role support.
* Cloud deployment with PostgreSQL.

---





* **Abhiram Girish Naik** – Project Lead & Developer

---

```
