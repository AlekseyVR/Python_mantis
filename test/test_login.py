def test_login(app):
    app.session.login("administrator", "root")
    # assert app.session.is_logged_in_as("administrator")
    assert app.soap.can_login("administrator", "root")
    prjct_lists = []
    get_prjct =  app.soap.get_project_list_user("administrator", "root")
    prjct_lists.append(get_prjct)
    print("\nnew_project: ", prjct_lists)
