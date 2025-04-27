# 🛠️ CodexContinue Git Workflow Cheatsheet

## 🛡️ Golden Rules
- Always **commit small changes** (don't stack everything)
- Always **write a meaningful commit message**
- Always **pull before pushing** (stay in sync)
- Never **push broken or untested code**
- Never **commit .venv/**, **node_modules/**, or private secrets
- Always **check git status** before committing

---

## 🔥 Essential Git Commands

| Command | Purpose |
| :------ | :------ |
| `git status` | See what's changed |
| `git add .` | Stage **everything** |
| `git add path/to/file.py` | Stage **specific file** |
| `git commit -m "message"` | Save changes locally |
| `git push` | Upload your commits to GitHub |
| `git pull` | Fetch & merge latest changes |
| `git checkout -b feature/my-feature` | Create & switch to new branch |
| `git branch` | List all branches |
| `git checkout main` | Switch back to main |
| `git merge feature/my-feature` | Merge feature branch into main |
| `git log --oneline --graph --all` | Beautiful graph of commits |
| `git reset HEAD~1` | Undo the last commit (keep code) |
| `git revert <commit_id>` | Revert a specific commit safely |
| `git stash` | Temporarily save uncommitted changes |
| `git stash pop` | Reapply stashed changes |

---

## 🚨 Caution Commands (Use Carefully)

| Command | Purpose |
| :------ | :------ |
| `git reset --hard` | WARNING: Discards ALL local changes |
| `git push --force` | WARNING: Force push (can overwrite history!) |

---

> 📚 Keep this file open in a second tab when working!  
> 📜 Updated by Captain MO + CodexContinue Assistant
