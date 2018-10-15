class SequenceLayer():
    def __init__(self, user_id, sound_id, rhythm):
        self.user_id = user_id
        self.sound_id = sound_id
        self.rhythm = rhythm

    def getUserId(self):
        return self.user_id

    def updateLayer(self, sound_id, rhythm):
        self.sound_id = sound_id
        self.rhythm = rhythm

    def getSequenceLayerObject(self):
        object = {
            'user_id': self.user_id,
            'sound_id': self.sound_id,
            'rhythm': self.rhythm
        }
        return object
