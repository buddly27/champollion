# :coding: utf-8

from sphinx import addnodes
from sphinx.domains.javascript import JSObject, JSCallable
from docutils.statemachine import StringList


class AutoDataDirective(JSObject):
    """Generate reStructuredText from JavaScript function.

    .. sourcecode:: rest

        .. js:autodata:: my-data-id

    """
    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        super(AutoDataDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        signature = arguments[0]

        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["variables"].keys():
            raise RuntimeError("Unexisting variable: {}".format(signature))

        self.variable_env = js_env["variables"][signature]
        self.module_env = js_env["modules"]

        if self.variable_env["description"]:
            self.content = StringList(
                self.variable_env["description"].split("\n")
            )

    def handle_signature(self, sig, signode):
        name = self.variable_env["name"]
        module_id = self.variable_env["module_id"]
        variable_type = self.variable_env["type"]
        module_name = self.module_env[module_id]["name"]

        signode["type"] = "variables"
        signode["id"] = self.variable_env["id"]
        signode["module"] = module_name
        signode['fullname'] = name

        signode += addnodes.desc_type(variable_type + " ", variable_type + " ")
        signode += addnodes.desc_addname(module_name + ".", module_name + ".")
        signode += addnodes.desc_name(name, name)
        return name, module_name

    def get_index_text(self, objectname, name_obj):
        self.objtype = "data"
        return super(AutoDataDirective, self).get_index_text(
            objectname, name_obj
        )
