import random
from math import ceil

def calcola_campione(N, p=0.5, E=0.05, confidenza=0.95):
    """
    Calcola la dimensione del campione necessario per ottenere una stima con il livello di confidenza dato.
    :param N: Numero totale di pagine nel volume in analisi
    :param p: Proporzione attesa di successo dello script (in questo caso si è impostato 50% per avere una maggiore dimensione del campione)
    :param E: Margine di errore accettabile (in questo caso 5%)
    :param confidenza: Livello di confidenza desiderato (in questo caso 95%)
    :return: Dimensione del campione da analizzare manualmente
    """
    # Valori Z-score corrispondenti a diversi livelli di confidenza
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    Z = z_scores.get(confidenza, 1.96)  # Default a 95%
    
    # Formula per il campione per proporzioni
    n = (Z**2 * p * (1 - p)) / (E**2)
    
    # Correzione per "popolazioni finite" (limitate)
    n_corretto = n / (1 + ((n - 1) / N))
    
    return ceil(n_corretto)  # Arrotondamento per eccesso

#La seguente funzione restituisce una lista di pagine casuali da un volume di N pagine. Può essere utilizzata per un'analisi più rappresentativa
"""def seleziona_pagine(N, n, stratificato=False):
    
    #Seleziona n pagine casuali da un volume di N pagine.
    #:param N: Numero totale di pagine nel volume
    #:param n: Numero di pagine da selezionare
    #:param stratificato: Se True, seleziona pagine distribuite equamente su tutto il volume
    #:return: Lista di pagine selezionate
    
    if stratificato:
        step = N // n  # Seleziona pagine a intervalli regolari
        pagine = [i * step + random.randint(0, step - 1) for i in range(n)]
    else:
        pagine = random.sample(range(1, N + 1), n)  # Campionamento casuale
    
    return sorted(pagine)"""

if __name__ == "__main__":
    N = int(input("Numero totale di pagine nel volume: "))
    livello_confidenza = 0.95  # Default a 95%
    margine_errore = 0.05  # Default 5%
    
    n_campione = calcola_campione(N, E=margine_errore, confidenza=livello_confidenza)
    print(f"Dimensione del campione necessario: {n_campione} pagine")
    
    """stratificato = input("Vuoi un campionamento stratificato? (si/no): ").lower() == 'si'
    pagine_selezionate = seleziona_pagine(N, n_campione, stratificato)
    print(f"Pagine da codificare manualmente: {pagine_selezionate}")"""