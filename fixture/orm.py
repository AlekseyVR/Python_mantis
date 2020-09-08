from pony.orm import *
from datetime import datetime
from models.group import Group
from models.contact import Contact
# from pymysql.converters import decoders
# ValueError: Value of unexpected type received from database: instead of datetime got <class 'str'>


class ORMFixture:
    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column="group_id")
        name_group = Optional(str, column="group_name")
        logo_group = Optional(str, column="group_header")
        footer_group = Optional(str, column="group_footer")
        contacts = Set(lambda: ORMFixture.ORMContact, table="address_in_groups", column="id", reverse="groups", lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        first_name_contact = Optional(str, column="firstname")
        last_name_contact = Optional(str, column="lastname")
        contact_address = Optional(str, column="address")
        home_contact = Optional(str, column='home')
        mobile_contact = Optional(str, column='mobile')
        work_contact = Optional(str, column='work')
        secondary_home = Optional(str, column='phone2')
        e_mail_contact = Optional(str, column='email')
        e_mail_2_contact = Optional(str, column='email2')
        e_mail_3_contact = Optional(str, column='email3')
        deprecated = Optional(datetime, column="deprecated")
        groups = Set(lambda: ORMFixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name_group=group.name_group, logo_group=group.logo_group, footer_group=group.footer_group)
        return list(map(convert, groups))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), first_name_contact=contact.first_name_contact, last_name_contact=contact.last_name_contact)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))
        # return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_groups_containing_contact(self, contact):
        orm_contact = list(select(c for c in ORMFixture.ORMContact if c.id == contact.id))[0]
        return self.convert_groups_to_model(orm_contact.groups)

    @db_session
    def get_groups_not_containing_contact(self, contact):
        orm_contact = list(select(c for c in ORMFixture.ORMContact if c.id == contact.id))[0]
        return self.convert_groups_to_model(
            select(g for g in ORMFixture.ORMGroup if orm_contact not in g.contacts))