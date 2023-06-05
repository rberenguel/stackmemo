"""
A simple spaced repetition system for the M5Stack Core2
and probably also other ESP32 devices with similar screens
and capabilities.
"""

import gc
import lvgl as lv

import json
import time

from colorify import colorify
from qa import qa
from questioner import Questioner
import memo

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
style_btn_do.set_bg_color(lv.palette_main(lv.PALETTE.DEEP_ORANGE))

style_btn_clean = lv.style_t()
style_btn_clean.init()
style_btn_clean.set_bg_color(lv.palette_main(lv.PALETTE.NONE))
style_btn_clean.set_border_width(0)
style_btn_clean.set_radius(0)


class QandA:
    def __init__(self):
        try:
            f = open("memos.json")
            memos = json.load(f)
        except:
            memos = {}
        try:
            f = open("to_edit.json")
            self.to_edit = json.load(f)
        except:
            self.to_edit = []
        self.qer = Questioner(qa, memos)
        self.off_button = None
        self.next_button = None
        self.q_counter = 0
        self._build_ui()

    def _build_ui(self):
        self._ui_main_text()
        self._ui_off_button()
        self._ui_next_button()
        self._ui_wrong_button()
        self._ui_right_button()
        self._ui_to_edit_button()

    def off_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        with open("memos.json", "w") as f:
            json.dump(self.qer.dump_memos(), f)
        try:
            if self.to_edit:
                with open("to_edit.json", "w") as f:
                    json.dump(self.to_edit, f)
        except:
            pass
        time.sleep(2)
        m5.power_off()

    def _ui_to_edit_button(self):
        self.to_edit_button = lv.btn(lv.scr_act())
        self.to_edit_button.align(lv.ALIGN.TOP_RIGHT, -3, 3)
        self.to_edit_button.set_size(150, 150)
        to_edit_button_label = lv.label(self.to_edit_button)
        to_edit_button_label.set_text("To fix")
        to_edit_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.to_edit_button.add_event_cb(self.to_edit_handler, lv.EVENT.ALL, None)
        self.to_edit_button.add_flag(lv.obj.FLAG.HIDDEN)

    def _ui_off_button(self):
        self.off_button = lv.btn(lv.scr_act())
        self.off_button.add_style(style_btn_do, 0)
        self.off_button.align(lv.ALIGN.TOP_LEFT, 3, 3)
        self.off_button.set_size(60, 50)
        self.off_button_label = lv.label(self.off_button)
        self.off_button_label.set_text(lv.SYMBOL.POWER)
        self.off_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.off_button.add_event_cb(self.off_event_handler, lv.EVENT.ALL, None)

    def _ui_wrong_button(self):
        self.wrong_button = lv.btn(lv.scr_act())
        self.wrong_button.add_style(style_btn_red, 0)
        self.wrong_button.align(lv.ALIGN.BOTTOM_LEFT, 8, -8)
        self.wrong_button.set_size(100, 50)
        wrong_button_label = lv.label(self.wrong_button)
        wrong_button_label.set_text("Wrong")
        wrong_button_label.align(lv.ALIGN.CENTER, 0, 0)
        self.wrong_button.add_event_cb(self.wrong_handler, lv.EVENT.ALL, None)
        self.wrong_button.add_flag(lv.obj.FLAG.HIDDEN)

    def _ui_right_button(self):
        self.right_button = lv.btn(lv.scr_act())
        self.right_button.add_style(style_btn_green, 0)
        self.right_button.align(lv.ALIGN.BOTTOM_RIGHT, -8, -8)
        self.right_button.set_size(100, 50)
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
        self.next_button.add_event_cb(
            self.show_answer_event_handler, lv.EVENT.ALL, None
        )

    def _ui_main_text(self):
        style_fnt = lv.style_t()
        style_fnt.init()
        style_fnt.set_text_font(lv.font_montserrat_16)
        self.button = lv.btn(lv.scr_act())
        self.button.align(lv.ALIGN.TOP_LEFT, 0, 0)
        self.button.set_size(320, 240)
        self.button.add_style(style_btn_clean, 0)
        self.label = lv.label(self.button)
        self.label.add_style(style_fnt, 0)
        self.label.set_long_mode(lv.label.LONG.WRAP)
        self.label.set_width(300)
        self.label.set_recolor(True)
        self.label.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.label.align(lv.ALIGN.CENTER, 0, -35)
        self.set_question()
        self.button.add_event_cb(self.show_info_event_handler, lv.EVENT.ALL, None)

    def set_question(self):
        self.question = self.qer.get_question()
        q = self.question["question"]
        self.label.set_text(colorify(q))
        self.questioning = True
        self.answering = False
        self.info = False
        if self.next_button:
            self.next_button.clear_flag(lv.obj.FLAG.HIDDEN)
        if self.off_button:
            self.off_button.clear_flag(lv.obj.FLAG.HIDDEN)

    def set_answer(self):
        a = self.question["answer"]
        self.label.set_text(colorify(a))
        self.answering = True
        self.questioning = False
        self.info = False
        self.off_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.wrong_button.clear_flag(lv.obj.FLAG.HIDDEN)
        self.right_button.clear_flag(lv.obj.FLAG.HIDDEN)

    def to_edit_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        self.to_edit += [self.question["id"]]

    def wrong_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        q = 2
        updated = memo.answered(q, self.question)
        self.qer.update_question(updated)
        self.q_counter += 1
        self._ui_switch_to_question()

    def right_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        q = 4.5
        updated = memo.answered(q, self.question)
        self.qer.update_question(updated)
        self.q_counter += 1
        self._ui_switch_to_question()

    def _ui_switch_to_question(self):
        self.wrong_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.right_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.next_button.clear_flag(lv.obj.FLAG.HIDDEN)
        self.set_question()

    def show_info_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        if self.info:
            self.to_edit_button.add_flag(lv.obj.FLAG.HIDDEN)
            if self.questioning:
                self.set_question()
            if self.answering:
                self.set_answer()
            self.info = False
        else:
            self.to_edit_button.clear_flag(lv.obj.FLAG.HIDDEN)
            self.off_button.add_flag(lv.obj.FLAG.HIDDEN)
            self.wrong_button.add_flag(lv.obj.FLAG.HIDDEN)
            self.right_button.add_flag(lv.obj.FLAG.HIDDEN)
            self.next_button.add_flag(lv.obj.FLAG.HIDDEN)
            n = self.question["n"]
            ef = self.question["ef"]
            i_n = self.question["i_n"]
            txt = (
                "_n_:  "
                + str(n)
                + "\n_i.n_:  "
                + str(i_n)
                + "\n_ef_:  "
                + str(ef)
                + "\n*c*:  "
                + str(self.q_counter)
                + "\n*F*:  "
                + str(len(self.to_edit))
            )
            self.label.set_text(colorify(txt))
            self.info = True

    def show_answer_event_handler(self, evt):
        code = evt.get_code()
        if code != lv.EVENT.CLICKED:
            return
        self.set_answer()
        self.next_button.add_flag(lv.obj.FLAG.HIDDEN)
        self.wrong_button.clear_flag(lv.obj.FLAG.HIDDEN)
        self.right_button.clear_flag(lv.obj.FLAG.HIDDEN)


QandA()
