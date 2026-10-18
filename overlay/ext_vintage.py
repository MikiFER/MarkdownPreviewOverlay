"""
Vim / Vintage mode extension support for Markdown Preview Overlay.

Translates Vintage mode navigation commands (vi_scroll_lines, set_motion)
into standard preview navigation commands (move, move_to, scroll_lines).
"""

NOOP = ("markdown_preview_overlay_noop", {})


def handle_vintage_command(view, command_name, args):
    """
    Translate a Vintage navigation command into a normalized command tuple.

    Returns (command_name, args) to dispatch, or None if not a recognized
    Vintage command.
    """
    args = args or {}
    if command_name == "vi_scroll_lines":
        forward = args.get("forward", True)
        line_h = view.line_height()
        half_page = max(1.0, (view.viewport_extent()[1] / line_h / 2.0)) if line_h > 0 else 10.0
        return ("scroll_lines", {"amount": -half_page if forward else half_page})

    if command_name == "set_motion":
        motion = args.get("motion")
        motion_args = args.get("motion_args") or {}

        if motion == "move":
            if motion_args.get("word_begin") or motion_args.get("word_end"):
                return NOOP
            return ("move", motion_args)

        if motion == "move_to":
            return ("move_to", motion_args)

        if motion == "vi_goto_line":
            return ("move_to", {"to": motion_args.get("ending")})

        return NOOP

    return None
