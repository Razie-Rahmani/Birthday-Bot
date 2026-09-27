# Birthday Bot

A Telegram bot for logging and viewing birthdays in one shared place.

## Features

* `/start` — greets the user and shows the main menu
* **Log Birthday** — guided flow that asks for name, then birthday
* **View Birthdays** — lists all birthdays currently logged
* `/cancel` — exits the log-birthday flow at any point; responds with "Nothing to cancel" if there is no active flow

## Built With

* **Python**
* **[aiogram](https://docs.aiogram.dev/)** — async Telegram bot framework. Chosen because Telegram bots are I/O-bound, which suits an async approach
* **PostgreSQL** — database storage, deployed through Render
* **FastAPI** — ASGI web framework used to handle the Telegram webhook
* **python-dotenv** — keeps environment variables out of source code
* **Render** — deployment platform for the web service and PostgreSQL database

## Setup

1. Clone the repo
2. Create a `.env` file in the project root:

   ```
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL=your_postgresql_database_url
   ```
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Run the bot:

   ```
   python main.py
   ```

The bot uses a webhook in production. The web service and PostgreSQL database are deployed on Render, with the Telegram webhook registered through `set_webhook()`.

## Why I Built This

This is my first programming project. The goal was to build something small enough to finish, but with enough moving parts to require real concepts, not just syntax. Specifically:

* Multi-step conversations using **finite state machines (FSM)**, so the bot tracks where a user is in a flow across multiple messages
* **Async/await** in a working context, not just as a keyword read about in documentation
* **PostgreSQL** for persistence, including schema design and basic database queries
* **Webhooks** and an **ASGI server**, to receive Telegram updates through a deployed web service instead of polling
* Project structure fundamentals: environment variables, `.gitignore`, version control from the start
* **Deployment** using Render, including environment variables, a web service, and a PostgreSQL database

Time spent: 2 months, working 1 hour daily. Self-taught through documentation and trial and error. AI tools (Claude, ChatGPT) were also used throughout as a learning aid — explaining concepts, and reviewing code after it was written to catch issues. All code was written and understood independently; AI was not used to generate the project wholesale.

### v2.1 — Current / In Progress

The project is currently in the middle of moving to v2.1. The main deployment and database changes are complete, while some improvements to the bot's structure and user experience are still in progress.

#### Completed

* ☑️ Change polling to webhook
* ☑️ Register the webhook with Telegram using `set_webhook()`
* ☑️ Use a Render start command to run an ASGI server
* ☑️ Add environment variables
* ☑️ Change SQLite to PostgreSQL on Render
* ☑️ Deploy on Render
* ☑️ Date picker tool

#### Still in Progress

* **Polish** — make the bot look better and improve the UI
* **Upgrade** — make the project more modular (`handlers/`, `services/`, `keyboards/`, etc.)
* **Additional commands** — `/delete` and `/edit_birthday` for managing existing entries, `/join` for group support; requires checking Telegram IDs
* **Sort dates generally** — improve how birthdays are ordered
* **Sort by upcoming date** — order birthdays by proximity to today
* **Reminders** — message users a set number of days before a birthday. This requires a background scheduler and storing each user's chat ID, neither of which exists yet
* **No Duplicate Names Check** — prevent duplicate names regardless of capitalization

### v2.2 — Planned

These are larger features that were identified during development but are being left for the next stage rather than being added while v2.1 is still being finished.

* **Users' profile picture** — each user can add a picture for herself if she wants
* **Admin panel** — one main admin and one admin for each group; first feature will be CRUD operations
* **Create/join group** — add group creation and joining, along with all related features
* **Birthday event planner** — add an event planner for each birthday, including place, people, theme, and a way for the birthday person to send invitations to their friends

## What I Learned

When I started this project, my first questions were very basic: "How do I create a project (folders with files in them) in VS Code?" and "How do I create a repository and connect it to VS Code?". The first month was focused only on learning Python syntax, but the second month was where I started learning how actual software projects are built.

Over time, my questions changed from "How do I write this?" to "Where should this change happen?", "How should this be structured?", and "How can this be improved in the future?". Through building and deploying this bot, I learned that programming is not only about knowing the language itself, but also about understanding how different parts of a project work together: code structure, databases, version control, deployment, and designing features with future improvements in mind.