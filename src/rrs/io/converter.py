import json
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

import litemapy


@dataclass
class BlockRecord:
    block_id: str
    position: Tuple[int, int, int]
    properties: Dict[str, str]


class LitematicConverter:
    """Converts .litematic schematics into raw RRS source files."""

    def convert(self, input_path: str, output_path: str | None = None, module_name: str | None = None) -> str:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Litematic file not found: {input_path}")

        schem = litemapy.Schematic.load(input_path)
        module_name = module_name or self._derive_module_name(input_path)
        output_path = output_path or self._default_output_path(input_path)

        script = self._generate_script(schem, module_name, os.path.basename(input_path))
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(script)
        return output_path

    def _default_output_path(self, source_path: str) -> str:
        base, _ = os.path.splitext(source_path)
        return f"{base}.rrs"

    def _derive_module_name(self, source_path: str) -> str:
        base = os.path.splitext(os.path.basename(source_path))[0]
        tokens = [re.sub(r"[^0-9a-zA-Z]", "", part) for part in re.split(r"[^0-9a-zA-Z]+", base)]
        tokens = [token for token in tokens if token]
        if not tokens:
            return "ConvertedModule"
        candidate = "".join(token.capitalize() for token in tokens)
        if candidate[0].isdigit():
            candidate = f"M{candidate}"
        return candidate

    def _generate_script(self, schem: litemapy.Schematic, module_name: str, source_name: str) -> str:
        entries = self._collect_blocks(schem)
        lines: List[str] = [f"# Auto-generated from {source_name}", "", f"module {module_name}():"]

        if not entries:
            lines.append("    pass")
        else:
            for record in entries:
                lines.append(f"    {self._render_block(record)}")

        lines.extend(["", f"m = {module_name}()", "export(m)", ""])
        return "\n".join(lines) + "\n"

    def _collect_blocks(self, schem: litemapy.Schematic) -> List[BlockRecord]:
        records: List[BlockRecord] = []
        for region in schem.regions.values():
            offset = (region.x, region.y, region.z)
            for (x, y, z) in region.block_positions():
                state = region[x, y, z]
                if state.id == "minecraft:air":
                    continue
                world_pos = (offset[0] + x, offset[1] + y, offset[2] + z)
                props = dict(state.properties()) if len(state) else {}
                records.append(BlockRecord(block_id=state.id, position=world_pos, properties=props))
        records.sort(key=lambda rec: (rec.position[0], rec.position[1], rec.position[2], rec.block_id))
        return records

    def _render_block(self, record: BlockRecord) -> str:
        args = [json.dumps(record.block_id), f"pos={self._format_position(record.position)}"]
        for key in sorted(record.properties.keys()):
            args.append(f"{key}={json.dumps(record.properties[key])}")
        return f"Block({', '.join(args)})"

    def _format_position(self, position: Tuple[int, int, int]) -> str:
        return f"({position[0]}, {position[1]}, {position[2]})"