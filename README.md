# SmartLibrary-Management-System
A desktop based Smart Library Management System built with Python (OOP), PyQt5, and PostgreSQL. Includes book management, loans, members, book clubs, and role based access.
# SmartLibrary – Limkokwing University Central Library System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-orange)](https://riverbankcomputing.com/software/pyqt/intro)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI Status](https://github.com/YOUR-USERNAME/SmartLibrary-Limkokwing/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR-USERNAME/SmartLibrary-Limkokwing/actions/workflows/ci.yml)

> A modern desktop library management system built with **Python (OOP)**, **PostgreSQL**, and **PyQt5**  
> Final Year Group Project – 3 members

## Features
- Role-based login (Librarian ↔ Member)
- Full CRUD for Books, Authors, Members & Book Clubs
- Borrow/Return books (7-day loan, max 3 active loans)
- Advanced search, filter & sorting
- Book Club management
- Real-time dashboard (most borrowed books, active clubs, etc.)
- Clean architecture (Repository Pattern + OOP)
- GitHub Actions CI with tests & linting

## Demo Video (Week 12)
(Will be uploaded before submission – link coming soon)

## Screenshots
<img src="docs/screenshots/login.png" width="49%" /> <img src="docs/screenshots/catalog.png" width="49%" />
<img src="docs/screenshots/loan.png" width="49%" /> <img src="docs/screenshots/dashboard.png" width="49%" />

## Tech Stack
- **Language**: Python 3.11
- **GUI**: PyQt5
- **Database**: PostgreSQL + psycopg2
- **Architecture**: OOP + Repository Pattern
- **DevOps**: GitHub + GitHub Actions

## Quick Setup (≤ 5 minutes)

```bash
# 1. Clone
git clone https://github.com/YOUR-USERNAME/SmartLibrary-Limkokwing.git
cd SmartLibrary-Limkokwing

# 2. Virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database (install PostgreSQL first)
createdb smartlibrary
psql smartlibrary < database/migrations/001_initial_schema.sql

# 5. Run
python src/main.py
