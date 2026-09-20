def verify_type(obj_to_verify: object, type: type, function_name: str, variable_name: str) -> None:
    if not isinstance(obj_to_verify, type):
        raise TypeError(f"{function_name} Le paramètre {variable_name} doit être du type {type}.")