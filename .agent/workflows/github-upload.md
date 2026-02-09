---
description: How to upload the Study Buddy Bot to GitHub
---

Follow these steps to upload your project to GitHub safely:

### 1. Initialize Git and Add Files
Open your terminal in the project directory and run:
```powershell
git add .
git commit -m "Initial commit: Redesigned UI and optimized agent"
```

### 2. Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Name your repository (e.g., `study-buddy-bot`).
3. Keep it **Public** or **Private**.
4. **DO NOT** initialize with README, license, or gitignore (we already have them).
5. Click **Create repository**.

### 3. Connect and Push
Copy the commands from the GitHub "Quick setup" page (specifically the "push an existing repository from the command line" section):
```powershell
git remote add origin https://github.com/YOUR_USERNAME/study-buddy-bot.git
git branch -M main
git push -u origin main
```

> [!IMPORTANT]
> Your `.env` file is already in `.gitignore`, so your API keys will **not** be uploaded. This is critical for security!
