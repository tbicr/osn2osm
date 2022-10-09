#!/usr/bin/python

import sys
import warnings

import jinja2
import lxml.etree


template = '''<?xml version="1.0" encoding="UTF-8"?>
<osm version="0.6" generator="osm notes">
  <bounds minlon="-180" minlat="-90" maxlon="180" maxlat="90" origin="http://www.openstreetmap.org/api/0.6"/>
{% for note in notes %}
  <node id="{{ note.id }}" version="{{ note.version }}" timestamp="{{ note.timestamp }}" uid="{{ note.uid }}" user="{{ note.user }}" changeset="{{ note.changeset }}" lat="{{ note.lat }}" lon="{{ note.lon }}">
    <tag k="name" v="{{ note.content }}"/>
    <tag k="osm_note" v="yes"/>
  </node>{% endfor %}
</osm>
'''


class Comment(object):

    __slots__ = ('action', 'timestamp', 'uid', 'user', 'text')

    def __init__(self, element):
        self.action = element.attrib['action']
        self.timestamp = element.attrib['timestamp']
        self.uid = element.attrib.get('uid', 0)
        self.user = element.attrib.get('user', 'anonimous')
        self.text = element.text


class Note(object):

    __slots__ = ('id', 'lat', 'lon', 'created_at', 'closed_at', 'comments')

    def __init__(self, element):
        self.id = element.attrib['id']
        self.lat = element.attrib['lat']
        self.lon = element.attrib['lon']
        self.created_at = element.attrib['created_at']
        self.closed_at = element.attrib.get('closed_at')
        self.comments = tuple(Comment(_) for _ in element.iterchildren('comment'))

    @property
    def version(self):
        return len(self.comments)

    @property
    def changeset(self):
        return self.id

    @property
    def user(self):
        return self.comments[0].user

    @property
    def uid(self):
        return self.comments[0].uid

    @property
    def timestamp(self):
        return self.created_at

    @property
    def content(self):
        return '\n'.join(
            '%s by %s at %s: %s' % (_.action, _.user, _.timestamp, _.text)
            for _ in self.comments
        )


def _clear_xml_element(element):
    element.clear()
    for ancestor in element.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]


def parse_notes(notes_dump):
    for event, element in lxml.etree.iterparse(notes_dump, events=('end',),
                                               tag='note', recover=True):
        if not element.attrib.get('closed_at'):
            node = Note(element)
            if node.comments:
                yield node
            else:
                warnings.warn(f'{node.id} note has no comments')
        _clear_xml_element(element)


def do():
    stdin = sys.stdin if sys.version_info.major == 2 else sys.stdin.buffer
    stdout = sys.stdout if sys.version_info.major == 2 else sys.stdout.buffer
    notes = parse_notes(stdin)
    for chunk in jinja2.Template(template, autoescape=True).generate(notes=notes):
        stdout.write(chunk.encode('utf8'))


if __name__ == '__main__':
    do()
