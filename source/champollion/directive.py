# :coding: utf-8

from sphinx import addnodes
from sphinx.domains.javascript import JSObject, JSCallable

from helper import generate_content


class AutoDataDirective(JSObject):
    """Generate reStructuredText from JavaScript data.

    .. sourcecode:: rest

        .. js:autodata:: my-data-id

    """
    #: Only one ``data id`` argument is required
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
        # element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["data"].keys():
            raise self.error(
                "The data id is unavailable: {0}".format(signature)
            )

        else:
            self.data_env = js_env["data"][signature]
            self.module_env = js_env["module"]

            module_id = self.data_env["module_id"]

            self.content = generate_content(
                self.data_env["name"],
                self.module_env[module_id]["name"],
                description=self.data_env["description"],
                exported=self.data_env["exported"],
                is_default=self.data_env["default"]
            )

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        for element in ["id", "name", "module_id", "type"]:
            if element not in self.data_env.keys():
                return signature, ""

        name = self.data_env["name"]
        value = self.data_env["value"]
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
        node += addnodes.desc_annotation(" = " + value, " = " + value)
        return name, module_name

    def get_index_text(self, objectname, name_obj):
        """Return relevant index text.
        """
        return " (global variable or constant)"


class AutoFunctionDirective(JSCallable):
    """Generate reStructuredText from JavaScript function.

    .. sourcecode:: rest

        .. js:autofunction:: my-function-id

    """
    #: Only one ``function id`` argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: No nesting available
    allow_nesting = False

    #: Javascript function is callable
    has_arguments = True

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    #: Define the Object type
    objtype = "function"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoFunctionDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )

        # The signature is always the first argument.
        signature = arguments[0]

        self.function_env = {}
        self.module_env = {}

        # Initiate Javascript environment and raise an error if the
        # element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["function"].keys():
            raise self.error(
                "The function id is unavailable: {0}".format(signature)
            )

        else:
            self.function_env = js_env["function"][signature]
            self.module_env = js_env["module"]

            module_id = self.function_env["module_id"]

            self.content = generate_content(
                self.function_env["name"],
                self.module_env[module_id]["name"],
                description=self.function_env["description"],
                exported=self.function_env["exported"],
                is_default=self.function_env["default"]
            )

    def handle_signature(self, signature, node):
        """Update the signature node.
        """
        for element in ["id", "name", "arguments", "module_id"]:
            if element not in self.function_env.keys():
                return signature, ""

        name = self.function_env["name"]
        module_id = self.function_env["module_id"]
        module_name = self.module_env[module_id]["name"]

        node["type"] = "function"
        node["id"] = self.function_env["id"]
        node["module"] = module_name
        node['fullname'] = name

        node += addnodes.desc_addname(module_name + ".", module_name + ".")
        node += addnodes.desc_name(name, name)

        param_list = addnodes.desc_parameterlist()
        for argument in self.function_env["arguments"]:
            param_list += addnodes.desc_parameter(argument, argument)
        node += param_list

        return name, module_name


class AutoClassDirective(JSCallable):
    """Generate reStructuredText from JavaScript class.

    .. sourcecode:: rest

        .. js:autoclass:: my-class-id

    """
    #: Only one ``class id`` argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: Nesting available
    allow_nesting = True

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    #: Define the Object type
    objtype = "class"

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(AutoClassDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )

        # The signature is always the first argument.
        signature = arguments[0]

        self.class_env = {}
        self.module_env = {}

        # Initiate Javascript environment and raise an error if the
        # element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["class"].keys():
            raise self.error(
                "The class id is unavailable: {0}".format(signature)
            )

        else:
            self.class_env = js_env["class"][signature]
            self.module_env = js_env["module"]

            module_id = self.class_env["module_id"]

            self.content = generate_content(
                self.class_env["name"],
                self.module_env[module_id]["name"],
                description=self.class_env["description"],
                exported=self.class_env["exported"],
                is_default=self.class_env["default"]
            )
