tp() {
    local cmd="$1"
    local exit_code
    
    # Check if user wants a known command or help
    if [[ "$cmd" == "add" || "$cmd" == "save" || "$cmd" == "list" || "$cmd" == "--help" || "$cmd" == "update" || "$cmd" == "--update" ]]; then
        teleport-core "$@"
        return $?
    fi

    local tmp_file=$(mktemp)
    
    # Default behavior: Jump
    # If no args, interactive. If args, search.
    if [[ -z "$cmd" ]]; then
        teleport-core jump --interactive --output-file "$tmp_file"
    else
        teleport-core jump "$@" --output-file "$tmp_file"
    fi
     
    exit_code=$?
    
    if [[ $exit_code -eq 0 && -s "$tmp_file" ]]; then
        local result=$(cat "$tmp_file")
        if [[ "$result" == CD:* ]]; then
            local dir=${result#CD:}
            cd "$dir"
        elif [[ "$result" == CMD:* ]]; then
            local command=${result#CMD:}
            echo "Executing: $command"
            history -s "$command"
            eval "$command"
        fi
    fi
    rm -f "$tmp_file"
}
