# -*- coding: utf-8 -*-
"""夹饼桌面宠物 手机版 (Kivy)"""
import os
import glob
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

BASE = os.path.dirname(os.path.abspath(__file__))
ANIM_DIR = os.path.join(BASE, "anim")

ANIMS = {
    "idle":    ("待机",   "loop", 90,  None),
    "bark":    ("汪汪叫", "once", 80,  "idle"),
    "happy":   ("开心",   "once", 70,  "idle"),
    "eat":     ("吃东西", "once", 90,  "happy"),
    "poop":    ("拉屎",   "once", 90,  "idle"),
    "curious": ("歪头",   "once", 90,  "idle"),
    "sleep":   ("睡觉",   "loop", 130, None),
    "belly":   ("仰躺",   "once", 80,  "idle"),
}
TARGET_MS = 5000


class BeaglePet(FloatLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.frames = {}
        self._load_anims()

        self.anim_state = "idle"
        self.frame_idx = 0
        self.loops_left = 1
        self.on_end = None

        # 宠物图像
        self.pet = Image(allow_stretch=True, keep_ratio=True, size_hint=(None, None))
        self.pet.pos_hint = {"center_x": 0.5, "center_y": 0.55}
        self.add_widget(self.pet)

        # 底部按钮栏
        bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=60,
                        pos_hint={"bottom": 1})
        buttons = [
            ("🦴", "feed",  "#D97706"),
            ("🤚", "pet",   "#E11D48"),
            ("🎾", "tease", "#7C3AED"),
            ("💩", "poop",  "#92400E"),
        ]
        for label, action, color in buttons:
            btn = Button(text=label, font_size=24, background_color=[0, 0, 0, 0],
                         color=[1, 1, 1, 1], size_hint_x=1)
            btn.background_normal = ""
            btn.background_color = [0.3, 0.3, 0.3, 0.8]
            btn.bind(on_press=lambda b, a=action: self._on_button(a))
            bar.add_widget(btn)
        self.add_widget(bar)

        # 随机行为定时器
        self._next_random = 15
        Clock.schedule_interval(self._tick, 0.09)
        Clock.schedule_interval(self._random_tick, 1.0)

        self._play("idle")

        # 触摸拖动
        self._touch_offset = None
        self._drag_start = None

    def _load_anims(self):
        for name in ANIMS:
            d = os.path.join(ANIM_DIR, name)
            files = sorted(glob.glob(os.path.join(d, "f*.png")))
            if files:
                self.frames[name] = files
                Logger.info(f"Loaded {name}: {len(files)} frames")

    def _play(self, name):
        if name not in self.frames:
            name = "idle"
        self.anim_state = name
        self.frame_idx = 0
        cfg = ANIMS[name]
        self.on_end = cfg[3]
        if cfg[1] == "loop":
            self.loops_left = 999999
        else:
            n = len(self.frames[name])
            dur_per_loop = cfg[2] * n
            self.loops_left = max(2, int(-(-TARGET_MS // dur_per_loop)))

    def _tick(self, dt):
        frames = self.frames.get(self.anim_state)
        if not frames:
            return
        n = len(frames)
        self.frame_idx += 1
        if self.frame_idx >= n:
            cfg = ANIMS[self.anim_state]
            if cfg[1] == "loop":
                self.frame_idx = 0
            elif self.loops_left > 1:
                self.loops_left -= 1
                self.frame_idx = 0
            else:
                end = self.on_end or "idle"
                self._play(end)
                return
        self.pet.source = frames[self.frame_idx]
        self.pet.canvas.ask_update()

    def _random_tick(self, dt):
        if self.anim_state == "idle":
            self._next_random -= dt
            if self._next_random <= 0:
                act = random.choice(["curious", "poop", "bark", "belly", "sleep"])
                self._play(act)
                self._next_random = random.uniform(20, 40)

    def _on_button(self, action):
        if action == "feed":
            self._play("eat")
        elif action == "pet":
            self._play("belly")
        elif action == "tease":
            self._play(random.choice(["bark", "curious"]))
        elif action == "poop":
            self._play("poop")

    def on_touch_down(self, touch):
        if self.pet.collide_point(*touch.pos):
            self._touch_offset = (touch.x - self.pet.x, touch.y - self.pet.y)
            self._drag_start = touch.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_offset:
            self.pet.x = touch.x - self._touch_offset[0]
            self.pet.y = touch.y - self._touch_offset[1]
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._touch_offset:
            dx = touch.x - self._drag_start[0]
            dy = touch.y - self._drag_start[1]
            if abs(dx) < 10 and abs(dy) < 10:
                # 单击 = 摸摸
                self._play("belly")
            self._touch_offset = None
            self._drag_start = None
        return super().on_touch_up(touch)


class BeagleApp(App):
    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        return BeaglePet()


if __name__ == "__main__":
    BeagleApp().run()
