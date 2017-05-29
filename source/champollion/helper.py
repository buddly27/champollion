# :coding: utf-8

from docutils.statemachine import StringList


def generate_content(
    name, module_name, description=None, exported=False, is_default=False
):
    """Return content as a `StringList` object.
    """
    content = StringList()

    if exported and is_default:
        content += StringList([
            "``import {name} from '{module}'``".format(
                name=name, module=module_name
            ),
            ""
        ])

    if exported and not is_default:
        content += StringList([
            "``import {{{name}}} from '{module}'``".format(
                name=name, module=module_name
            ),
            ""
        ])

    # Initiate content if description is available.
    if description:
        content += StringList(description.split("\n"))

    return content
