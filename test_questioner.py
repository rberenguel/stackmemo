import unittest
import questioner as qer


class TestQuestioner(unittest.TestCase):
    qa = [
        {"id": "q0", "question": "foo?", "answer": "bar"},
        {"id": "q1", "question": "bar?", "answer": "foo"},
    ]
    answer_info = {"q0": {"n": 2, "i_n": 5, "ef": 2.5}}

    def test_get_question(self):
        questioner = qer.Questioner(self.qa, self.answer_info)
        q = questioner.get_question()
        self.assertEqual(q["id"], "q1")

    def test_update_question(self):
        questioner = qer.Questioner(self.qa, self.answer_info)
        questioner.update_question({"n": 12, "i_n": 6, "ef": 2.5})
        q = questioner.get_question()
        self.assertEqual(q["id"], "q0")
        q = questioner.qas[-1]
        self.assertEqual(q["n"], 12)
        self.assertEqual(q["i_n"], 6)
        self.assertEqual(q["ef"], 2.5)

    def test_dump(self):
        questioner = qer.Questioner(self.qa, self.answer_info)
        questioner.update_question({"n": 12, "i_n": 6, "ef": 2.5})
        dump = questioner.dump_memos()
        self.assertEqual(dump["q0"]["n"], 2)
        self.assertEqual(dump["q0"]["i_n"], 5)
        self.assertEqual(dump["q1"]["n"], 12)
        self.assertEqual(dump["q1"]["i_n"], 6)


if __name__ == "__main__":
    unittest.main()
