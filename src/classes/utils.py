from src.classes.warlord import Warlord

def class_by_name(class_name):
    class_object = None

    if class_name == "워로드" or "warlord":
        class_object = Warlord()
    
    return class_object