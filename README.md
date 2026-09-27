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
   INTERNAL_DATABASE_URL=your_internal_postgresql_database_url
   EXTERNAL_DATABASE_URL=your_external_postgresql_database_url
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
* ☑️ No duplicate names within the same group - regardless of capitalisation
* ☑️ Modularized

#### Still in Progress

A single flat feature list turned out to hide real dependencies between features — several items only make sense once an earlier one exists (reminders need real per-user Telegram IDs, which need groups to exist first, and so on). So this is now ordered as build phases, each depending on the one before it, rather than a loose checklist.

**Phase 1 — Schema foundation**
Nothing else below can be built correctly until this is in place.
* `Users` table — `telegram_id`, `name`, `birthday`
* `Groups` table — `id`, `name`, `password_hash`
* `GroupMembers` join table — `user_id`, `group_id` (includes a `role` column now, defaulted to `"member"`, so the v2.2 admin panel doesn't need its own migration later)
* Retire the old `Birthdays` table and the free-typed-name logging flow entirely
* Update `services/`, `handlers/`, and `states/` to operate on Users/Groups/GroupMembers instead of the old model

**Phase 2 — Onboarding & registration**
* First-ever `/start` → "Join existing group" or "Create new group" (one-time only, per person)
* Every later `/start` → auto-enters their one group, or asks which one if they belong to several
* **Log Birthday** → becomes "register your own birthday," read from `message.from_user`, no more typing someone else's name

**Phase 3 — Group management surface**
* "Groups" button on the main menu → join another group, create another, or switch between groups already joined; only place a password is entered outside first-time onboarding

**Phase 4 — Additional commands**
* `/delete` and `/edit_birthday`, each scoped to the caller's own `telegram_id` — this is what "requires checking Telegram IDs" turns into once Phase 1 exists: a user's ID *is* their row, so there's no ambiguity left to resolve
* `/join` — same mechanism as the Phase 3 "Groups" button, exposed as a command

**Phase 5 — Sorting**
* Sort dates generally
* Sort by upcoming date

Both scoped per group rather than globally, now that groups are real.

**Phase 6 — Reminders**
* Background scheduler
* Per-group notification to other members ahead of a birthday ("Sara's birthday is in 1 week")
* Separate, one-off "Happy birthday" DM sent directly to the birthday person

This is the most dependent feature on the list — it needs groups, membership, and real per-user Telegram IDs, all from earlier phases, to know who to message and where.

**Phase 7 — Polish**
* UI/UX pass on wording, menus, and flow

Deliberately last — no point polishing surfaces that are still changing shape through Phases 1–6.

### v2.2 — Planned

These are larger features that were identified during development but are being left for the next stage rather than being added while v2.1 is still being finished.

* **Users' profile picture** — each user can add a picture for herself if she wants
* **Admin panel** — one main admin and one admin for each group; first feature will be CRUD operations
* **Birthday event planner** — add an event planner for each birthday, including place, people, theme, and a way for the birthday person to send invitations to their friends

### v3 — Planned

Frontend work — a proper interface beyond Telegram's own chat UI. Nothing about v2.1 or v2.2 is being built with this as a hard requirement, but the modular `services/`/`handlers/` split means a future frontend could call the same `services/` functions the Telegram handlers already use, through new FastAPI routes, without needing to touch or duplicate the underlying group/birthday logic.

## What I Learned

When I started this project, my first questions were very basic: "How do I create a project (folders with files in them) in VS Code?" and "How do I create a repository and connect it to VS Code?". The first month was focused only on learning Python syntax, but the second month was where I started learning how actual software projects are built.

Over time, my questions changed from "How do I write this?" to "Where should this change happen?", "How should this be structured?", and "How can this be improved in the future?". Through building and deploying this bot, I learned that programming is not only about knowing the language itself, but also about understanding how different parts of a project work together: code structure, databases, version control, deployment, and designing features with future improvements in mind.