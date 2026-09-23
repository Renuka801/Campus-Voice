# Campus Voice

A platform for students to report college-related problems safely — including anonymously — 
so college administration can view, categorize, track, and resolve them.

## Access Control
- Only students with a valid **college email domain** can register (e.g. `@mru.edu.in` — change this in `.env`)
- Registration requires **email + roll number** for identity verification
- Students can still choose to submit any individual complaint **anonymously** — their identity is 
  never attached to that complaint in the database, even though they're logged in (this is what lets 
  them track status later without revealing who they are to admins)
- Admins have a separate role flag and see all complaints with full details

## Issue Categories
- Water Problem
- Hostel Problem
- Lecturer Problem
- Student Related
- Infrastructure
- Academic Issues
- Transportation
- Safety
- Other

## Tech Stack
**Backend:** FastAPI, PostgreSQL, SQLAlchemy, JWT auth, Passlib (bcrypt)
**Frontend:** React + TypeScript, Tailwind CSS, Axios, React Router
**Database:** PostgreSQL (via Supabase/Neon free tier or local Postgres)

## Project Structure
