

class UnsupportedFileFormatError(ValueError):
    """Не поддерживаемый формат файла"""
    def __init__(self, incorrect_format, allowed_format):
        self.message = "Не поддерживаемый формат файла «%s»! Доступные варианты: %s" % (incorrect_format, ", ".join([f"«{f}»" for f in allowed_format]))
        super().__init__(self.message)
