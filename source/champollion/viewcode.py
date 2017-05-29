# :coding: utf-8

from sphinx import addnodes
from docutils import nodes
from sphinx.util.nodes import make_refnode


def add_source_code_links(app, doctree):
    """Parse *doctree* and add source code link when available.

    Create temporary '_js_modules' to store all module information
    which will be used to create the code page links.

    """
    js_env = app.env.js_environment
    builder_env = app.builder.env

    # Store the module information to ease the source pages creation
    if not hasattr(builder_env, "_js_modules"):
        builder_env._js_modules = {}

    # Loop through all js signature nodes
    for objnode in doctree.traverse(addnodes.desc):
        if objnode.get("domain") != "js":
            continue

        for signode in objnode:
            if not isinstance(signode, addnodes.desc_signature):
                continue

            js_env_element = js_env[signode.get("type")][signode.get("id")]
            module_id = js_env_element["module_id"]
            pagename = "_modules/{0}".format(module_id.replace(".", "/"))

            if module_id not in builder_env._js_modules.keys():
                builder_env._js_modules[module_id] = dict(
                    pagename=pagename,
                    docname=builder_env.docname,
                    entries=dict()
                )

            lineno = js_env_element["line_number"]
            builder_env._js_modules[module_id]["entries"][lineno] = (
                js_env_element["name"]
            )

            onlynode = addnodes.only(expr="html")
            onlynode += addnodes.pending_xref(
                "",
                reftype="viewcode",
                refdomain="std",
                refexplicit=False,
                reftarget=pagename,
                refid=signode.get("fullname"),
                refdoc=builder_env.docname
            )
            onlynode[0] += nodes.inline(
                "", "[source]",
                classes=["viewcode-link"]
            )
            signode += onlynode


def create_code_pages(app):
    """Create all code pages and the links to the documentation.
    """
    builder_env = app.builder.env
    if not hasattr(builder_env, "_js_modules"):
        return

    module_env = app.env.js_environment["module"]
    file_env = app.env.js_environment["file"]

    highlighter = app.builder.highlighter
    urito = app.builder.get_relative_uri

    for module_id, element in builder_env._js_modules.items():
        file_id = module_env[module_id]["file_id"]
        pagename = element["pagename"]
        docname = element["docname"]

        highlighted = highlighter.highlight_block(
            file_env[file_id]["content"], "js", linenos=False
        )
        lines = highlighted.splitlines()

        for lineno, name in element["entries"].items():
            link = urito(pagename, docname) + "#" + name
            lines[lineno-1] = (
                "<div class='viewcode-block' id='{name}'>"
                "<a class='viewcode-back' href='{link}'>[docs]</a>"
                "{line}".format(
                    name=name,
                    link=link,
                    line=lines[lineno-1]
                )
            )

        parents = []

        for module_name in module_id.split(".")[:-1]:
            parents.append({
                "link": urito(
                    pagename, "_modules/" + module_name.replace(".", "/")
                ),
                "title": module_name
            })

        parents.append({
            "link": urito(pagename, "_modules/index"),
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
        yield pagename, context, "page.html"

    yield create_code_page_index(app, urito)


def create_code_page_index(app, urito):
    """Create index code pages.
    """
    builder_env = app.builder.env
    if not hasattr(builder_env, "_js_modules"):
        return

    body = ["\n"]

    stack = [""]

    for module_id in sorted(builder_env._js_modules.keys()):
        if module_id.startswith(stack[-1]):
            stack.append(module_id + ".")
            body.append("<ul>")
        else:
            stack.pop()
            while not module_id.startswith(stack[-1]):
                stack.pop()
                body.append("</ul>")
            stack.append(module_id + ".")
        body.append(
            "<li><a href='{link}'>{name}</a></li>\n".format(
                link=urito(
                    "_modules/index", "_modules/" + module_id.replace(".", "/")
                ),
                name=module_id
            )
        )

    body.append("</ul>" * (len(stack) - 1))

    context = {
        "title": "Overview: module code",
        "body": (
            "<h1>All modules for which code is available</h1>{0}".format(
                "".join(body)
            )
        ),
    }

    return "_modules/index", context, "page.html"


def create_missing_code_link(app, env, node, contnode):
    """Create code link if missing.
    """
    if node["reftype"] == 'viewcode':
        return make_refnode(
            app.builder,
            node['refdoc'],
            node['reftarget'],
            node['refid'],
            contnode
        )
