# :coding: utf-8

from sphinx.domains.javascript import JSObject
from docutils.statemachine import StringList


class BaseDirective(JSObject):
    """Directive mixin to regroup common helper methods
    """
    #: Only the object id argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: Nested element is automatically generated and can not be manually entered
    allow_nesting = True

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    def __init__(
        self, name, arguments, options, content, lineno, content_offset,
        block_text, state, state_machine
    ):
        """Initiate the base directive.

        Raise an error if the variable id is unavailable within the Javascript
        environment parsed.

        """
        super(BaseDirective, self).__init__(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )
        # The signature is always the first argument.
        signature = arguments[0]

        self._env = {}
        self._module_env = {}

        # Initiate Javascript environment and raise an error if the
        # element is unavailable.
        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env[self.objtype].keys():
            raise self.error(
                "The {objtype} id is unavailable: {signature}".format(
                    objtype=self.objtype,
                    signature=signature
                )
            )

        else:
            self._env = js_env[self.objtype][signature]
            self._module_env = js_env["module"]

    def _generate_import_statement(self):
        """Return the `StringList` import statement.
        """
        name = self._env["name"]
        module_id = self._env["module_id"]
        module_name = self._module_env[module_id]["name"]
        exported = self._env["exported"]
        is_default = self._env["default"]

        if exported and is_default:
            return StringList([
                "``import {name} from \"{module}\"``".format(
                    name=name, module=module_name
                ),
                ""
            ])

        if exported and not is_default:
            return StringList([
                "``import {{{name}}} from \"{module}\"``".format(
                    name=name, module=module_name
                ),
                ""
            ])

        return StringList()

    def _generate_description(self):
        """Return the `StringList` description.
        """
        description = self._env["description"]

        content = StringList()
        if description:
            content += StringList(description.split("\n"))

        return content
