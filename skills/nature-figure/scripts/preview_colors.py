"""Compatibility entry point: render the five-colour supplemental preview."""
import sys
from preview_palette import preview
if __name__ == '__main__':
    preview(sys.argv[1] if len(sys.argv)>1 else 'template-preview')
