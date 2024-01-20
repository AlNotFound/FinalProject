from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_client, get_excursion_client, \
    get_new_client, borrow_excursion, set_return_date, del_excursion_client

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    if request.values.get('client'):
        client_id = int(request.values.get('client'))
        session['client_id'] = client_id
    elif request.values.get('new_client'):
        new_client = request.values.get('new_client')
        session['client_id'] = get_new_client(conn, new_client)
    elif request.values.get('excursion'):
        excursion_id = int(request.values.get('excursion'))
        borrow_excursion(conn, excursion_id, session['client_id'])
    elif request.values.get('return_val'):
        excursion_client_id = request.values.get("return_val")
        set_return_date(conn, excursion_client_id)
    elif request.values.get('delete'):
        excursion_client_id = request.values.get('excursion_client_id')
        # print(excursion_client_id)
        del_excursion_client(conn, excursion_client_id)
    else:
        if "client_id" in session.keys():
            session['client_id'] = session['client_id']
        else:
            session['client_id'] = 1
    df_client = get_client(conn)
    df_excursion_client = get_excursion_client(conn, session['client_id'])

    html = render_template(
        'index.html',
        client_id=session['client_id'],
        combo_box=df_client,
        excursion_client=df_excursion_client,
        len=len,
    )
    return html
