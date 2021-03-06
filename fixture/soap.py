from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list_user(self, username, password):
        self.can_login(username, password)
        client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")

        try:
            response = client.service.mc_projects_get_user_accessible(username, password)
            project_list = []
            for element in response:
                project = Project(id=element.id, name_project=element.name, description_project=element.description)
                project_list.append(project)
            return project_list
        except WebFault:
            return False

