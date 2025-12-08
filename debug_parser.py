from rrs.dsl.parser import RRSParser

parser = RRSParser()
code = """module MyMod(x, y):
    Stone(pos=(x, y, 0))
"""
try:
    tree = parser.parse(code)
    print("Success!")
    print(tree)
except Exception as e:
    print(e)
