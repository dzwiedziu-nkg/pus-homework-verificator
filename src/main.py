from pus import Pus
from elf import Elf
from credentials import ELF_LOGIN, ELF_PASSWORD

if __name__ == "__main__":
    pus = Pus()

    print('Import list form Google Sheet...', end='', flush=True)
    homeworks = pus.get_homeworks()
    print(' done')

    elf = Elf()
    elf.logon(ELF_LOGIN, ELF_PASSWORD)
    elf.get_homeworks(homeworks)

    pus.update_sheet(homeworks)

    elf.get_gesture(homeworks)
    elf.get_indices(homeworks)
    elf.get_confirmation(homeworks)

    pus.update_gestures(homeworks)

    print('done')
