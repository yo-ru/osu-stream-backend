class Player:
    def __init__(self) -> None:
        self._id: int = 0
        self._username: str = ''
        self._hash: str = ''
        self._deviceId: str = ''
        self._deviceType: int = 0
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
        
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value: str):
        self._username = value
        
    @property
    def hash(self):
        return self._hash
    
    @hash.setter
    def hash(self, value: str):
        self._hash = value
        
    @property
    def deviceId(self):
        return self._deviceId
    
    @deviceId.setter
    def deviceId(self, value: str):
        self._deviceId = value
        
    @property
    def deviceType(self):
        return self._deviceType
    
    @deviceType.setter
    def deviceType(self, value: int):
        self._deviceType = value

    @classmethod
    def from_submission(cls, data: str) -> 'Player':
        device_id = data.split('&')[0].split('=')[1]
        player_hash = data.split('&')[12].split('=')[1]
        username = data.split('&')[15].split('=')[1]
        device_type = int(data.split('&')[16].split('=')[1])
        
        p = cls()
        p.deviceId = device_id
        p.hash = player_hash
        p.username = username
        p.deviceType = device_type
        
        return p
        
        