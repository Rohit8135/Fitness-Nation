# 🏋️ FITNESS NATION HEALTH CLUB
### Complete Gym Management Website + Backend System

---

## 📁 PROJECT STRUCTURE

```
fitness_nation/
├── app.py                  ← Flask backend (main server)
├── requirements.txt        ← Python dependencies
├── fitness_nation.db       ← SQLite database (auto-created)
├── README.md
├── templates/
│   ├── index.html          ← Main website
│   ├── login.html          ← Admin login page
│   └── admin.html          ← Admin dashboard
└── static/
    ├── css/
    │   └── style.css       ← Website styles
    └── js/
        └── main.js         ← Website scripts
```

---

## ⚙️ SETUP & RUN INSTRUCTIONS

### Step 1 – Install Python (if not already)
Download from: https://www.python.org/downloads/

### Step 2 – Install Flask
```bash
pip install flask
```
Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3 – Run the server
```bash
cd fitness_nation
python app.py
```

### Step 4 – Open in browser
| Page       | URL                          |
|------------|------------------------------|
| Website    | http://127.0.0.1:5000        |
| Admin      | http://127.0.0.1:5000/admin  |
| Login      | http://127.0.0.1:5000/login  |

---

## 🔐 ADMIN CREDENTIALS

| Field     | Value      |
|-----------|------------|
| Username  | admin      |
| Password  | admin123   |

---

## 🗄️ DATABASE

SQLite database is auto-created on first run.

**Table: enquiries**
| Column  | Type    | Description           |
|---------|---------|-----------------------|
| id      | INTEGER | Auto-increment PK     |
| name    | TEXT    | Customer name         |
| phone   | TEXT    | Phone number          |
| plan    | TEXT    | Selected plan         |
| message | TEXT    | Optional message      |
| date    | TEXT    | Date/time submitted   |
| status  | TEXT    | New / Called / Joined |

---

## 🌟 FEATURES

### Website (index.html)
- Sticky navbar with mobile hamburger menu
- Hero section with animated elements
- 4 Membership plans with pricing
- 6 Facilities showcase
- Photo gallery (placeholder-ready)
- 4 Customer testimonials
- About section with owner info
- Contact form with AJAX submission
- Google Maps embed (Shelpimpalgaon, Khed)
- Floating WhatsApp button
- Fully mobile responsive

### Admin Panel
- Secure login / logout
- Dashboard with stats (total, today's count)
- View all enquiries in table
- Search by name, phone, or plan
- Change enquiry status (New / Called / Joined)
- Delete enquiries
- Dark theme with yellow accents

---

## 📞 GYM DETAILS

**Fitness Nation Health Club**
A/P Shelpimpalgaon, Tal-Khed, Dist-Pune, Maharashtra, India
Owner: Nilash Awate
📞 9766694579 / 8605747000
✉️ fitnessnation001@gmail.com

---

*Built with Flask + SQLite + Vanilla JS*
