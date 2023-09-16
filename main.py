from multiprocessing import Pool

import wikipedia
import warnings
from bs4 import GuessedAtParserWarning

warnings.filterwarnings('ignore', category=GuessedAtParserWarning)


class WikipediaGame:

    def __init__(self):
        self.solutions = []
        self.visitedNodes = set()

    def reset(self):
        self.solutions = []
        self.visitedNodes = set()

    def shortestDistanceWrapper(self, argDict):
        if len(self.solutions) != 0:
            return
        try:
            self.shortestDistance(titles=argDict["titles"], target=argDict["target"])
        except Exception:
            return

    def shortestDistance(self, *, titles: [], target: str):
        a = wikipedia.page(titles[-1])

        unvisitedPages = []
        for link in a.links:
            if link in self.visitedNodes:
                continue
            self.visitedNodes.add(link)
            unvisitedPages.append(link)
        # print(f"looking between {titles} and {target}, through {unvisitedPages}")

        if target in unvisitedPages:
            path = titles + [target]
            print(f"found path: {path}")
            self.solutions.append(path)
            return

        with Pool(60) as p:
            p.map(self.shortestDistanceWrapper,
                  [{"titles": titles + [title], "target": target} for title in unvisitedPages])


if __name__ == '__main__':
    w = WikipediaGame()
    w.shortestDistance(titles=["Giraffe"], target="International Union for Conservation of Nature")
    w.reset()
    w.shortestDistance(titles=["Giraffe"], target="Tendon")
    w.reset()
