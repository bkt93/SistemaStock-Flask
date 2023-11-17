

from flask import Blueprint, render_template

hardware_bp = Blueprint('hardware', __name__)

@hardware_bp.route('/hardware')
def index():
    return render_template('/hardware/hardware.html')