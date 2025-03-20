import xml.etree.ElementTree as ET

def main():
    root = ET.Element("data")
    tree = ET.ElementTree(root)
    tree.write("db.xml")

main()
