# :coding: utf-8


class RSTRenderer(object):

    @staticmethod
    def get_rst_class_elements(
        environment, module_name, members=True, undoc_members=False,
        private_members=False, rst_elements=None
    ):
        if rst_elements is None:
            rst_elements = {}

        for class_environment in environment["class"].values():
            name = class_environment["name"]
            description = class_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = class_environment["line_number"]
                rst_element = RSTRenderer.rst_generate(
                    directive="autoclass",
                    element_id=class_environment["id"],
                    alias=class_environment["name"],
                    module_alias=module_name

                )
                rst_elements[line_number] = [rst_element]

        return rst_elements

    @staticmethod
    def get_rst_attribute_elements(
        class_environment, members=True, undoc_members=False,
        private_members=False, blacklist=None, rst_elements=None,
    ):
        if rst_elements is None:
            rst_elements = {}

        # As a method can also be a variable, use the method directive
        # by default when available
        if blacklist is None:
            blacklist = []

        for attr_environment in class_environment["attribute"].values():
            if attr_environment["id"] in blacklist:
                continue

            name = attr_environment["name"]
            description = attr_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = attr_environment["line_number"]
                rst_element = RSTRenderer.rst_generate(
                    directive="autoattribute",
                    element_id=attr_environment["id"],

                )
                rst_elements[line_number] = [rst_element]

        return rst_elements

    @staticmethod
    def get_rst_method_elements(
        class_environment, members=True, skip_constructor=False,
        undoc_members=False, private_members=False, rst_elements=None
    ):
        if rst_elements is None:
            rst_elements = {}

        for method_environment in class_environment["method"].values():
            name = method_environment["name"]
            if name == "constructor" and skip_constructor:
                continue

            description = method_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = method_environment["line_number"]
                rst_element = RSTRenderer.rst_generate(
                    directive="automethod",
                    element_id=method_environment["id"],

                )
                rst_elements[line_number] = [rst_element]

        return rst_elements

    @staticmethod
    def get_rst_function_elements(
        environment, module_name, members=True, undoc_members=False,
        private_members=False, rst_elements=None
    ):
        if rst_elements is None:
            rst_elements = {}

        for function_environment in environment["function"].values():
            name = function_environment["name"]
            description = function_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = function_environment["line_number"]
                rst_element = RSTRenderer.rst_generate(
                    directive="autofunction",
                    element_id=function_environment["id"],
                    alias=function_environment["name"],
                    module_alias=module_name

                )
                rst_elements[line_number] = [rst_element]

        return rst_elements

    @staticmethod
    def get_rst_data_elements(
        environment, module_name, members=True, undoc_members=False,
        private_members=False, rst_elements=None, blacklist=None
    ):
        if rst_elements is None:
            rst_elements = {}

        # As a function can also be a variable, use the function directive
        # by default when available
        if blacklist is None:
            blacklist = []

        for data_environment in environment["data"].values():
            if data_environment["id"] in blacklist:
                continue

            name = data_environment["name"]
            description = data_environment["description"]
            if description is None and not undoc_members:
                continue

            if name.startswith("_") and not private_members:
                continue

            if members is True or name in members:
                line_number = data_environment["line_number"]
                rst_element = RSTRenderer.rst_generate(
                    directive="autodata",
                    element_id=data_environment["id"],
                    alias=data_environment["name"],
                    module_alias=module_name

                )
                rst_elements[line_number] = [rst_element]

        return rst_elements

    @staticmethod
    def get_rst_export_elements(
        file_environment, environment, module_name, rst_elements=None
    ):
        export_environment = file_environment["export"]
        import_environment = file_environment["import"]

        if rst_elements is None:
            rst_elements = {}

        for _exported_env_id, _exported_env in export_environment.items():
            from_module_id = _exported_env["module"]
            line_number = _exported_env["line_number"]

            if line_number not in rst_elements.keys():
                rst_elements[line_number] = []

            name = _exported_env["name"]
            alias = _exported_env["alias"]
            if alias is None:
                alias = name

            # Update module origin and name from import if necessary
            if (from_module_id is None and
                    _exported_env_id in import_environment.keys()):
                name = import_environment[_exported_env_id]["name"]
                from_module_id = import_environment[name]["module"]

            # Ignore element if the origin module can not be found
            if from_module_id not in environment["module"].keys():
                continue

            from_module_environment = environment["module"][from_module_id]
            from_file_id = from_module_environment["file_id"]
            from_file_env = environment["file"][from_file_id]

            if name == "default":
                rst_element = RSTRenderer.get_rst_default_from_file_environment(
                    from_file_env, alias, module_name
                )
                if rst_element is None:
                    continue

                rst_elements[line_number].append(rst_element)

            elif name == "*":
                rst_element = RSTRenderer.rst_generate(
                    directive="automodule",
                    element_id=from_module_id,
                    module_alias=module_name,
                    extra_options=[":force-partial-import:"]
                )
                rst_elements[line_number].append(rst_element)

            else:
                rst_element = RSTRenderer.get_rst_name_from_file_environment(
                    name, from_file_env, alias, module_name
                )
                if rst_element is None:
                    continue

                rst_elements[line_number].append(rst_element)

        return rst_elements

    @staticmethod
    def get_rst_default_from_file_environment(
        file_environment, alias, module_name
    ):
        for class_env in file_environment["class"].values():
            if class_env["default"]:
                return RSTRenderer.rst_generate(
                    directive="autoclass",
                    element_id=class_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

        for function_env in file_environment["function"].values():
            if function_env["default"]:
                return RSTRenderer.rst_generate(
                    directive="autofunction",
                    element_id=function_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

        for data_env in file_environment["data"].values():
            if data_env["default"]:
                return RSTRenderer.rst_generate(
                    directive="autodata",
                    element_id=data_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

    @staticmethod
    def get_rst_name_from_file_environment(
        name, file_environment, alias, module_name
    ):
        for class_env in file_environment["class"].values():
            if class_env["name"] == name and class_env["exported"]:
                return RSTRenderer.rst_generate(
                    directive="autoclass",
                    element_id=class_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

        for function_env in file_environment["function"].values():
            if function_env["name"] == name and function_env["exported"]:
                return RSTRenderer.rst_generate(
                    directive="autofunction",
                    element_id=function_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

        for data_env in file_environment["data"].values():
            if data_env["name"] == name and data_env["exported"]:
                return RSTRenderer.rst_generate(
                    directive="autodata",
                    element_id=data_env["id"],
                    alias=alias,
                    module_alias=module_name
                )

    @staticmethod
    def rst_generate(
        directive, element_id, alias=None, module_alias=None,
        extra_options=None
    ):
        if extra_options is None:
            extra_options = []

        element_rst = "\n.. js:{directive}:: {id}\n".format(
            directive=directive, id=element_id
        )

        if alias is not None:
            element_rst += "    :alias: {alias}\n".format(
                alias=alias
            )

        if module_alias is not None:
            element_rst += "    :module-alias: {module}\n".format(
                module=module_alias
            )

        for option in extra_options:
            element_rst += "    {option}\n".format(
                option=option
            )

        element_rst += "\n"
        return element_rst
