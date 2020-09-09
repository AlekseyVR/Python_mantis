from model.project import Project
import random


def test_add_project(app):
    app.session.login("administrator", "root")
    project = Project(name_project="name_" + str(random.randrange(30)), description_project="description_" + str(random.randrange(50)))
    old_project = app.project.get_project_list()
    app.project.add_project(project)
    new_project = app.project.get_project_list()
    old_project.append(project)
    print("old_project: ", old_project, "new_project: ", new_project)
    assert sorted(old_project, key=Project.id_or_max) == sorted(new_project, key=Project.id_or_max)
