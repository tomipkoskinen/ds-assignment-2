from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import xml.etree.ElementTree as ET

import requests


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class Notebook:
        def health(self) -> str:
            return "ok"

        def add_note(self, topic: str, name: str, text: str, timestamp: str) -> bool:
            tree = ET.parse("db.xml")
            root = tree.getroot()

            topic_exists = False
            for topic_el in root.findall("topic"):
                if topic_el.attrib["name"] == topic:
                    topic_exists = True
                    note_el = ET.SubElement(topic_el, "note")
                    note_el.attrib["name"] = name
                    text_el = ET.SubElement(note_el, "text")
                    text_el.text = text
                    timestamp_el = ET.SubElement(note_el, "timestamp")
                    timestamp_el.text = timestamp
                    break
            
            if not topic_exists:
                topic_el = ET.SubElement(root, "topic")
                topic_el.attrib["name"] = topic
                note_el = ET.SubElement(topic_el, "note")
                note_el.attrib["name"] = name
                text_el = ET.SubElement(note_el, "text")
                text_el.text = text
                timestamp_el = ET.SubElement(note_el, "timestamp")
                timestamp_el.text = timestamp

            tree.write("db.xml")
            return True

        def get_notes(self, topic) -> list:
            tree = ET.parse("db.xml")
            root = tree.getroot()

            notes = []

            for topic_el in root.findall("topic"):
                if topic_el.attrib["name"] == topic:
                    for note_el in topic_el.findall("note"):
                        note = {
                            "name": note_el.get("name"),
                            "text": note_el.find("text").text,
                            "timestamp": note_el.find("timestamp").text
                        }
                        notes.append(note)
            return notes

    server.register_instance(Notebook())

    # Run the server's main loop
    server.serve_forever()
