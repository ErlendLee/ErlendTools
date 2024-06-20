import re
import os
# import json
import datetime
import sublime
import sublime_plugin
from sublime import Window, View
from sublime_plugin import EventListener

from .ErlendTRS import baidu_translate_api as my_trans


TAG = '\n' + ('-' * 10) + '\n'


class SharedOutputPanelListener(EventListener):
    OUTPUT_PANEL_NAME = "GPT"

    def __init__(self, window: Window = None, markdown: bool = True) -> None:
        super().__init__()
        self.markdown: bool = markdown
        self.window: Window = window
        self.output_panel: View = self.window.find_output_panel(
            self.OUTPUT_PANEL_NAME) or self.window.create_output_panel(self.OUTPUT_PANEL_NAME)

        if self.markdown:
            self.output_panel.set_syntax_file(
                "Packages/Markdown/MultiMarkdown.sublime-syntax")

    def toggle_overscroll(self, enabled: bool):
        self.output_panel.settings().set("scroll_past_end", enabled)

    def update_output_panel(self, text: str):
        self.output_panel.set_read_only(False)
        self.output_panel.run_command('append', {'characters': text})
        self.output_panel.set_read_only(True)

    def refresh_output_panel(self):
        self.output_panel.set_read_only(False)
        # scrolling panel to the bottom.
        point = self.output_panel.text_point(
            __get_number_of_lines__(view=self.output_panel), 0)
        self.output_panel.show_at_center(point)
        self.output_panel.set_read_only(True)

    def clear_output_panel(self):
        self.show_panel()
        self.output_panel.set_read_only(False)
        # self.output_panel.erase(edit, sublime.Region(0, self.output_panel.size()))
        self.output_panel.run_command("select_all")
        self.output_panel.run_command("right_delete")

    def show_panel(self):
        self.window.run_command(
            "show_panel", {"panel": f"output.{self.OUTPUT_PANEL_NAME}"})

    def save_panel(self, path):
        content = self.output_panel.substr(
            sublime.Region(0, self.output_panel.size()))
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            print("保存路径不存在")
        with open(path, 'a') as f:
            f.write(content)


def __get_number_of_lines__(view: View) -> int:
    last_line_num = view.rowcol(view.size())[0]
    return last_line_num


def get_trans_result(r_str):
    """
    TODO 异常处理
    """
    text = []
    for i in r_str['trans_result']:
        text.append(i['dst'])
    return '\n'.join(text) + '\n'


class Translate(sublime_plugin.TextCommand):
    def run(self, edit, to_lang):
        selection = self.view.sel()
        old_text = self.view.substr(selection[0])

        query = old_text

        from_lang = 'auto'
        # to_lang en 英文；zh 中文
        # r_str = my_trans(from_lang, to_lang, query)
        url = xxx
        data = xxx
        r_str = requests.request("POST", url, json=data).json()

        new_text = TAG + get_trans_result(r_str)
        self.view.insert(edit, max(selection[0].a, selection[0].b), new_text)


class AddCurrentDate(sublime_plugin.TextCommand):
    def run(self, edit):
        today_f = datetime.datetime.now().strftime("%Y-%m-%d")
        insert_text = 'Modified on ' + today_f
        self.view.run_command("insert_snippet", {"contents": insert_text})


class FormatSelectText(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        region = sublime.Region(selection[0].a, selection[0].b)
        old_text = self.view.substr(selection[0])

        lines = old_text.split('\n')
        lines_clo_list = []

        max_len = 1
        max_clo_len = {}

        for line in lines:
            each = line.split()
            lines_clo_list.append(each)
            if len(each) > max_len:
                max_len = len(each)
            for index in range(0, len(each)):
                max_clo_len.setdefault(index, 0)
                if len(each[index]) > max_clo_len[index]:
                    max_clo_len[index] = len(each[index])

        new_lines = []
        for a_line_list in lines_clo_list:
            a = []
            for ind in range(0, len(a_line_list)):
                fill_num = max_clo_len[ind] - len(a_line_list[ind]) + 1
                each_clo = a_line_list[ind] + ' ' * fill_num
                a.append(each_clo)
            new_lines.append(''.join(a).rstrip())
        new_text = '\n'.join(new_lines)

        self.view.replace(edit, region, new_text)


class GetSum(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        old_text = self.view.substr(selection[0])

        r_str = r'(\d+\.\d*)|(\d*\.\d+)|(\d+)'
        r_str_p = re.compile(r_str)
        find_result = r_str_p.findall(old_text)

        a = []
        for t in find_result:
            a.append(max(t))

        sum_l = sum([float(i) for i in a])
        new_text = TAG + '\n'.join([str(a), str(sum_l), '\n'])
        self.view.insert(edit, max(selection[0].a, selection[0].b), new_text)


class ClearNone(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        region = sublime.Region(selection[0].a, selection[0].b)
        old_text = self.view.substr(selection[0])

        lines = old_text.split('\n')

        new_lines = [a for a in lines if a]

        self.view.replace(edit, region, '\n'.join(new_lines))


class ShiftVimModel(sublime_plugin.ApplicationCommand):
    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        current = s.get("ignored_packages", [])
        msg = ''
        vim_name = "Vintage"

        if vim_name in current:
            current.remove(vim_name)
            msg = 'Enable vim MODEL'
        else:
            current.append(vim_name)
            msg = 'Unable vim MODEL'

        s.set("ignored_packages", current)
        sublime.status_message(msg)

        sublime.save_settings("Preferences.sublime-settings")


class ShiftCamelOrUnderline(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        region = sublime.Region(selection[0].a, selection[0].b)
        old_text = self.view.substr(selection[0])

        # 下划线转驼峰
        if '_' in old_text:
            words = old_text.split('_')
            result = ''.join([word.capitalize() for word in words])

        # 驼峰转下划线
        else:
            result = ''
            if old_text[0].islower():
                result = old_text[0].upper() + old_text[1:]
            if old_text[0].isupper():
                for char in old_text:
                    if char.isupper() and not result:
                        result += char.lower()
                    elif char.isupper() and result:
                        result += '_' + char.lower()
                    else:
                        result += char
        self.view.replace(edit, region, result)


import threading
import requests
import json


DEFAULT_MODULE = 'azure-gpt-4'


class AskGpt(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.window = sublime.active_window()
        self.listener = SharedOutputPanelListener(
            window=self.window, markdown=True)
        self.out_file = r'D:\00work\GPT_OUT.md'

    def run(self, edit, panel_op='ask'):
        global DEFAULT_MODULE
        if panel_op == 'ask':
            thread = threading.Thread(target=self.request_gpt)
            thread.start()
        elif panel_op == 'just_show':
            self.listener.show_panel()
        elif panel_op == 'clear':
            self.listener.clear_output_panel()
        elif panel_op == 'shift_module':
            DEFAULT_MODULE = 'glm-4' if DEFAULT_MODULE == 'azure-gpt-4' else 'azure-gpt-4'
            sublime.status_message(f'>>>当前模型{DEFAULT_MODULE}<<<')

    def get_prompt(self):
        selection = self.view.sel()
        prompt = self.view.substr(selection[0])
        return prompt

    def output_panel(self, text):
        self.listener.update_output_panel(text)
        self.listener.refresh_output_panel()

    def output_panel_file(self, text, file_instance):
        self.output_panel(text)
        file_instance.write(text)

    def request_gpt(self):
        global DEFAULT_MODULE
        self.listener.show_panel()
        self.listener.toggle_overscroll(enabled=False)

        prompt = self.get_prompt()

        url = xxx
        payload = json.dumps(xxx)
        headers = xxx

        with open(self.out_file, 'a', encoding='utf-8') as out_file:
            self.output_panel_file("\n\n\n# 问题：" + prompt + '\n', out_file)
            self.output_panel(
                text=f"--------------------------开始请求{DEFAULT_MODULE}--------------------------\n\n")
            self.output_panel_file("## 回答：\n", out_file)
            with requests.request("POST", url, headers=headers, data=payload, stream=True) as response:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        self.output_panel_file(chunk.decode('utf-8'), out_file)

        sublime.set_timeout(self.output_panel(
            "\n\n\n--------------------------请求完成--------------------------"), 0)


CONTINUE_FLG = True


class Monitor(sublime_plugin.ApplicationCommand):
    # continue_flg = True
    pre_value = '0'

    def run(self, op='once'):
        global CONTINUE_FLG
        if op == 'once':
            self.fetch_data_my()
        if op == 'continue':
            CONTINUE_FLG = True
            thread = threading.Thread(target=self.fetch_loop)
            thread.start()
        if op == 'stop':
            CONTINUE_FLG = False

    def fetch_data(self):
        url = f"https://sqt.gtimg.cn/q=sh601012"
        response = requests.request("GET", url)
        if response.status_code == 200:
            msg = response.text.split('~')[3]
            sublime.status_message(f'>>>{msg}<<<')
        else:
            sublime.status_message(f'>>>Error fetching data<<<')

    def fetch_data_my(self):
        url = xxx
        try:
            response = requests.request("GET", url)
            if response.status_code == 200:
                msg = response.text
                tag = "🔺" if float(msg) > float(self.pre_value) else "🟢" if float(
                    msg) < float(self.pre_value) else "➖"
                sublime.status_message(f'>>>{tag}{msg}<<<')
                self.pre_value = msg
            else:
                sublime.status_message(f'>>>接口状态异常<<<')
        except Exception as e:
            sublime.status_message(f'>>>{e}<<<')

    def fetch_loop(self):
        global CONTINUE_FLG
        event = threading.Event()
        while CONTINUE_FLG:
            self.fetch_data_my()
            event.wait(5)
            t = datetime.datetime.now()
            if (t.hour == 11 and t.minute >= 30) or t.hour == 12 or t.hour >= 15:
                CONTINUE_FLG = False
