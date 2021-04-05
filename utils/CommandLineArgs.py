class CommandLineArgs:
    def _convert_type (self, type_string, value):
        if type_string == 'int':
            return int(value)
        elif type_string == 'str':
            return str(value)
        elif type_string == 'float':
            return float(value)
        elif type_string == 'bool':
            return value == 'True'
        else:
            raise CommandInputError(f"Type '{type_string}' is not valid")

    def __init__(self, argv, *args):
        self._arguments = {}
        self._template = args
        for i,x in enumerate(args):
            split = x.split(":")
            if len(split) != 3:
                raise CommandFormatError(f"Argument '{x}' template is incorrectly formatted")
            key = split[0]
            type_string = split[1]
            default = split[2]
            required = default == '!'                
            if len(argv) <= i:
                if required:
                    raise CommandInputError(f"Required argument '{x}' is missing")
                else:
                    try:
                        self._arguments[key] = self._convert_type(type_string, default)
                    except ValueError:
                        raise CommandInputError(f"Default value for '{x}' is of an incorrect type")
            else:
                value = argv[i]
                if required and not value:
                    raise CommandInputError(f"Required argument '{x}' is missing")
                try:
                    value = self._convert_type(type_string, value)
                except ValueError:
                    raise CommandInputError(f"Argument '{x}' is of an incorrect type")
                self._arguments[key] = value

    def get (self, key):
        try:
            return self._arguments[key]
        except KeyError:
            raise CommandArgumentDoesNotExistError(f"Argument '{key}' does not exist")

class CommandInputError(Exception):
    pass

class CommandFormatError(Exception):
    pass

class CommandArgumentDoesNotExistError(Exception):
    pass