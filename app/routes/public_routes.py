from flask import Blueprint, render_template
from datetime import datetime

#public_bp = Blueprint('public', __name__)

public_bp = Blueprint('public', __name__, template_folder='../templates'  
# para entrar en templates/
)


@public_bp.route('/')
def home():
    fecha_actual = datetime.now().strftime('%Y')
    return render_template('/base.html', fecha_completa=fecha_actual)
