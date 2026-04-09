# EasyBash

EasyBash is a CLI tool designed to make Bash commands **simpler, faster, and more readable**.  
It focuses on reducing repetitive `cd` usage and simplifying long paths.

---

# Purpose

- Reduce repetitive `cd` commands
- Simplify complex file paths
- Separate file operations and folder operations
- Improve developer workflow speed

---

# Core Concept

EasyBash separates commands into two main categories:

| Command | Target | Purpose |
|--------|-------|--------|
| `for` | Files | Perform actions on files |
| `rush` | Folders | Navigate and execute commands in directories |

---

# Installation

## Basic Usage

```bash
python easybash.py
```

---

# Global Command Setup (Use Anywhere)
## termux
```bash
chmod +x easybash
```
```bash
mv easybash $PREFIX/bin/
```
## linux
```bash
chmod +x easybash
```
```bash
sudo mv easybash /usr/local/bin/
```
## macOS
```bash
chmod +x easybash
```
```bash
sudo mv easybash /usr/local/bin/
```
## Windows
### Create a file:
```bash
easybash.bat
```
### Add:
```bash
@echo off
```
```bash
python C:\path\to\easybash.py %*
```
Add to PATH
1. Open Start Menu → Search "Environment Variables"
2. Click "Edit the system environment variables"
3. Go to "Environment Variables"
4. Select Path
5. Click "Edit"
Add your .bat file directory

# Dependencies

EasyBash uses only Python standard library modules, so **no external installation is required**.

---

## Built-in Modules

```text
shlex
subprocess
pathlib
glob
typing
```

# Why EasyBash?

EasyBash makes command-line workflows faster by:

- Eliminating repetitive `cd` commands
- Simplifying long paths
- Providing intuitive syntax for file and folder operations

Example:

Traditional Bash:
cd web && cd myweb && rm logic.py

EasyBash:
for logic.py in web|myweb rm

## 🎬 Demo

![demo](demo.gif)