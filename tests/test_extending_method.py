
from dataclasses import dataclass
from flex_dispatch import dispatcher

@dataclass
class Person:
    name: str
    age: int
    city: str

    @dispatcher
    @staticmethod
    def parse_person(person) -> 'Person':  # type: ignore
        if isinstance(person, str):
            if person.strip().startswith('{'):
                return 'json'  # type: ignore
        elif isinstance(person, dict):
            return dict  # type: ignore

    @parse_person.map('json')
    @staticmethod
    def _parse_person_json(person: str) -> 'Person':
        import json
        return Person(**json.loads(person))

    @parse_person.map(dict)
    @staticmethod
    def _parse_person_dict(person: dict) -> 'Person':
        return Person(**person)


def parse_person_xml_dispatcher(person: any):
    if isinstance(person, str) and person.strip().startswith('<'):
        return 'xml'

Person.parse_person.extend(parse_person_xml_dispatcher)

@Person.parse_person.map('xml')
def parse_person_xml(person: str) -> Person:
    from xml.dom.minidom import parseString
    doc = parseString(person).documentElement
    return Person(
        name=doc.getAttribute('name'),
        age=int(doc.getAttribute('age')),
        city=doc.getAttribute('city')
    )
    return None

def test_extending_method():
    assert Person('Bob', 3, 'NYC') == Person.parse_person('<Person name="Bob" age="3" city="NYC" />')



