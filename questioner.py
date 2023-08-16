class Questioner:
    def __init__(self, qas, memo):
        self.qas = []
        for qa in qas:
            qa.update(memo.get(qa["id"], self._default_info()))
            self.qas.append(qa)
        self._sort()
        self.asked = []
        self.q_index = 0

    def _sort(self):
        """Shouldn't be extremely expensive to compute, since it's almost all sorted after the first"""
        self.qas.sort(key=lambda f: f["i_n"])

    def _default_info(self):
        return {"n": 0, "i_n": 0, "ef": 2.5}

    def get_question(self):
        for idx, qa in enumerate(self.qas):
            if qa["id"] not in self.asked:
                self.q_index = idx
                return qa

    def update_question(self, new_memo):
        """The question to be updated is in self.q_index"""
        self.qas[self.q_index].update(new_memo)
        self.asked.append(self.qas[self.q_index]["id"])
        self._sort()

    def dump_memos(self):
        memos = {}
        for qa in self.qas:
            memos[qa["id"]] = {"n": qa["n"], "i_n": qa["i_n"], "ef": qa["ef"]}
        return memos
