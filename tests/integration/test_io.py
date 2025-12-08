import os
import pytest
from rrs.core.module import Module
from rrs.core.block import Stone
from rrs.io.exporter import rrs_export
from rrs.io.importer import rrs_import

TEST_FILE = "tests/assets/test_structure.litematic"

@pytest.fixture
def cleanup_file():
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_export_import_roundtrip(cleanup_file):
    # Create a simple structure
    m = Module("TestModule")
    m.add(Stone(pos=(0, 0, 0)))
    m.add(Stone(pos=(0, 1, 0)))
    
    # Export
    rrs_export(m, TEST_FILE, "TestRegion")
    
    assert os.path.exists(TEST_FILE)
    
    # Import
    imported_module = rrs_import(TEST_FILE, "ImportedModule")
    
    # Verify
    assert imported_module.id == "ImportedModule"
    flattened = imported_module.flatten()
    assert len(flattened) == 2
    
    positions = sorted([b.pos for b in flattened])
    assert positions == [(0, 0, 0), (0, 1, 0)]
    
    # Check block types
    for b in flattened:
        assert b.id == "minecraft:stone"
