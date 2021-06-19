class FieldFormatIncorrect(Exception):

    def __init__(self, message):
        self.message = message
        super(FieldFormatIncorrect, self).__init__(self.message)
