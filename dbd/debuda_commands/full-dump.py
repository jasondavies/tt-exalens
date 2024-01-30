"""
Usage:
  fd

Description:
  Dumps all stream configuration at the currently selected core.

Examples:
  fd
"""

command_metadata = {"short": "fd", "type": "dev", "description": __doc__}


def run(cmd_text, context, ui_state=None):
    ui_state["current_device"].full_dump_xy(ui_state["current_loc"])

    return None
