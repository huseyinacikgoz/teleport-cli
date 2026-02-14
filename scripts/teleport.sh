# Teleport v1.0.0
# Minimalist Shell Wrapper

tp() {
    local cmd="$1"
    
    # 1. Help & Config Handling
    if [[ "$cmd" == "--help" || "$cmd" == "-h" ]]; then
        /opt/teleport-cli/venv/bin/python3 -m teleport.cli help
        return 0
    fi

    # 2. Version
    if [[ "$cmd" == "--version" || "$cmd" == "-v" ]]; then
        echo "Teleport v1.0.0"
        return 0
    fi

    # 3. Known Commands
    case "$cmd" in
        uninstall)
            echo "To uninstall Teleport-CLI, run:"
            echo "sudo apt remove teleport-cli"
            return 0
            ;;
        add|save|list|clean|config|scan)
            /opt/teleport-cli/venv/bin/python3 -m teleport.cli "$@"
            return $?
            ;;
    esac

    # 4. Jump Logic
    local tmp_file=$(mktemp)
    if [[ -z "$cmd" ]]; then
        /opt/teleport-cli/venv/bin/python3 -m teleport.cli jump --interactive --output-file "$tmp_file"
    else
        /opt/teleport-cli/venv/bin/python3 -m teleport.cli jump "$@" --output-file "$tmp_file"
    fi
     
    local exit_code=$?
    
    # 5. Process Result
    if [[ $exit_code -eq 0 && -s "$tmp_file" ]]; then
        local result=$(cat "$tmp_file")
        if [[ "$result" == CD:* ]]; then
            local dir=${result#CD:}
            builtin cd "$dir" 2>/dev/null || echo "Error: Directory not found."
        elif [[ "$result" == CMD:* ]]; then
            local command=${result#CMD:}
            print -s "$command" 2>/dev/null || history -s "$command" 2>/dev/null
            eval "$command"
        fi
    fi
    rm -f "$tmp_file"
}
