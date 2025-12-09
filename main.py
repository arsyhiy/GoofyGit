#!/usr/bin/env python3
import os
import subprocess
import sys

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
        # "-" в начале означает, что подмодуль не клонирован
        return [l for l in lines if l.startswith("-")]
    except Exception:
        return []

def main():
    path = os.getcwd()

    if not is_git_repo(path):
        return  # не репозиторий, молчим

    uninit = get_uninitialized_submodules(path)
    if not uninit:
        return  # все подмодули уже есть, молчим

    print("Обнаружены подмодули, которые ещё не клонированы:")
    for line in uninit:
        print(" ", line)

    choice = input("Вы хотите их клонировать? [y/n]: ").strip().lower()
    if choice == "y":
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=path
        )
        print("Подмодули успешно клонированы.")

if __name__ == "__main__":
    main()
