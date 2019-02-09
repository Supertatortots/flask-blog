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