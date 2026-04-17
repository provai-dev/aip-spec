#!/usr/bin/env python3
"""
XInclude resolver for xml2rfc v3.32+ compatibility.

Uses lxml to properly resolve xi:include directives, producing
a single self-contained XML file suitable for xml2rfc processing.
"""

import argparse
import sys
from pathlib import Path
from lxml import etree


def resolve_xincludes(input_path, output_path):
    """Resolve all XInclude directives using lxml."""
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {input_file}...", file=sys.stderr)
    
    try:
        parser = etree.XMLParser(resolve_entities=True)
        tree = etree.parse(str(input_file), parser)
        
        base_url = input_file.absolute().as_uri()
        tree.xinclude()
        
        with open(output_file, 'wb') as f:
            tree.write(f, xml_declaration=True, encoding='UTF-8', pretty_print=True)
        
        print(f"✓ Generated {output_file} with XIncludes resolved", file=sys.stderr)
        return True
        
    except etree.XIncludeError as e:
        print(f"Error: XInclude processing failed: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Resolve XInclude directives in draft.xml')
    parser.add_argument('--input', '-i', default='draft.xml', help='Input XML file')
    parser.add_argument('--output', '-o', default='draft-expanded.xml', help='Output XML file')
    parser.add_argument('--validate', '-v', action='store_true', help='Validate output with xmllint')
    args = parser.parse_args()

    if resolve_xincludes(args.input, args.output):
        if args.validate:
            import subprocess
            result = subprocess.run(['xmllint', '--noout', args.output], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ XML validation passed", file=sys.stderr)
            else:
                print(f"✗ XML validation failed: {result.stderr}", file=sys.stderr)
                sys.exit(1)
        
        print(f"Build with: xml2rfc {args.output} --html -o draft.html", file=sys.stderr)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
