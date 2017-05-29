# :coding: utf-8

from sphinx import addnodes
from sphinx.domains.javascript import JSObject, JSCallable
from docutils.statemachine import StringList


class AutoDataDirective(JSObject):
    """Generate reStructuredText from JavaScript global data.

    .. sourcecode:: rest

        .. js:autodata:: my-data-id

    """
    #: Only one ``variable id`` argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: No nesting available
    allow_nesting = False

    #: Javascript data are not callable
    has_arguments = False

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    #: Define the Object type
    objtype = "data"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoDataDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )

        # The signature is always the first argument.
        signature = arguments[0]

        # Initiate Javascript environment and raise an error if the
        # variable element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["data"].keys():
            raise RuntimeError("Unexisting variable: {}".format(signature))

        self.variable_env = js_env["data"][signature]
        self.module_env = js_env["module"]

        # Initiate content if description is available.
        if self.variable_env["description"]:
            self.content = StringList(
                self.variable_env["description"].split("\n")
            )

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        name = self.variable_env["name"]
        module_id = self.variable_env["module_id"]
        variable_type = self.variable_env["type"]
        module_name = self.module_env[module_id]["name"]

        node["type"] = "data"
        node["id"] = self.variable_env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_type(variable_type + " ", variable_type + " ")
        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)
        return name, module_name

    def get_index_text(self, objectname, name_obj):
        """Return relevant index text.
        """
        return " (global variable or constant)"
