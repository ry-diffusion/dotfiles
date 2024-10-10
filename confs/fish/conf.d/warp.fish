if status is-interactive
    if test "$TERM_PROGRAM" = WarpTerminal
        #echo bugcheck: on warp! THIS SHOULDN\'T APPEAR ON A WARP SHELL.
        printf '\eP$f{"hook": "SourcedRcFileForWarp", "value": { "shell": "fish" }}\x9c'

        # Turn off syntax highlighting
        for color in fish_color_command fish_color_comment fish_color_end \
            fish_color_escape fish_color_match fish_color_operator \
            fish_color_param fish_color_search_match fish_color_quote \
            fish_pager_color_description fish_pager_color_prefix
            set -g $color normal
        end

        set -g fish_color_autosuggestion white
        set -g fish_color_error red

        set -g fish_pager_color_progress white
    end
end
