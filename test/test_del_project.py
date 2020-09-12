from model.project import Project
import random


def test_delete_project(app):
    app.session.login("administrator", "root")
    if len(app.project.get_project_list()) == 0:
        app.project.add_project(Project(name_project="name_del_" + str(random.randrange(30)), description_project="description_del_" + str(random.randrange(50))))
    old_project = app.project.get_project_list()
    project = random.choice(old_project)
    app.project.delete_project(project)
    new_project = app.project.get_project_list()
    old_project.remove(project)
    assert sorted(old_project, key=Project.id_or_max) == sorted(new_project, key=Project.id_or_max)

def test_delete_project_soap(app):
    app.session.login("administrator", "root")
    if len(app.project.get_project_list()) == 0:
        app.project.add_project(Project(name_project="name_del_" + str(random.randrange(30)), description_project="description_del_" + str(random.randrange(50))))
    old_project = app.soap.get_project_list_user("administrator", "root")
    project = random.choice(old_project)
    app.project.delete_project(project)
    new_project = app.soap.get_project_list_user("administrator", "root")
    old_project.remove(project)
    print("old_project: ", old_project, "new_project: ", new_project)
    assert sorted(old_project, key=Project.id_or_max) == sorted(new_project, key=Project.id_or_max)