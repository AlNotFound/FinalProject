from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_organizator_count, get_guide_count, get_typeExcursion_count, get_filtered_excursion, get_all_organizator, get_all_guide, get_all_typeExcursion

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()

    selected_organizator = []
    selected_guide = []
    selected_typeExcursion = []

    df_organizator = get_organizator_count(conn)
    df_guide = get_guide_count(conn)
    df_typeExcursion = get_typeExcursion_count(conn)
    df_excursion = get_filtered_excursion(
            conn,
            get_all_organizator(conn),
            get_all_guide(conn),
            get_all_typeExcursion(conn)
        )
    
    if request.method == 'POST':
        if 'confirm' in request.form:
            selected_organizator = request.form.getlist("organizator")
            selected_guide = request.form.getlist("guide")
            selected_typeExcursion = request.form.getlist("typeExcursion")

        if 'reset' in request.form:
            selected_organizator = []
            selected_guide = []
            selected_typeExcursion = []
        
        df_excursion = get_filtered_excursion(
            conn,
            get_all_organizator(conn) if not selected_organizator else selected_organizator,
            get_all_guide(conn) if not selected_guide else selected_guide,
            get_all_typeExcursion(conn) if not selected_typeExcursion else selected_typeExcursion
        )

    html = render_template(
        'search.html',
        selected_organizator=selected_organizator,
        df_organizator=df_organizator,
        selected_guide=selected_guide,
        df_guide=df_guide,
        selected_typeExcursion=selected_typeExcursion,
        df_typeExcursion=df_typeExcursion,
        df_excursion=df_excursion
    )
    return html
