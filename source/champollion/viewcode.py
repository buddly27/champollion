# :coding: utf-8

from sphinx import addnodes
from docutils import nodes
from sphinx.util.nodes import make_refnode


def add_source_code_links(app, doctree):
    """Parse *doctree* and add source code link when available.

    Create temporary 'js_modules' in *app* builder environment to store all
    module information which will be used to create the code page links.

    This function is called with the ``doctree-read`` Sphinx event, emitted
    when a *doctree* has been parsed and read by the  environment, and is
    about to be pickled

    """
    js_env = app.env.js_environment
    builder_env = app.builder.env

    # Store the module information to ease the source pages creation
    if not hasattr(builder_env, "js_modules"):
        builder_env.js_modules = {}

    # Loop through all js signature nodes
    for object_node in doctree.traverse(addnodes.desc):
        if object_node.get("domain") != "js":
            continue

        for node in object_node:
            if not isinstance(node, addnodes.desc_signature):
                continue

            node_type = node.get("type", None)
            if node_type not in js_env.keys():
                continue

            node_id = node.get("id", None)
            if node_id not in js_env[node_type].keys():
                continue

            js_env_element = js_env[node_type][node_id]
            for element in ["name", "module_id", "line_number"]:
                if element not in js_env_element.keys():
                    continue

            module_id = js_env_element["module_id"]
            page_name = "_modules/{0}".format(module_id.replace(".", "/"))

            if module_id not in builder_env.js_modules.keys():
                builder_env.js_modules[module_id] = {
                    "pagename": page_name,
                    "docname": builder_env.docname,
                    "entries": {}
                }

            line_number = js_env_element["line_number"]
            builder_env.js_modules[module_id]["entries"][line_number] = (
                js_env_element["name"]
            )

            link_node = addnodes.only(expr="html")
            link_node += addnodes.pending_xref(
                "",
                reftype="viewcode",
                refdomain="std",
                refexplicit=False,
                reftarget=page_name,
                refid=node.get("fullname"),
                refdoc=builder_env.docname
            )
            link_node[0] += nodes.inline(
                "", "[source]", classes=["viewcode-link"]
            )
            node += link_node


def create_code_pages(app):
    """Create all code pages and the links to the documentation.

    This function is called with the ``html-collect-pages`` Sphinx event,
    emitted when the HTML builder is starting to write non-document pages.

    """
    builder_env = app.builder.env
    if not hasattr(builder_env, "js_modules"):
        return

    module_env = app.env.js_environment["module"]
    file_env = app.env.js_environment["file"]

    highlighter = app.builder.highlighter
    uri = app.builder.get_relative_uri

    all_pages = [elt["pagename"] for elt in builder_env.js_modules.values()]

    for module_id, element in builder_env.js_modules.items():
        file_id = module_env[module_id]["file_id"]
        page_name = element["pagename"]
        doc_name = element["docname"]

        if builder_env.config.highlight_language in ("js", "default", "none"):
            lexer = builder_env.config.highlight_language
        else:
            lexer = "js"

        highlighted = highlighter.highlight_block(
            file_env[file_id]["content"], lexer, linenos=False
        )
        lines = highlighted.splitlines()

        for line_number, name in element["entries"].items():
            link = uri(page_name, doc_name) + "#" + name
            lines[line_number-1] = (
                "<div class='viewcode-block' id='{name}'>"
                "<a class='viewcode-back' href='{link}'>[docs]</a>"
                "{line}".format(
                    name=name,
                    link=link,
                    line=lines[line_number-1]
                )
            )

        parents = []

        for module_name in reversed(module_id.split(".")[:-1]):
            link_page = "_modules/{0}".format(module_name.replace(".", "/"))
            if link_page in all_pages:
                parents.append({
                    "link": uri(page_name, link_page),
                    "title": module_name
                })

        parents.append({
            "link": uri(page_name, "_modules/index"),
            "title": "Code"
        })
        parents.reverse()

        # putting it all together
        context = {
            "parents": parents,
            "title": module_id,
            "body": (
                "<h1>Source code for {name}</h1>{content}".format(
                    name=module_id,
                    content="\n".join(lines)
                )
            ),
        }
        yield page_name, context, "page.html"

    yield create_code_page_index(app)


def create_code_page_index(app):
    """Create page index regrouping all code page links.
    """
    builder_env = app.builder.env
    if not hasattr(builder_env, "js_modules"):
        return

    body = ["\n<ul>"]

    for module_id in sorted(builder_env.js_modules.keys()):
        link_page = "_modules/{0}".format(module_id.replace(".", "/"))
        uri = app.builder.get_relative_uri

        body.append(
            "<li><a href='{link}'>{name}</a></li>\n".format(
                link=uri("_modules/index", link_page),
                name=module_id
            )
        )

    body.append("</ul>")

    context = {
        "title": "Overview: module code",
        "body": (
            "<h1>All modules for which code is available</h1>{0}".format(
                "".join(body)
            )
        ),
    }

    return "_modules/index", context, "page.html"


def create_missing_code_link(app, env, node, content_node):
    """Resolve all '[source]' links in Api documentation pages.

    This function is called with the ``missing-reference`` Sphinx event,
    emitted when a cross-reference to a Python module or object cannot be
    resolved.

    """
    if node["reftype"] == "viewcode":
        return make_refnode(
            app.builder,
            node["refdoc"],
            node["reftarget"],
            node["refid"],
            content_node
        )
