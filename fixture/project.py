# -*- coding: utf-8 -*-
from model.project import Project
from selenium.webdriver.support.ui import Select


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def add_project(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def open_project_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

    def add_name_project(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def add_option_value(self, field_name, option):
        wd = self.app.wd
        if option is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(option)

    def fill_project(self, project):
        self.add_name_project("name", project.name_project)
        self.add_option_value("status", project.status_project)
        self.add_option_value("view_state", project.view_status_project)
        self.add_name_project("description", project.description_project)

    def get_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        project_table_2 = wd.find_elements_by_tag_name("table")[2]
        table_rows = project_table_2.find_elements_by_tag_name("tr")[2:]
        project_list = []
        for row in table_rows:
            element = row.find_elements_by_tag_name("td")
            id = element[0].find_element_by_tag_name("a").get_attribute("href").replace(
                "http://localhost/mantisbt-1.2.20/manage_proj_edit_page.php?project_id=", "")
            name_project = element[0].find_element_by_tag_name("a").text
            status_project = element[1].text
            view_status_project = element[3].text
            description_project = element[4].text
            project_list.append(Project(id=id, name_project=name_project, description_project=description_project))
        return project_list

    def delete_project(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("a[href='manage_proj_edit_page.php?project_id=%s" % project.id).click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
