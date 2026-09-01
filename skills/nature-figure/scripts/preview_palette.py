"""Compatibility entry point for the current six-colour abcd palette preview."""
import sys
from preview_six_colors import main as preview
if __name__=='__main__':
    preview(sys.argv[1] if len(sys.argv)>1 else 'palette-preview')
