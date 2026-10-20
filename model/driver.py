from dataclasses import dataclass, field


@dataclass
class Driver:
    driverId: int
    forename: str
    surname: str
    nationality: str
    vittorie: int = 0
    circuiti: set = field(default_factory=set)    # circuiti su cui ha vinto nel periodo

    def __hash__(self):
        return hash(self.driverId)

    def __eq__(self, other):
        return self.driverId == other.driverId

    def __str__(self):
        return f"{self.forename} {self.surname}"