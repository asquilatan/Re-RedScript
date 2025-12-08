import argparse
import sys
import os
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter
from rrs.io.exporter import rrs_export

def main():
    parser = argparse.ArgumentParser(description="Re-RedScript CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Compile command
    compile_parser = subparsers.add_parser("compile", help="Compile .rrs file to .litematic")
    compile_parser.add_argument("input", help="Input .rrs file")
    compile_parser.add_argument("-o", "--output", help="Output .litematic file (default: input name + .litematic)")

    args = parser.parse_args()

    if args.command == "compile":
        if not os.path.exists(args.input):
            print(f"Error: File not found {args.input}")
            sys.exit(1)
            
        print(f"Parsing {args.input}...")
        parser_dsl = RRSParser()
        try:
            program = parser_dsl.parse_file(args.input)
        except Exception as e:
            print(f"Parse Error: {e}")
            sys.exit(1)
            
        print("Interpreting...")
        interpreter = Interpreter()
        try:
            results = interpreter.run(program)
        except Exception as e:
            print(f"Runtime Error: {e}")
            sys.exit(1)
            
        if not results:
            print("Warning: No modules executed/instantiated at top level.")
            sys.exit(0)
            
        # Export logic
        output_path = args.output
        if not output_path:
            base_name = os.path.splitext(os.path.basename(args.input))[0]
            output_path = f"{base_name}.litematic"
            
        print(f"Exporting {len(results)} modules...")
        
        if len(results) == 1:
            rrs_export(results[0], output_path)
            print(f"Saved to {output_path}")
        else:
            print(f"Warning: Multiple top-level modules found ({len(results)}). Exporting all.")
            base, ext = os.path.splitext(output_path)
            for i, res in enumerate(results):
                out = f"{base}_{res.id}{ext}" 
                rrs_export(res, out)
                print(f"Saved {res.id} to {out}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()