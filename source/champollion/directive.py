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

        self.data_env = {}
        self.module_env = {}

        # Initiate Javascript environment and raise an error if the
        # variable element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["data"].keys():
            raise self.error("The global data is unavailable: {0}".format(
                signature
            ))

        else:
            self.data_env = js_env["data"][signature]
            self.module_env = js_env["module"]

            self.content = StringList()

            if self.data_env["exported"]:
                self.content += self.get_import_statement(
                    self.data_env["default"]
                )

            # Initiate content if description is available.
            if self.data_env["description"]:
                self.content += StringList(
                    self.data_env["description"].split("\n")
                )

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        for element in ["id", "name", "module_id", "type"]:
            if element not in self.data_env.keys():
                return signature, ""

        name = self.data_env["name"]
        module_id = self.data_env["module_id"]
        variable_type = self.data_env["type"]
        module_name = self.module_env[module_id]["name"]

        node["type"] = "data"
        node["id"] = self.data_env["id"]
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

    def get_import_statement(self, is_default):
        """Return import statement as a `StringList`.
        """
        module_id = self.data_env["module_id"]
        module_name = self.module_env[module_id]["name"]

        if is_default:
            return StringList(
                [
                    "``import {name} from '{module}'``".format(
                        name=self.data_env["name"],
                        module=module_name
                    ),
                    ""
                ]
            )

        else:
            return StringList(
                [
                    "``import {{{name}}} from '{module}'``".format(
                        name=self.data_env["name"],
                        module=module_name
                    ),
                    ""
                ]
            )
