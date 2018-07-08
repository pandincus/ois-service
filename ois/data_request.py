from .data_request_type import DataRequestType

class DataRequest():

    def __init__(self, fieldName, requestType):
        self.fieldName = fieldName
        self.requestType = requestType
        self.value = 0

