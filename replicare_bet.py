#!/usr/bin/env python3
import sys
import logging
import argparse

import portfolio
import crawler_bvb

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(sys.argv[0][:-2] + "log"),
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser(prog=sys.argv[0], add_help=False)
    parser.add_argument("sum", 
        type = float,
        help = "sum care se dorește investită, în RON")
    parser.add_argument("-h", "--help",
        action = "help",
        help = "se va afișa acest mesaj și se va ieși")
    parser.add_argument("-p", "--no-prices",
        action = "store_true",
        help = "nu se va încerca obținerea prețurilor de pe internet, se vor folosi cele din fișierul csv")
    parser.add_argument("-w", "--no-weights",
        action = "store_true",
        help = "nu se va încerca obținerea ponderilor în BET de pe internet, se vor folosi ponderile din fișierul csv")
    parser.add_argument("-c", "--comission", 
        type = float,
        default = 0.65,
        help = "comisionul broker-ului, în procente; valoarea implicită este 0.65")
    parser.add_argument("-m", "--min-comission", 
        type = float,
        default = 1.9,
        help = """comisionul minim al broker-ului, în RON; valoarea implicită este 1.9; 
                    script-ul va sugera cumpărarea unui simbol doar dacă se atinge sau depășește comisionul minim""")
    parser.add_argument("-f", "--file",
        default = "portofoliu.csv",
        help = "numele fișierului csv din care se vor citi deținerile curenteș valoarea implicită este 'portofoliu.csv'")

    args = parser.parse_args()

    p = portfolio.Portfolio()
    if not p.readStocks(args.file):
        return
    print(f"Suma de investit: {args.sum}")
    print(f"Comision broker: {args.comission}%")
    print(f"Comision minim broker: {args.min_comission}")
    print()
    if not (args.no_prices and args.no_weights):
        crawlData = crawler_bvb.crawl()
        if not args.no_prices:
            p.updatePrice(crawlData)
        if not args.no_weights:
            p.updateWeight(crawlData)
    p.display()
    

if __name__ == "__main__":
    main()