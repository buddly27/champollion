# :coding: utf-8

from sphinx.directives import Directive

from docutils.statemachine import StringList
import docutils.nodes


def _parse_members(argument):
    """Convert the :members: options to class directive."""
    if argument is None:
        return True
    return [arg.strip() for arg in argument.split(",")]


class AutoModuleDirective(Directive):
    """Generate reStructuredText from JavaScript module.

    .. sourcecode:: rest

        .. js:automodule:: my-module-id

    """
    #: Only the object id argument is required
    required_arguments = 1

    #: No optional argument is available
    optional_arguments = 0

    #: Content is automatically generated and can not be manually entered
    has_content = False

    #: Nested element is automatically generated and can not be manually entered
    allow_nesting = False

    #: module options
    option_spec = {
        "members": _parse_members,
        "undoc-members": lambda x: True,
        "private-members": lambda x: True,
    }

    def run(self):
        """Run the directive."""
        if not hasattr(
            self.state.document.settings.env, "js_environment"
        ):
            raise self.error(
                "The javascript environment has not been parsed properly"
            )

        # The signature is always the first argument.
        signature = self.arguments[0]

        js_env = self.state.document.settings.env.js_environment
        if signature not in js_env["module"].keys():
            raise self.error(
                "The module id is unavailable: {signature}".format(
                    signature=signature
                )
            )

        nodes = []

        module_environment = js_env["module"][signature]
        file_id = module_environment["file_id"]

        env = js_env["file"][file_id]

        # Options manually set
        undoc_members = self.options.get("undoc-members", False)
        private_members = self.options.get("private-members", False)

        members = self.options.get("members", True)
        if members:
            nested_elements = {}

            # Gather classes
            for class_environment in env["class"].values():
                name = class_environment["name"]
                description = class_environment["description"]
                if description is None and not undoc_members:
                    continue

                if name.startswith("_") and not private_members:
                    continue

                if members is True or name in members:
                    line_number = class_environment["line_number"]
                    nested_elements[line_number] = (
                        "autoclass", class_environment["id"]
                    )

            # Gather functions
            for function_environment in env["function"].values():
                name = function_environment["name"]
                description = function_environment["description"]
                if description is None and not undoc_members:
                    continue

                if name.startswith("_") and not private_members:
                    continue

                if members is True or name in members:
                    line_number = function_environment["line_number"]
                    nested_elements[line_number] = (
                        "autofunction", function_environment["id"]
                    )

            # Gather variables
            for data_environment in env["data"].values():
                # As a function can also be a variable, use the function
                # directive by default when available
                if data_environment["id"] in env["function"].keys():
                    continue

                name = data_environment["name"]
                description = data_environment["description"]
                if description is None and not undoc_members:
                    continue

                if name.startswith("_") and not private_members:
                    continue

                if members is True or name in members:
                    line_number = data_environment["line_number"]
                    nested_elements[line_number] = (
                        "autodata", data_environment["id"]
                    )

            # Add content while respecting the line order
            for line_number in sorted(nested_elements.keys()):
                directive, element_id = nested_elements[line_number]
                element_rst = (
                    "\n.. js:{directive}:: {id}\n\n".format(
                        directive=directive, id=element_id
                    )
                )
                content = StringList(element_rst.split("\n"))
                node = docutils.nodes.paragraph()
                self.state.nested_parse(content, 0, node)

                nodes.append(node)

        return nodes
