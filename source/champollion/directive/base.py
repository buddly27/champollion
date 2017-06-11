# :coding: utf-8

from sphinx.domains.javascript import JSObject

import rst_generator


class BaseDirective(JSObject):
    """Base class for :term:`Javascript` object directive.
    """

    #: Only the object id argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: Nested element is automatically generated and can not be manually entered
    allow_nesting = False

    #: No prefix is displayed right before the documentation entry
    display_prefix = None

    def run(self):
        """Run the directive."""
        if not hasattr(self.state.document.settings.env, "js_environment"):
            raise self.error(
                "The javascript environment has not been parsed properly"
            )

        # The signature is always the first argument.
        signature = self.arguments[0]

        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env[self.objtype].keys():
            raise self.error(
                "The {objtype} id is unavailable: {signature}".format(
                    objtype=self.objtype,
                    signature=signature
                )
            )

        self.state.document.settings.env.element_environment = (
            js_env[self.objtype][signature]
        )
        self.state.document.settings.env.module_environment = (
            js_env["module"]
        )

        return super(BaseDirective, self).run()

    def generate_import_statement(
        self, environment, module_environment, force_partial_import=False
    ):
        """Return import statement generated from *environment* and
        *module_environment*.

        The import statement will be generated only if the element is exported
        and the usage of partial import will depend whether the element is
        exported as default.

        *force_partial_import* indicate whether the usage of partial import
        should be used even if the element is exported as default.

        .. warning::

            The statement is using :term:`Javascript` ES6
            `import
            <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import>`_
            keyword

        Example:

        .. code-block:: js

            import element from "module"
            import {partialElement} from "module"

        """
        name = self.options.get("alias", environment["name"])
        module_id = environment["module_id"]
        module_name = self.options.get(
            "module-alias", module_environment[module_id]["name"]
        )
        exported = environment["exported"]
        is_default = environment["default"]

        if exported and is_default and not force_partial_import:
            return rst_generator.rst_string(
                "``import {name} from \"{module}\"``\n".format(
                    name=name, module=module_name
                )
            )

        if exported and (not is_default or force_partial_import):
            return rst_generator.rst_string(
                "``import {{{name}}} from \"{module}\"``\n".format(
                    name=name, module=module_name
                )
            )

        return rst_generator.rst_string()

    def generate_description(self, environment):
        """Return description generated from *environment*.
        """
        description = environment["description"]

        content = rst_generator.rst_string()
        if description:
            content += rst_generator.rst_string(description)

        return content
