#!/usr/bin/env python3
import os
import subprocess
import pickle
from pathlib import Path

SESSION_FILE = Path.home() / ".git_submodule_checked.pkl"

# Загружаем список уже проверенных репозиториев
if SESSION_FILE.exists():
    try:
        with open(SESSION_FILE, "rb") as f:
            checked_repos = pickle.load(f)
    except Exception:
        checked_repos = set()
else:
    checked_repos = set()

def save_checked_repos():
    with open(SESSION_FILE, "wb") as f:
        pickle.dump(checked_repos, f)

def is_git_repo(path):
    return subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

def get_uninitialized_submodules(path):
    try:
        result = subprocess.run(
            ["git", "submodule", "status"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        lines = result.stdout.strip().splitlines()
        return [l for l in lines if l.startswith("-")]
    except Exception:
        return []

def main():
    cwd = os.getcwd()
    if not is_git_repo(cwd) or cwd in checked_repos:
        return

    uninit = get_uninitialized_submodules(cwd)
    if uninit:
        print(f"\nОбнаружены неинициализированные подмодули в {cwd}:")
        for line in uninit:
            print(" ", line)
        choice = input("Вы хотите их клонировать? [y/n]: ").strip().lower()
        if choice == "y":
            subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=cwd)
            print("Подмодули успешно клонированы.")

    # отмечаем как проверенный
    checked_repos.add(cwd)
    save_checked_repos()

if __name__ == "__main__":
    main()

