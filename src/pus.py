from sheet import Sheet
from elf import DOCUMENTATIONS

PUS_SHEET_ID = '15Jc3cvqTF0jlyMwx12DrIR-tXzoeYmntjx4BtMBReDs'
GROUPS = 6
START_ROW = 1
GROUP_ROWS = 3+18
LABS = DOCUMENTATIONS.keys()
LABS_ROWS = {1: 'AA', 2: 'AB', 3: 'AC', 4: 'AD', 7: 'AE', 8: 'AF', 9: 'AG', 11: 'AH', 12: 'AI'}


class Pus:
    def __init__(self):
        self.sheet = Sheet(PUS_SHEET_ID)
        #self.sheet.update_cell('AB6', 'test')

    def get_groups(self):
        groups = []
        values = self.sheet.get_values('B:B')
        for i in range(0, GROUPS):
            groups.append(values[i*GROUP_ROWS + START_ROW][0])
        return groups

    def get_homeworks(self):
        names = self.sheet.get_values('A:C')
        homeworks = self.sheet.get_values('AA:AI')

        values = []
        for i in range(0, GROUPS):
            group = {}
            students = []
            group['name'] = names[i*GROUP_ROWS + START_ROW][1]
            for j in range(0, 18):
                row = i * GROUP_ROWS + START_ROW + 2 + j
                if len(names[row]) > 1:
                    homes = {}
                    k_pos = 0
                    for k in LABS:
                        if len(homeworks) > row and len(homeworks[row]) > k_pos:
                            homes[k] = homeworks[row][k_pos]
                        else:
                            homes[k] = None
                        k_pos += 1
                    students.append({
                        'forename': names[row][1].strip(),
                        'lastname': names[row][2].strip(),
                        'homeworks': homes,
                        'doc': {},
                        'src': {}})
            group['students'] = students
            values.append(group)
        return values

    def update_sheet(self, homeworks):
        h_nr = 0
        for h in homeworks:
            print('Group: ' + h['name'])
            for i in range(0, len(h['students'])):
                current = h['students'][i]
                print('  Student: ' + str(i + 1) + ". " + current['forename'] + ' ' + current['lastname'], end='', flush=True)
                row_nr = START_ROW + 1 + h_nr * GROUP_ROWS + 2 + i

                for l in LABS:
                    hw = current['homeworks'][l]
                    v = hw
                    if not hw or hw == '-' or hw == '?' or hw == 'o' or hw == '+' or hw == '\'+':
                        v = current['doc'][l]
                        cell = LABS_ROWS[l] + str(row_nr)
                        annotation = None
                        if v != '-' and current['src'][l] == '-':
                            v = 'o'
                            annotation = 'Brak kodów źródłowych'
                        if v == '+':
                            v = '\'+'
                        if hw == '+':
                            hw = '\'+'
                        if v != hw:
                            self.sheet.update_cell(cell, v)
                    print(' ' + v, end='', flush=True)
                print('')
            print('')
            h_nr += 1

    def update_gestures(self, homeworks):
        h_nr = 0

        part_parsed = {}
        participant = self.sheet.get_values('Gesty!B3:B')
        filled = self.sheet.get_values('AX:BA')
        for p in participant:
            pp = p[0].split(' ')
            if len(pp) and pp[0].isdigit():
                part_parsed[int(pp[0])] = 1

        for h in homeworks:
            print('Group: ' + h['name'])
            for i in range(0, len(h['students'])):
                current = h['students'][i]
                if current['lastname'] == 'GRUSZCZYŃSKA':
                    print("jest")
                print('  Student: ' + str(i + 1) + ". " + current['forename'] + ' ' + current['lastname'], end='', flush=True)
                row_nr = START_ROW + 1 + h_nr * GROUP_ROWS + 2 + i

                ax = '-'
                ay = '-'
                az = '-'
                ba = ''
                if 'gesture_lab' in current:
                    ba = current['gesture_lab']

                if current['index'].isdigit():
                    ax = '\'+'
                    #self.sheet.update_cell('AX%d' % row_nr, '\'+')
                    if int(current['index']) in part_parsed:
                        az = '\'+'
                        #self.sheet.update_cell('AZ%d' % row_nr, '\'+')
                    #else:
                        #self.sheet.update_cell('AZ%d' % row_nr, '-')
                #else:
                    #self.sheet.update_cell('AX%d' % row_nr, '-')
                    #self.sheet.update_cell('AZ%d' % row_nr, '-')

                #self.sheet.update_cell('AY%d' % row_nr, current['confirmation'])
                ay = current['confirmation']

                if len(filled) <= row_nr or len(filled[row_nr - 1]) < 1 or ax.replace('\'', '') != filled[row_nr - 1][0]:
                    self.sheet.update_cell('AX%d' % row_nr, ax)
                if len(filled) <= row_nr or len(filled[row_nr - 1]) < 2 or ay.replace('\'', '') != filled[row_nr - 1][1]:
                    self.sheet.update_cell('AY%d' % row_nr, ay)
                if len(filled) <= row_nr or len(filled[row_nr - 1]) < 3 or az.replace('\'', '') != filled[row_nr - 1][2]:
                    self.sheet.update_cell('AZ%d' % row_nr, az)
                if len(filled) <= row_nr or len(filled[row_nr - 1]) < 4 or ba != int(filled[row_nr - 1][3]):
                    #if len(filled[row_nr - 1]) >= 4:
                    self.sheet.update_cell('BA%d' % row_nr, ba)

                print('')

            print('')
            h_nr += 1
