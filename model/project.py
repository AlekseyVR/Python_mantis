from sys import maxsize


class Project:

    def __init__(self, name_project=None, description_project=None, status_project=None, view_status_project=None, id=None):
        self.name_project = name_project
        self.description_project = description_project
        self.status_project = status_project
        self.view_status_project = view_status_project
        self.id = id

    def __repr__(self):
        return "%s:%s;%s" % (self.id, self.name_project, self.description_project)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name_project == other.name_project and \
               self.description_project == other.description_project


    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

