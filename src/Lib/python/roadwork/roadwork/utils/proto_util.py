class ProtoUtil:
    @staticmethod
    def json_object_to_proto_map(jsonObject):
        info = {}

        for key, value in jsonObject.items():
            if type(value) == bool:
                info[key] = str(int(value)) # Convert bool to 0 or 1
            else:
                info[key] = str(value)
        
        return info