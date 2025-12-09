#!/usr/bin/env bash

# Папка для скрипта
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Копируем скрипт
cp main.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/main.py"

echo "Скрипт установлен в $INSTALL_DIR/main.py"

# Проверяем оболочку и автоматически добавляем hook
SHELL_NAME=$(basename "$SHELL")

if [[ "$SHELL_NAME" == "bash" ]]; then
    RC_FILE="$HOME/.bashrc"
    HOOK='
# Auto Git Submodule Check
export PREV_DIR=""
function auto_check_submodules() {
    [[ $- != *i* ]] && return
    if [[ "$PWD" != "$PREV_DIR" ]]; then
        PREV_DIR="$PWD"
        python3 "$HOME/.local/bin/main.py"
    fi
}
PROMPT_COMMAND="auto_check_submodules;$PROMPT_COMMAND"
'
elif [[ "$SHELL_NAME" == "zsh" ]]; then
    RC_FILE="$HOME/.zshrc"
    HOOK='
autoload -U add-zsh-hook
function auto_check_submodules() {
    python3 "$HOME/.local/bin/main.py"
}
add-zsh-hook chpwd auto_check_submodules
auto_check_submodules
'
else
    echo "Ваша оболочка ($SHELL_NAME) не поддерживается автоматически. Добавьте вызов скрипта вручную."
    exit 0
fi

# Проверяем, есть ли уже hook
if ! grep -Fq "main.py" "$RC_FILE"; then
    echo "$HOOK" >> "$RC_FILE"
    echo "Автоматический hook добавлен в $RC_FILE"
else
    echo "Hook уже присутствует в $RC_FILE"
fi

echo "Установка завершена. Перезапустите терминал для активации."

