from perceval.backends.core.github import GitHub


class Ingester:
    def __init__(self) -> None:
        self.g = GitHub("tensorflow", "tensorflow", ["<private-key-here>"])

    def get_data(self):
        for data in self.g.fetch():
            print(data)


if __name__ == "__main__":
    i = Ingester()
    i.get_data()
