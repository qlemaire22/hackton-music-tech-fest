from sequence_layer import SequenceLayer


class Hub():
    def __init__(self, id, location):
        self.location = location
        self.id = id
        self.sequence = []
        # print(len(self.sequence))

    def addLayer(self, layer):
        self.sequence.append(layer)

    def updateLayer(self, user_id, sound_id, rhythm):
        updated = False
        for l in self.sequence:
            if user_id == l.getUserId():
                updated = True
                l.updateLayer(sound_id, rhythm)
        if not(updated):
            self.sequence.append(SequenceLayer(user_id, sound_id, rhythm))

    def getHubObject(self):
        object = []
        for l in self.sequence:
            object.append(l.getSequenceLayerObject())
        return object

    def getLocation(self):
        return self.location
