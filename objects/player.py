import aiobcrypt
import databases

import settings
from constants.auth import AuthResponse
class Player:
    def __init__(self) -> None:
        self._id: int = 0
        self._username: str = ""
        self._hash: str = ""
        self._deviceId: str = ""
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
    def username_safe(self):
        return self._username.lower().replace(" ", "_")

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

    async def connect(self) -> AuthResponse:
        async with databases.Database(settings.DB_DSN) as db:
            result = await db.fetch_one(
                "SELECT * FROM players WHERE username = :username_safe",
                {"username_safe": self.username_safe},
            )

            if not result:
                return await self._register()

            if result["device_id"] and not result["device_id"] == self.deviceId:
                return AuthResponse.ALREADY_LINKED  # device already linked

            if not await aiobcrypt.checkpw(
                self.hash.encode("utf-8"),
                result["hash"].encode("utf-8"),
            ):
                return AuthResponse.CREDENTIAL_MISMATCH  # password incorrect

            # update the device_id and device_type if necessary
            if (
                result["device_id"] != self.deviceId
                or result["device_type"] != self.deviceType
            ):
                await db.execute(
                    "UPDATE players SET device_id = :device_id, device_type = :device_type WHERE username_safe = :username_safe",
                    {
                        "device_id": self.deviceId,
                        "device_type": self.deviceType,
                        "username_safe": self.username_safe,
                    },
                )

            return AuthResponse.SUCCESS  # successful login

    async def _register(self) -> AuthResponse:
        async with databases.Database(settings.DB_DSN) as db:
            hash_bcrypt = await aiobcrypt.hashpw(
                self.hash.encode("utf-8"),
                await aiobcrypt.gensalt(),
            )

            await db.execute(
                "INSERT INTO players (username, username_safe, hash, device_id, device_type) VALUES (:username, :username_safe, :hash, :device_id, :device_type)",
                {
                    "username": self.username,
                    "username_safe": self.username_safe,
                    "hash": hash_bcrypt,
                    "device_id": self.deviceId,
                    "device_type": self.deviceType,
                },
            )
            return AuthResponse.SUCCESS  # successful registration -> login

    async def disconnect(self) -> AuthResponse:
        async with databases.Database(settings.DB_DSN) as db:
            hash = await db.fetch_one(
                "SELECT hash FROM players WHERE username = :username_safe",
                {"username_safe": self.username_safe},
            )

            if not hash or not await aiobcrypt.checkpw(
                self.hash.encode("utf-8"),
                hash[0].encode("utf-8"),
            ):
                return AuthResponse.CREDENTIAL_MISMATCH  # password incorrect

            await db.execute(
                "UPDATE players SET device_id = NULL, device_type = NULL WHERE username_safe = :username_safe",
                {"username_safe": self.username_safe},
            )
            return AuthResponse.SUCCESS  # successful logout
    @classmethod
    def from_submission(cls, data: str) -> "Player":
        device_id = data.split("&")[0].split("=")[1]
        player_hash = data.split("&")[12].split("=")[1]
        username = data.split("&")[15].split("=")[1]
        device_type = int(data.split("&")[16].split("=")[1])

        p = cls()
        p.deviceId = device_id
        p.hash = player_hash
        p.username = username
        p.deviceType = device_type

        return p

    @classmethod
    def from_connect(cls, args: dict) -> "Player":
        device_id = args.get("udid")
        username = args.get("username")
        hash = args.get("cc")

        p = cls()
        p.deviceId = device_id
        p.username = username
        p.hash = hash

        return p

    @classmethod
    def from_disconnect(cls, args: dict) -> "Player":
        username = args.get("username")
        hash = args.get("cc")

        p = cls()
        p.username = username
        p.hash = hash

        return p
