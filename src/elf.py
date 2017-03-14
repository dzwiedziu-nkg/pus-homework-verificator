import requests
from urllib.parse import urlencode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL_LOGIN = "https://elf2.pk.edu.pl/login/index.php"
URL_VIEW = "http://elf2.pk.edu.pl/mod/assign/view.php"

URL_INDICES = "http://elf2.pk.edu.pl/mod/assign/view.php?id=47093&action=grading"
URL_CONFIRMATIONS = "http://elf2.pk.edu.pl/mod/assign/view.php?id=47097&action=grading"

URL_GESTURES = "http://elf2.pk.edu.pl/mod/choice/report.php?id=50176"
URL_GESTURES_TXT = "http://elf2.pk.edu.pl/mod/choice/report.php"

DOCUMENTATIONS = {
    1: 47098,
    2: 47100,
    3: 47102,
    4: 47105,
    7: 47108,
    8: 47110,
    9: 47112,
    11: 47115,
    12: 47117
}

SOURCES = {
    1: 47119,
    2: 47121,
    3: 47123,
    4: 47104,
    7: 47129,
    8: 47131,
    9: 47133,
    11: 47136,
    12: 47138
}


class Elf:
    def __init__(self):
        self.session = requests.session()

    def logon(self, login, password):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        params = {'anchor': '', 'username': login, 'password': password, 'rememberusername': 1}
        self.session.post(URL_LOGIN, urlencode(params), headers=headers, verify=False)

    def get_view_page(self, element_id):
        params = {'id': element_id, 'action': 'grading'}
        r = self.session.get(URL_VIEW + "?" + urlencode(params))
        return r.text

    def parse_view_page(self, content, homeworks, lab, kind):
        c = content.replace("\n", "")
        for h in homeworks:
            for s in h['students']:
                result = re.search(s['forename'] + '(.*?)' + s['lastname'] + '</a>(.*?)</tr>', c, re.IGNORECASE)
                if result is None:
                    s[kind][lab] = '?'
                else:
                    row = result.group(2)
                    if re.search('Brak przesłanego zadania', row, re.IGNORECASE):
                        s[kind][lab] = '-'
                    elif kind == 'doc':
                        pdf = re.search('\.pdf', row, re.IGNORECASE)
                        if pdf:
                            s[kind][lab] = '\'+'
                        else:
                            s[kind][lab] = '-'
                    elif kind == 'src':
                        zip = re.search('\.zip', row, re.IGNORECASE)
                        if zip:
                            s[kind][lab] = '\'+'
                        else:
                            s[kind][lab] = '-'

    def get_indices(self, students):
        content = self.session.get(URL_INDICES)
        c = content.text.replace("\n", "")
        for h in students:
            for s in h['students']:
                result = re.search(s['forename'] + '(.*?)' + s['lastname'] + '</a>(.*?)</tr>', c, re.IGNORECASE)
                if result is None:
                    s['index'] = '?'
                else:
                    row = result.group(2)
                    r = re.search('<div class="no-overflow"><p>([0-9]+)', row)
                    if r:
                        s['index'] = r.group(1)
                    else:
                        s['index'] = '-'

    def get_confirmation(self, students):
        content = self.session.get(URL_CONFIRMATIONS)
        c = content.text.replace("\n", "")
        for h in students:
            for s in h['students']:
                result = re.search(s['forename'] + '(.*?)' + s['lastname'] + '</a>(.*?)</tr>', c, re.IGNORECASE)
                if result is None:
                    s['confirmation'] = '?'
                else:
                    row = result.group(2)
                    r = re.search('<div class="no-overflow"><p>Przyjmuję do wiadomości informacje zawarte w syllabusie, zasadach oceniania oraz opisie przebiegu laboratorium. Potwierdzam także swoje \.\.\.', row)
                    if r:
                        s['confirmation'] = '\'+'
                    else:
                        s['confirmation'] = '-'

    def get_gesture(self, students):
        c = self.session.get(URL_GESTURES).text
        sesskey = re.search('"sesskey":"(.*?)"', c).group(1)

        params = {'sesskey': sesskey, 'id': '50176', 'download': 'txt'}
        form = urlencode(params)
        txt = self.session.post(URL_GESTURES_TXT, params).text

        for h in students:
            for s in h['students']:
                result = re.search(s['lastname'] + '(.*?)' + s['forename'] + '(.*?)PUS (\d\d) -', txt, re.IGNORECASE)
                if result:
                    s['gesture_lab'] = int(result.group(3))

    @staticmethod
    def math_pairs(homeworks):
        for h in homeworks:
            for i in range(0, len(h['students'])):
                current = h['students'][i]
                pair = None
                if i % 2:
                    pair = h['students'][i - 1]
                elif i + 1 != len(h['students']):
                    pair = h['students'][i + 1]

                if pair is not None:
                    for k in DOCUMENTATIONS.keys():
                        for d in ['doc', 'src']:
                            if current[d][k] != '-' and current[d][k] != '?':
                                pair[d][k] = current[d][k]

    def get_homeworks(self, homeworks):
        for k in DOCUMENTATIONS.keys():
            print('Import list of documentations of PUS ' + str(k) + ' from ELF3...', end='', flush=True)
            self.parse_view_page(self.get_view_page(DOCUMENTATIONS[k]), homeworks, k, 'doc')
            print(' done')

            print('Import list of source codes of PUS ' + str(k) + ' from ELF3...', end='', flush=True)
            self.parse_view_page(self.get_view_page(SOURCES[k]), homeworks, k, 'src')
            print(' done')
        Elf.math_pairs(homeworks)
        return homeworks
