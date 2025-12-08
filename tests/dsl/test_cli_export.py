import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from rrs.cli import compile_file

TEST_RRS = "tests/assets/test_script.rrs"
TEST_OUT = "tests/assets/test_script.litematic"

@pytest.fixture
def cleanup_files():
    yield
    if os.path.exists(TEST_RRS):
        os.remove(TEST_RRS)
    if os.path.exists(TEST_OUT):
        os.remove(TEST_OUT)

def test_cli_compile_export(cleanup_files):
    # Create a test .rrs file
    with open(TEST_RRS, 'w') as f:
        f.write('Piston(pos=(0,0,0), facing="up")\n')
        
    compile_file(TEST_RRS, TEST_OUT)
    
    assert os.path.exists(TEST_OUT)
    # We could verify content with rrs_import but that's covered in core tests.
    # Here we just check if CLI flow works.
