#!/usr/bin/env python3
import os
import sys
import unittest

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from overlay.ext_vintage import handle_vintage_command


class DummyView:
    def line_height(self):
        return 20.0

    def viewport_extent(self):
        return (800.0, 400.0)


class TestVintageExtension(unittest.TestCase):
    """Test suite for basic Vintage / Vim navigation commands."""

    def setUp(self):
        self.view = DummyView()

    def test_vi_scroll_lines(self):
        # ctrl+d / ctrl+u: half-page scroll forward / backward
        self.assertEqual(
            handle_vintage_command(self.view, "vi_scroll_lines", {"forward": True}),
            ("scroll_lines", {"amount": -10.0}),
        )
        self.assertEqual(
            handle_vintage_command(self.view, "vi_scroll_lines", {"forward": False}),
            ("scroll_lines", {"amount": 10.0}),
        )

    def test_set_motion_move(self):
        # j / k: move by lines forward / backward
        args_j = {"motion": "move", "motion_args": {"by": "lines", "forward": True}}
        self.assertEqual(
            handle_vintage_command(self.view, "set_motion", args_j),
            ("move", {"by": "lines", "forward": True}),
        )
        args_k = {"motion": "move", "motion_args": {"by": "lines", "forward": False}}
        self.assertEqual(
            handle_vintage_command(self.view, "set_motion", args_k),
            ("move", {"by": "lines", "forward": False}),
        )

    def test_set_motion_goto_line(self):
        # gg / G: jump to top / bottom
        args_gg = {"motion": "vi_goto_line", "motion_args": {"ending": "bof"}}
        self.assertEqual(
            handle_vintage_command(self.view, "set_motion", args_gg),
            ("move_to", {"to": "bof"}),
        )
        args_G = {"motion": "vi_goto_line", "motion_args": {"ending": "eof"}}
        self.assertEqual(
            handle_vintage_command(self.view, "set_motion", args_G),
            ("move_to", {"to": "eof"}),
        )


if __name__ == "__main__":
    unittest.main()
