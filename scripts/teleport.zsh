tp() {
    local cmd="$1"
    local exit_code
    
    # Check if user wants a known command or help
    if [[ "$cmd" == "add" || "$cmd" == "save" || "$cmd" == "list" || "$cmd" == "--help" || "$cmd" == "update" || "$cmd" == "--update" ]]; then
        python3 -m teleport.cli "$@"
        return $?
    fi

    local tmp_file=$(mktemp -t teleport.XXXXXX)
    
    # Default behavior: Jump
    if [[ -z "$cmd" ]]; then
        python3 -m teleport.cli jump --interactive --output-file "$tmp_file"
    else
        python3 -m teleport.cli jump "$@" --output-file "$tmp_file"
    fi
     
    exit_code=$?
    
    # Check if file has content
    if [[ $exit_code -eq 0 && -f "$tmp_file" ]]; then
        local result=$(<"$tmp_file")
        if [[ "$result" == CD:* ]]; then
            local dir=${result#CD:}
            builtin cd "$dir"
        elif [[ "$result" == CMD:* ]]; then
            local command=${result#CMD:}
            print -s "$command"
            echo "Executing: $command"
            eval "$command"
        fi
    fi
    rm -f "$tmp_file"
}
