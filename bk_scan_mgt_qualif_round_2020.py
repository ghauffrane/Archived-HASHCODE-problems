PATH = 'E:/HASH CODE/2020/2020/Hash Code 2020 - Online Qualification Round/a_example.txt'


def get_input(path):
    input_file = open(path, 'r')
    lines = input_file.readlines()
    l_contt = [lines[0][i] for i in range(0, len(lines[0])) if lines[0][i].isdigit()]
    b, l, tot_scan_days = l_contt
    S = list((lines[1].replace('\n', '')).replace(' ', ''))
    lib_info = []
    for i in range(2, len(lines), 2):
        d = dict()
        l_1 = lines[i].replace('\n', '').replace(' ', '')
        l_2 = lines[i + 1].replace('\n', '').replace(' ', '')
        d['lib_id'] = int(0.5 * i - 1)
        d['lib_total_bks'] = l_1.strip()[0]
        d['singup days'] = l_1.strip()[1]
        d['ship bks per day'] = l_1.strip()[2]
        d['lib_bks_ids'] = list(l_2.strip())

        lib_info.append(d)

    return b, l, tot_scan_days, S, lib_info


B, L, D, scores, librarys = get_input(PATH)
