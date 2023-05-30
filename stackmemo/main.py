import gc
import lvgl as lv

import json
import time

from qa import qa
from questioner import Questioner

from axpili9342 import ili9341
from ft6x36 import ft6x36
from m5stack import M5Stack

display = ili9341()
touch = ft6x36()
m5 = M5Stack()

gc.collect()
m5.lcd_brightness(20)
m5.power_led(False)


style_btn_red = lv.style_t()
style_btn_red.init()
style_btn_red.set_bg_color(lv.palette_main(lv.PALETTE.RED))

style_btn_green = lv.style_t()
style_btn_green.init()
style_btn_green.set_bg_color(lv.palette_main(lv.PALETTE.GREEN))

style_btn_do = lv.style_t()
style_btn_do.init()
style_btn_green.set_bg_color(lv.palette_main(lv.PALETTE.DEEP_ORANGE))


def colorify(txt):
    opened = False
    new_text = []
    for c in txt:
        if c == "_":
            opened = not opened
            if opened:
                new_text.append("#003399 ")
            else:
                new_text.append("#")
        elif c == "*":
            opened = not opened
            if opened:
                new_text.append("#009933 ")
            else:
                new_text.append("#")
        elif c == "`":
            opened = not opened
            if opened:
                new_text.append("#993300 ")
            else:
                new_text.append("#")
        else:
            new_text.append(c)
    return "".join(new_text)


class QandA:
    def generate_candidates(self):
        self.candidates = [i for i in range(0, len(qa))]
        shuffle(self.candidates)

    def get_candidate(self):
        if not self.candidates:
            self.generate_candidates()
        return self.candidates.pop()

    def _build_ui(self):
        self._ui_off_button()
        self._ui_main_text()
        self._ui_next_button()
        self._ui_wrong_button()
        self._ui_right_button()
        # Missing: the GOOD/BAD answer buttons, need to be constructed now
    
    def off_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        self.off_button_label.set_text("Turning off, will save")
        with open("memo.json") as f:
            json.dump(self.questioner.dump())
        time.sleep(1)
        m5.power_off()

    def _ui_off_button(self):
        off_button.add_style(style_btn_do, 0)
        off_button.align(lv.ALIGN.TOP_LEFT, 8, 8)
        off_button.set_size(90, 50)
        self.off_button_label = lv.label(off_button)
        self.off_button_label.set_text("Turn off")
        self.off_button_label.align(lv.ALIGN.CENTER, 0, 0)
        off_button.add_event_cb(self.off_event_handler, lv.EVENT.ALL, None)



    def _ui_wrong_button(self):
        self.wrong_button = lv.btn(lv.scr_act())
        self.wrong_button.add_style(style_btn_red, 0)
        self.wrong_button.align(lv.ALIGN.BOTTOM_LEFT, 8, -8)
        self.wrong_button.set_size(80, 50)
        wrong_button_label = lv.label(self.wrong_button)
        wrong_button_label.set_text("Wrong")
        wrong_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.wrong_button.add_event_cb(self.wrong_handler, lv.EVENT.ALL, None)
        self.wrong_button.add_flag(lv.obj.FLAG.HIDDEN)

    def _ui_right_button(self):
        self.right_button = lv.btn(lv.scr_act())
        self.right_button.add_style(style_btn_green, 0)
        self.right_button.align(lv.ALIGN.BOTTOM_RIGHT, -8, -8)
        self.right_button.set_size(80, 50)
        right_button_label = lv.label(self.right_button)
        right_button_label.set_text("Right")
        right_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.right_button.add_event_cb(self.right_handler, lv.EVENT.ALL, None)
        self.right_button.add_flag(lv.obj.FLAG.HIDDEN)

    def _ui_next_button(self):
        self.next_button = lv.btn(lv.scr_act())
        self.next_button.align(lv.ALIGN.BOTTOM_RIGHT, -10, -10)
        self.next_button.set_size(120, 50)
        self.next_button_label = lv.label(self.next_button)
        self.next_button_label.set_text("Show answer")
        self.next_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.next_button.add_event_cb(self.show_answer_event_handler, lv.EVENT.ALL, None)

    def _ui_info_button(self):
        self.info_button = lv.btn(lv.scr_act())
        self.info_button.align(lv.ALIGN.TOP_RIGHT, 8, 8)
        self.info_button.set_size(90, 50)
        self.info_button_label = lv.label(self.info_button)
        self.info_button_label.set_text("Info")
        self.info_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.info_button.add_event_cb(self.show_info_event_handler, lv.EVENT.ALL, None)
        self.info = False



    def _ui_main_text(self):
        style_fnt = lv.style_t()
        style_fnt.init()
        style_fnt.set_text_font(lv.font_montserrat_16)
        self.label = lv.label(lv.scr_act())
        self.label.add_style(style_fnt, 0)
        self.label.set_long_mode(lv.label.LONG.WRAP)
        self.label.set_width(240)
        self.label.set_recolor(True)
        self.label.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.label.align(lv.ALIGN.CENTER, 0, -20)
        self.set_question()

    def set_question(self):
        self.question = self.qer.get_question()
        q = self.question["question"]
        self.label.set_text(colorify(q))
        self.questioning = True
        self.answering = False

    def set_answer(self):
        a = self.question["answer"]
        self.label.set_text(colorify(a))
        self.answering = True
        self.questioning = False

    def __init__(self):
        memos = {}#json.loads("memos.json")
        self.qer = Questioner(qa, memos)
        self._build_ui()

    def wrong_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        self._ui_switch_to_question()
        q = 2
        updated = memo.answered(q, self.question)
        self.questioner.update_question(updated)
        self._ui_switch_to_question()


    def right_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        q = 4.5
        updated = memo.answered(q, self.question)
        self.questioner.update_question(updated)
        self._ui_switch_to_question()

    def _ui_switch_to_question(self):
        self.wrong_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.right_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.next_button.clear_flag(lv.obj.FLAG.HIDDEN)

    def show_info_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        if self.info:
            if self.questioning:
                self.set_question()
            if self.answering:
                self.set_answer()
            self.info = False
        else:
            n = self.question["n"]
            ef = self.question["ef"]
            i_n = self.question["i_n"]
            txt = "_n_: "+n+"\n_i_n_:"+i_n+"\n_ef_: "+ef
            self.label.set_text(colorify(txt))
            self.info = False

    def show_answer_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        a = self.question["answer"]
        self.label.set_text(colorify(a))
        self.next_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.wrong_button.clear_flag(lv.obj.FLAG.HIDDEN)
        self.right_button.clear_flag(lv.obj.FLAG.HIDDEN)

QandA()
