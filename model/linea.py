from dataclasses import dataclass


@dataclass
class Linea:
    id_linea: int
    nome: str
    velocita: float
    intervallo: float
    colore: str

    # non scrivo un to string perché probabilmente non dovrò stampare l'oggetto Linea,
    # non scrivo un hash function perché probabilmente non saranno nodi del nostro grafo
