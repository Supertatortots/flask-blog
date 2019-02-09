#app.py

import datetime
import functools
import os
import re
import urllib

from flask import (Flask, abort, flash, Markup, redirect, render_template, request, Response, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite.CodeHiliteExtention
from markdown.extensions.extra import ExtraExtention
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *

class Entry(flask_db.Model):
  title = CharField()
  slug = CharField(unique=True)
  content = TextField()
  published = BooleanField(index=True)
  timestamp = DateTimeField(default=datetime.datetime.now, index=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = re.sub('[^\w]+', '-', self.title.lower())
    ret = super(Entry, self).save(*args, **kwargs)

    #store search component
    self.update_search_index()
    return ret
  def update_search_index(self):
    search_content = '\n'.join((self.title, self.content))
    try:
      fts_entry = FTSEntry.get(FTSEntry.docid == self.id)
    except FTSEntry.DoesNotExist:
      FTSEntry.create(docid=self.id, content=search_content)
    else:
      fts_entry.content = search_content
      fts_entry.save()

class FTSEntry(FTSmodel):
  content = SearchField()

class Meta:
  database = database

  