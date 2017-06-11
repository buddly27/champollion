# :coding: utf-8

from sphinx.directives import Directive
import docutils.parsers.rst.directives
import docutils.nodes

import rst_generator


class AutoModuleDirective(Directive):
    """Directive to render :term:`Javascript` module documentation.

    The unique argument should be the identifier of the module element.

    .. sourcecode:: rest

        .. js:automodule:: module.test

    The available options are:

    * undoc-members:
        Indicate whether members with no docstrings should be displayed.

    * private-members:
        Indicate whether private members (with a name starting with an
        underscore) should be displayed.

    * module-alias:
        String element to replace the module name.

    * force-partial-import:
        Indicate whether each import statement display within the module
        should be indicated with partial import.

    .. seealso::

        :ref:`directive/automodule`

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
        "undoc-members": lambda x: True,
        "private-members": lambda x: True,
        "module-alias": docutils.parsers.rst.directives.unchanged_required,
        "force-partial-import": lambda x: True,
    }

    def run(self):
        """Run the directive."""
        if not hasattr(self.state.document.settings.env, "js_environment"):
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
        module_name = self.options.get(
            "module-alias", module_environment["name"]
        )
        env = js_env["file"][file_id]

        # Options manually set
        undoc_members = self.options.get("undoc-members", False)
        private_members = self.options.get("private-members", False)

        rst_elements = {}

        # Gather classes
        rst_elements = rst_generator.get_rst_class_elements(
            env, module_name,
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements
        )

        # Gather functions
        rst_elements = rst_generator.get_rst_function_elements(
            env, module_name,
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements,
        )

        # Gather variables
        rst_elements = rst_generator.get_rst_data_elements(
            env, module_name,
            blacklist_ids=env["function"].keys(),
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements,
        )

        # Gather exported elements
        rst_elements = rst_generator.get_rst_export_elements(
            env, js_env, module_name,
            rst_elements=rst_elements
        )

        # Add content while respecting the line order
        for line_number in sorted(rst_elements.keys()):
            for rst_element in rst_elements[line_number]:
                node = docutils.nodes.paragraph()
                self.state.nested_parse(rst_element, 0, node)

                nodes.append(node)

        return nodes
