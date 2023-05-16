import re
# import sys
# import json
import datetime
import sublime
import sublime_plugin
from .ErlendTRS import baidu_translate_api as my_trans


TAG = '\n' + ('-' * 10) + '\n'


def get_trans_result(r_str):
    """
    TODO 异常处理
    """
    text = []
    for i in r_str['trans_result']:
        text.append(i['dst'])
    return '\n'.join(text) + '\n'


class TransToEnglish(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        old_text = self.view.substr(selection[0])

        query = old_text

        from_lang = 'auto'
        to_lang = 'en'

        r_str = my_trans(from_lang, to_lang, query)

        new_text = TAG + get_trans_result(r_str)
        self.view.insert(edit, max(selection[0].a, selection[0].b), new_text)


class TransToChinese(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        old_text = self.view.substr(selection[0])

        query = old_text

        from_lang = 'auto'
        to_lang = 'zh'

        r_str = my_trans(from_lang, to_lang, query)

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

        if current:
            current = []
            msg = 'Enable vim MODEL'
        else:
            current = ["Vintage"]
            msg = 'Unable vim MODEL'

        s.set("ignored_packages", current)
        sublime.status_message(msg)

        sublime.save_settings("Preferences.sublime-settings")
