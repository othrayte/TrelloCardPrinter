"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from TrelloCardPrinter import app
from flask import request
import json

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html'
    )

@app.route('/print', methods=['POST'])
def print():
    """Renders the contact page."""
    jsonData = json.loads(request.form['json'])
    checklists = {checklist['id']: {
                    'name': checklist['name'] or "",
                    'checklistItems': [{'name': item['name'] or "", 'state': item['state'] or ""} for item in checklist['checkItems']]
                  } for checklist in jsonData['checklists']}
    lists = {list_['id']: {
        'name': list_['name'] or "",
        'closed': bool(list_['closed']),
        'position': list_['pos']
        } for list_ in jsonData['lists']}

    cards = [{
        'name': card['name'],
        'desc': card['desc'],
        'checklists': [checklists[id] for id in card['idChecklists']]
        } for card in jsonData['cards'] if not lists[card['idList']]['closed']]
    
    return render_template(
        'print.html',
        cards=cards
    )
