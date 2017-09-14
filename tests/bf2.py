import os
import re
import sys


class Mod(object):

    def __init__(self):
        self.root = self.find_mod_root()

    def find_mod_root(self):
        workdir_parts = os.getcwd().split(os.sep)
        return os.sep.join(
            workdir_parts[:workdir_parts.index('mods') + 2])

    def get_object_path(self, name):
        for dirname, dirnames, filenames in os.walk(
                os.path.join(self.root, 'objects')):
            for filename in filenames:
                if filename.split('.')[-1] in ['con', 'tweak']:
                    filepath = os.path.join(
                        self.root, 'objects', dirname, filename)
                    root = TemplateParser(filepath).get_root()
                    if root is not None and root[1] == name:
                        return filepath



# ############################################### #
# !!!untested shit leftover from materials parser #
class TemplateParser:
    # regex from mats
    # ObjectTeamplate.(create|activeSafe) <?Type\S*> <?Object\S*>

    def __init__(self, filepath):
        self.path_object_folder = self.get_root_folder(filepath)
        self.path_object_template = filepath
        self.object_types_list = [
            'PlayerControlObject',
            'Wing',
            'Wheel',
            'Spring',
            'RotationalBundle',
            'Engine'
            'SimpleObject'
        ]

    def get_root_folder(self, filepath):
        path, filename = os.path.split(filepath)
        return path

    def get_root(self):
        object_types_string = '|'.join(self.object_types_list)
        pattern1 = r'ObjectTemplate.create (' + object_types_string + ') (\w)+'
        with open(self.path_object_template) as confile:
            for line in confile:
                match = re.search(pattern1, line)
                if match:
                    # first match is our object
                    type = match.group().split(' ')[1]
                    name = match.group().split(' ')[2]
                    return (type, name)

    def get_child_list(self):
        child_list = []
        object_types_string = '|'.join(self.object_types_list)
        pattern1 = r'ObjectTemplate.create (' + object_types_string + ') (\w)+'
        pattern2 = r'include (\w)+.tweak'
        with open(self.path_object_template) as confile:
            for line in confile:
                match = re.search(pattern1, line)
                if match:
                    child_list.append(match.group())
                match = re.search(pattern2, line)
                if match:
                    with open(os.path.join(self.path_object_folder, match.group().split(' ')[1])) as tweakfile:
                        for line in tweakfile:
                            match = re.search(pattern1, line)
                            if match:
                                child_list.append(match.group())
        return child_list

    def get_wings(self):
        wings = []
        pattern1 = r'ObjectTemplate.(create|activeSafe) Wing (\w)+'
        pattern2 = r'include (\w)+.tweak'
        pattern3 = r'(ObjectTemplate.(create|activeSafe) Wing (\w)+)|(ObjectTemplate.setWingLift ([-+]?\d*\.\d+|\d+))|(ObjectTemplate.setFlapLift ([-+]?\d*\.\d+|\d+))'
        with open(self.path_object_template) as confile:
            for line in confile:
                match = re.search(pattern2, line)
                if match:
                    with open(os.path.join(self.path_object_folder, match.group().split(' ')[1])) as tweakfile:
                        '''
                        for id, line in enumerate(tweakfile.readlines()):
                            match = re.search(pattern1, line)
                            if match:
                                wing_name = match.group().split(' ')[2]
                                wing = Wing(wing_name)
                                #wing.lift_wing =
                        '''
                        # whole file test
                        for line in tweakfile.readlines():
                            match = re.search(pattern3, line)
                            if match:
                                print(match.group())


class Materials:
    # MaterialManager.createCell 1 18
    # MaterialManager.damageMod 1

    class Material:

        def __init__(self, id):
            self.id = id
            self.name = None
            self.damage_mod = {}

        def __eq__(self, other):
            return self.id == other.id

        def __hash__(self):
            return hash('id', self.id)

    def __init__(self, filepath):
        self.cells = self.parse_settings(filepath)

    def parse_settings(self, filepath):
        cells = {}
        with open(filepath) as fo:
            matches = re.finditer(
                r'MaterialManager.createCell (\d+) (\d+)\nMaterialManager.damageMod ((\d+\.\d+)|(\d+))',
                fo.read())
            for match in matches:
                #pattern_cell = r'MaterialManager.createCell (\d+) (\d+)'
                #match_cell = re.match(pattern_cell, match.group())
                mat_id_attacker, mat_id_target = int(
                    match.group(1)), int(match.group(2))
                attacker = self.Material(mat_id_attacker)
                if attacker.id not in cells:
                    cells[attacker.id] = attacker
                if mat_id_target not in cells[attacker.id].damage_mod:
                    cells[attacker.id].damage_mod[
                        mat_id_target] = float(match.group(3))
        return cells


class GameObject:

    def __init__(self, name):
        self.name = name
        self.type = None
        self.childs = []
        self.childs_created = []
        self.mapped_materials = {}

    def loadFromCon(self, path_confile):
        parser = TemplateParser(path_confile)
        self.type, self.name = parser.get_root()
        self.childs_created = parser.get_child_list()
        # print(self.childs_created)


class Jet:

    def __init__(self):
        self.name = None
        self.type = None
        self.wings = []

    def loadFromCon(self, path_confile):
        parser = TemplateParser(path_confile)
        self.type, self.name = parser.get_root()
        self.wings = parser.get_wings()


class Wing():

    def __init__(self, name):
        self.name = name
        self.lift_wing = 0
        self.lift_flap = 0
