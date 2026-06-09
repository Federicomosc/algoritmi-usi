"""
Coda circolare con array — implementazione di ENQUEUE (e DEQUEUE per testarla).

Il pseudocodice del corso usa indici 1-based (posizioni 1 … length).
In Python usiamo una lista di lunghezza length+1: l'indice 0 resta inutilizzato,
così Q[1] … Q[length] corrispondono esattamente al diagramma del PDF.

Animazione visiva: apri esercizi/coda_circolare.html nel browser
(o esegui: python3 esercizi.py --anim)
"""

import sys
import webbrowser
from pathlib import Path

class Queue:
    def __init__(self, length: int):
        self.length = length
        # Indice 0 non usato → Q[i] coincide con la posizione i del diagramma
        self.Q = [None] * (length + 1)
        self.head = 1
        self.tail = 1
        self.queue_empty = True
        self.queue_full = False

    def enqueue(self, x):
        """ENQUEUE(Q, x) — pseudocodice del corso."""
        if self.queue_full:
            raise OverflowError("overflow")

        # 1. inserisci x nella posizione tail
        self.Q[self.tail] = x

        # 2. avanza tail (circolare: dopo length torna a 1)
        if self.tail < self.length:
            self.tail = self.tail + 1
        else:
            self.tail = 1

        # 3. se tail raggiunge head, la coda è piena
        if self.tail == self.head:
            self.queue_full = True

        # 4. abbiamo almeno un elemento
        self.queue_empty = False

    def dequeue(self):
        """DEQUEUE(Q) — complemento per testare la coda."""
        if self.queue_empty:
            raise IndexError("underflow")

        x = self.Q[self.head]

        if self.head < self.length:
            self.head = self.head + 1
        else:
            self.head = 1

        if self.head == self.tail:
            self.queue_empty = True

        self.queue_full = False
        return x

    def __repr__(self):
        if self.queue_empty:
            contenuto = "[]"
        elif self.queue_full:
            # tutti gli slot occupati
            if self.head <= self.tail:
                idx = list(range(self.head, self.tail)) + list(range(self.tail, self.length + 1)) + list(range(1, self.head))
            else:
                idx = list(range(self.head, self.length + 1)) + list(range(1, self.tail))
            # quando full, head==tail: elementi da head in avanti circolare
            idx = list(range(self.head, self.length + 1)) + list(range(1, self.head))
            contenuto = str([self.Q[i] for i in idx])
        elif self.head < self.tail:
            contenuto = str([self.Q[i] for i in range(self.head, self.tail)])
        else:
            contenuto = str(
                [self.Q[i] for i in range(self.head, self.length + 1)]
                + [self.Q[i] for i in range(1, self.tail)]
            )
        return (
            f"Queue(head={self.head}, tail={self.tail}, "
            f"empty={self.queue_empty}, full={self.queue_full}, data={contenuto})"
        )


def demo_stato_diagramma():
    """
    Ricrea lo stato del diagramma del PDF:
    - array da 12 posizioni
    - head → slot 6  (primo elemento da estrarre)
    - tail → slot 12 (prossimo inserimento)
    - elementi occupati: slot 6, 7, 8, 9, 10, 11
    """
    q = Queue(12)
    q.head = 6
    q.tail = 12
    q.queue_empty = False
    q.queue_full = False
    for i, val in enumerate(["A", "B", "C", "D", "E", "F"], start=6):
        q.Q[i] = val
    return q


def Pingala_Inc(n: int) -> int:
    if n <= 2:
        return n
    pprev, prev = 1, 2
    for _ in range(3, n + 1):
        pprev, prev = prev, prev + pprev
    return prev


def apri_animazione():
    """Apre il simulatore animato nel browser."""
    path = Path(__file__).parent / "coda_circolare.html"
    url = path.as_uri()
    print(f"Apro animazione: {url}")
    webbrowser.open(url)


if __name__ == "__main__":
    if "--anim" in sys.argv or "-a" in sys.argv:
        apri_animazione()
        sys.exit(0)

    print("=== Coda circolare — ENQUEUE ===")
    print("Tip: python3 esercizi.py --anim  →  simulatore animato nel browser\n")

    q = demo_stato_diagramma()
    print("Stato iniziale (come nel diagramma):")
    print(q)
    print("  → head=6: il prossimo DEQUEUE restituisce 'A'")
    print("  → tail=12: il prossimo ENQUEUE scrive nello slot 12\n")

    print("ENQUEUE(q, 'G')")
    q.enqueue("G")
    print(q)
    print("  → 'G' va in Q[12], tail passa da 12 a 1 (wrap-around)\n")

    print("ENQUEUE(q, 'H')")
    q.enqueue("H")
    print(q)
    print("  → 'H' va in Q[1], tail passa a 2\n")

    print("DEQUEUE(q) →", q.dequeue())
    print(q)
    print("  → head avanza da 6 a 7\n")

    print("=== Pingala (esercizio precedente) ===")
    print("Pingala_Inc(10) =", Pingala_Inc(10))
