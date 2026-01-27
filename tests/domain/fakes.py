from datetime import date


class FakeDescription:
    def __init__(self, lang, name=None, about=None, full_desc=None):
        self.lang = lang
        self.name = name
        self.about = about
        self.full_desc = full_desc


class FakeProject:
    def __init__(self, deploy_date=None, stacks=None, descriptions=None):
        self.deploy_date = deploy_date
        self.stacks = stacks or []
        self.descriptions = descriptions or []
