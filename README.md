# 📦 EasyBash

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📌 Description

EasyBash is a Python CLI tool that simplifies shell workflows by adding higher-level commands for file management, batch automation, and multi-directory execution.

It acts as a productivity layer over traditional shell commands.

---

## 🎯 Purpose

- Reduce repetitive terminal commands
- Improve workflow speed
- Enable batch automation
- Support multi-directory execution

---

## 📥 Installation

git clone https://github.com/sonych995-byte/EasyBash.git
cd EasyBash
chmod +x easybash

---

## 🚀 Run

python easybash.py

Or run from path:

python /path/to/easybash.py

---

## 🌍 Global Setup

Linux / macOS:
chmod +x easybash
sudo mv easybash /usr/local/bin/

Windows:
@echo off
python C:\path\to\easybash.py %*

(Add to PATH)

Termux:
chmod +x easybash
mv easybash $PREFIX/bin/

---

## ⚙️ Commands

### 🔁 for
Run command across multiple directories.

Syntax:
for <file_pattern> in <path1|path2> <command>

Example:
for *.py in src|tests python {}

---

### ⚡ rush
Run commands in parallel directories.

Syntax:
rush <path1|path2> <command>

Example:
rush src|tests git status

---

### 📁 copy
Copy files by pattern.

Syntax:
copy <pattern> to <dest1|dest2> <mode>

Modes:
dir  -> copy into each folder
flat -> copy into single folder

Example:
copy *.log to backup|archive dir

---

### 📦 move
Move files safely (copy then delete).

Syntax:
move <pattern> to <dest1|dest2> <mode>

Example:
move *.tmp to logs|archive flat

---

### 🔍 find
Search files recursively.

Syntax:
find <pattern> in <path1|path2>

Example:
find *.py in src|lib

---

### 📜 batch
Execute commands from file.

Syntax:
batch <file>

Example:
batch commands.txt

---

## 🧠 How it works

1. Parse command
2. Expand paths
3. Execute via subprocess
4. Return output

---

## 🧩 Architecture

- CommandParser
- PathManager
- CommandExecutor

---

## 🌐 Compatibility

Linux     -> full support
macOS     -> full support
Termux    -> full support
Windows   -> partial (needs .bat)
PowerShell-> partial

---

## 🔒 Safety

- move only deletes after success
- batch uses trusted files only
- parallel execution is limited
- recursion is controlled

---

## 📦 Version

v3.0.0

---

## 🔥 Update Notes

Added:
- parallel execution
- batch system
- recursive search
- safe move

Fixed:
- file loss bug
- thread race condition
- unicode batch issue

Improved:
- performance
- error handling
- stability

---

## 💡 Tips

- Use {} as file placeholder
- Use | to separate paths
- Combine with shell commands
- Use batch for automation
