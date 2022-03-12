from data_retriever import DataRetriever


class Main:

    def __init__(self):
        self.main = None

    def run(self):
        data_retriever = DataRetriever()

        c = 1
        while c < 1002:
            data_retriever.pull_a_page(c)
            print("Page Number: ", c)
            c = c + 1