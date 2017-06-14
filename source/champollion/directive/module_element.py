# :coding: utf-8

from sphinx.directives import Directive
from sphinx import addnodes
import docutils.parsers.rst.directives
import docutils.nodes

# import rst_generator
from .rst_generator import (
    get_rst_class_elements,
    get_rst_function_elements,
    get_rst_data_elements,
    get_rst_export_elements
)


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
        # The signature is always the first argument.
        signature = self.arguments[0]

        js_env = self.state.document.settings.env.app.config.js_environment
        if signature not in js_env["module"].keys():
            raise self.error(
                "The module id is unavailable: {signature}".format(
                    signature=signature
                )
            )

        env = self.state.document.settings.env
        module_environment = js_env["module"][signature]

        # Update references
        ref_context = self.state.document.settings.env.ref_context
        ref_context["js:module"] = module_environment["id"]
        ref_context["js:object"] = "module"

        nodes = []

        # Add target to reference this module
        module_id = module_environment["id"]
        env.domaindata["js"]["modules"][module_id] = env.docname
        env.domaindata['js']["objects"][module_id] = (env.docname, "module")
        target_node = docutils.nodes.target(
            "", "", ids=["module-" + module_id], ismod=True
        )

        self.state.document.note_explicit_target(target_node)
        nodes.append(target_node)
        index_text = "{0} (module)".format(module_id)
        index_node = addnodes.index(
            entries=[("single", index_text, "module-" + module_id, "", None)]
        )
        nodes.append(index_node)

        file_id = module_environment["file_id"]
        module_name = self.options.get(
            "module-alias", module_environment["name"]
        )
        file_environment = js_env["file"][file_id]

        # Options manually set
        undoc_members = self.options.get("undoc-members", False)
        private_members = self.options.get("private-members", False)

        rst_elements = {}

        # Gather classes
        rst_elements = get_rst_class_elements(
            file_environment, module_name,
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements
        )

        # Gather functions
        rst_elements = get_rst_function_elements(
            file_environment, module_name,
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements,
        )

        # Gather variables
        rst_elements = get_rst_data_elements(
            file_environment, module_name,
            blacklist_ids=file_environment["function"].keys(),
            undocumented_members=undoc_members,
            private_members=private_members,
            force_partial_import=self.options.get(
                "force-partial-import", False
            ),
            rst_elements=rst_elements,
        )

        # Gather exported elements
        rst_elements = get_rst_export_elements(
            file_environment, js_env, module_name,
            rst_elements=rst_elements
        )

        # Add content while respecting the line order
        for line_number in sorted(rst_elements.keys()):
            for rst_element in rst_elements[line_number]:
                node = docutils.nodes.paragraph()
                self.state.nested_parse(rst_element, 0, node)

                nodes.append(node)

        return nodes
