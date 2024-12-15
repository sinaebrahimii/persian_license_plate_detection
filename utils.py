def replace_class_id(class_id):
    """
    Maps a single class_id integer to a new value based on specific rules, converts it to a string, and returns it.

    Args:
        class_id (int): The class_id to be mapped.

    Returns:
        str: The mapped class_id as a string.
    """
    if class_id == 1:
        class_id = 9
    elif class_id == 3:
        class_id = "DAL"
    elif class_id == 15:
        class_id = "SAD"
    elif class_id == 16:
        class_id = "NOON"
    elif class_id == 6:
        class_id = "JIM"
    elif class_id == 14:
        class_id = "SIN"
    elif class_id == 18:
        class_id = "VAV"
    elif class_id == 18:
        class_id = "TA"
    elif class_id == 11:
        class_id = 1
    elif class_id == 20:
        class_id = 2
    elif class_id == 21:
        class_id = 3
    elif class_id == 22:
        class_id = 4
    elif class_id == 23:
        class_id = 5
    elif class_id == 24:
        class_id = 6
    elif class_id == 25:
        class_id = 7
    elif class_id == 26:
        class_id = 8
    
    return str(class_id)



def make_text(character_list:list[dict])->str:
    text:str=''
    for ch in character_list:
       text+= " " + str(ch.get("class"))
    return text