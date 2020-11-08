import time
import os
import shutil
from ipydex import IPS
from splinter import Browser

import glob


from ipydex import IPS, activate_ips_on_exception
activate_ips_on_exception()


url = "https://bramp.github.io/js-sequence-diagrams/"

download_path = f"{os.environ['HOME']}/Downloads"


# splinter:

d = dict()
d['loggingPrefs'] = {'browser': 'ALL'}
options_for_browser = dict(driver_name='chrome', headless=False, desired_capabilities=d)



class JS_Diagram_Converter(object):
    def __init__(self):
        self.browser = None

    def _init(self):
        self.browser = Browser(**options_for_browser)

        self.browser.visit(url)

    def convert_diagram(self, source):

        if self.browser is None:
            self._init()

        s = self.browser.find_by_xpath('//select')[0]
        s.select_by_text("Simple")


        a = self.browser.find_by_text("Download as SVG")[0]

        # writing to the textarea is a bit clumsy
        ta = self.browser.find_by_xpath('//textarea')[0]

        # select all text
        snippet1 = f"""document.querySelector("textarea").focus()"""
        snippet2 = f"""document.querySelector("textarea").select()"""
        self.browser.execute_script(snippet1)
        self.browser.execute_script(snippet2)

        # insert some dummy text
        # ta.fill("S1 -> S2: test")
        # select again
        # self.browser.execute_script(snippet)

        # now insert the actual source (unfortunately this is slow to simulate typing)
        ta.fill(source)
        s.select_by_text("Simple")

        time.sleep(2)

        a.click()

    def quit(self):

        if not self.browser is None:
            self.browser.quit()
            self.browser = None


def get_all_src():
    fnames = glob.glob("diagram_*.md")

    res = dict()

    for fname in fnames:
        with open(fname, "r") as file_:
            src = file_.read()

        src = src.replace("```sequence\n", "\n").replace("```\n", "\n")

        res[fname] = src


    return res

jdc = JS_Diagram_Converter()
def convert(fname, source):

    jdc.convert_diagram(source)

    d_path = os.path.join(download_path, "diagram.svg")
    dst_path = os.path.join(".", fname.replace(".md", ".svg"))


    for i in range(10):
        time.sleep(1)
        try:
            shutil.move(d_path, dst_path)
        except FileNotFoundError:
            continue
        else:
            break


res = list(get_all_src().items())
# res = list(get_all_src().items()); convert(*res[0])

IPS()

jdc.quit()

