class crawlerRes:
    def __init__(self, oj: str, username: str, sync: bool = True):
        self.oj = oj
        self.username = username
        self.sync = sync
        self.solved: int = 0
        self.submissions: int = 0
        self.solvedList: set = set()
        self.error: bool = False
        self.message: str = ""

    def add_solved_list(self, value):
        self.solvedList.add(value)

    def set_solved_list(self, value: list):
        self.solvedList = set(value) if value is not None else set()

    def set_solved(self, value: int):
        self.solved = value
        self.sync = False

    def get_solved(self) -> int:
        return self.solved if not self.sync else len(self.solvedList)

    def get_solved_lists(self) -> set:
        return self.solvedList

    def set_error(self, message):
        self.message = message
        self.error = True

    def __eq__(self, other):
        return self.username == other.username and self.oj == other.oj
