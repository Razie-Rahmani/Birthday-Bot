# Birthday Bot

A Telegram bot for logging and viewing birthdays in one shared place.

## Features
- `/start` — greets the user and shows the main menu
- **Log Birthday** — guided flow that asks for name, then birthday
- **View Birthdays** — lists all birthdays currently logged
- `/cancel` — exits the log-birthday flow at any point; responds with "Nothing to cancel" if there is no active flow

## Built With
- **Python**
- **[aiogram](https://docs.aiogram.dev/)** — async Telegram bot framework. Chosen because Telegram bots are I/O-bound, which suits an async approach
- **sqlite3** — local storage, no external database required
- **python-dotenv** — keeps the bot token out of source code

## Setup
1. Clone the repo
2. Create a `.env` file in the project root:
   ```
   BOT_TOKEN=your_telegram_bot_token
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python main.py
   ```

## Why I Built This
This is my first programming project. The goal was to build something small enough to finish, but with enough moving parts to require real concepts, not just syntax. Specifically:

- Multi-step conversations using **finite state machines (FSM)**, so the bot tracks where a user is in a flow across multiple messages
- **Async/await** in a working context, not just as a keyword read about in documentation
- **sqlite** for persistence, including schema design and basic `INSERT`/`SELECT` queries
- Project structure fundamentals: environment variables, `.gitignore`, version control from the start

Time spent: 2 months, working 1 hour daily. Self-taught through documentation and trial and error. AI tools (Claude, ChatGPT) were also used throughout as a learning aid — explaining concepts, and reviewing code after it was written to catch issues. All code was written and understood independently; AI was not used to generate the project wholesale.

## Planned for v2
Several features were identified during development that would improve the bot, but were deliberately left out of v1. The reasoning: as a first project, the priority was shipping something complete and working, not maximizing scope. These are intended to be revisited after gaining more experience, so they can be implemented properly rather than added prematurely.

- **Multi-group support** — a `Groups` table with pass-protected group names, so separate groups can maintain independent birthday lists on the same bot instance
- **Admin panel** — a way for group organizers (or the bot owner) to manage entries directly: remove incorrect birthdays, manage members, etc., without relying on individual users to self-correct
- **Stricter date validation** — current input accepts any text as a date; proper validation (leap years, days per month) is needed
- **Additional commands** — `/delete` and `/edit_birthday` for managing existing entries, `/join` for group support
- **Sorting by upcoming date** — ordering the birthday list by proximity to today instead of insertion order
- **Reminders** — messaging users a set number of days before a birthday. This requires a background scheduler and storing each user's chat ID, neither of which exists yet

## What I Learned
When I started this project, my first questions were very basic: "How do I create a project (folders with files in them) in VS Code?" and "How do I create a repository and connect it to VS Code?". The first month was focused only on learning Python syntax, but the second month was where I started learning how actual software projects are built. Over time, my questions changed from "How do I write this?" to "Where should this change happen?", "How should this be structured?", and "How can this be improved in the future?". Through building and deploying this bot, I learned that programming is not only about knowing the language itself, but also about understanding how different parts of a project work together: code structure, databases, version control, deployment, and designing features with future improvements in mind.