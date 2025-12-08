import argparse
import sys
import os
from rrs.dsl.parser import RRSParser
from rrs.dsl.interpreter import Interpreter
from rrs.io.exporter import rrs_export
from rrs.io.converter import LitematicConverter

def main():
    parser = argparse.ArgumentParser(description="Re-RedScript CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Compile command
    compile_parser = subparsers.add_parser("compile", help="Compile .rrs file to .litematic")
    compile_parser.add_argument("input", help="Input .rrs file")
    compile_parser.add_argument("-o", "--output", help="Output .litematic file (default: input name + .litematic)")

    convert_parser = subparsers.add_parser("convert", help="Convert .litematic file to .rrs script")
    convert_parser.add_argument("input", help="Input .litematic file")
    convert_parser.add_argument("-o", "--output", help="Output .rrs file (default: input name + .rrs)")
    convert_parser.add_argument("--module-name", help="Override the generated module name", dest="module_name")

    args = parser.parse_args()

    if args.command == "compile":
        try:
            compile_file(args.input, args.output)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif args.command == "convert":
        try:
            convert_file(args.input, args.output, args.module_name)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()

def compile_file(input_path, output_path=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found {input_path}")
        
    print(f"Parsing {input_path}...")
    parser_dsl = RRSParser()
    program = parser_dsl.parse_file(input_path)
    
    print("Interpreting...")
    interpreter = Interpreter()
    results = interpreter.run(program)
    
    if not results:
        print("Warning: No modules executed/instantiated at top level.")
        return
        
    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
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
    
    return output_path

def convert_file(input_path, output_path=None, module_name=None):
    converter = LitematicConverter()
    result = converter.convert(input_path, output_path, module_name)
    print(f"Saved script to {result}")
    return result

if __name__ == "__main__":
    main()