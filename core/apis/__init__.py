# from core import app
# from .responses import APIResponse
# app.response_class = APIResponse
from flask import Blueprint

from core.apis.assignments import principal_assignments_resources
from core.apis.teachers import principal_teacher_resources

principal_resources = Blueprint('principal_resources', __name__)

principal_resources.register_blueprint(principal_assignments_resources, url_prefix='/assignments')
principal_resources.register_blueprint(principal_teacher_resources, url_prefix='/teachers')

