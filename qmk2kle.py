import json
import pprint as pp


qmk_src_json = 'de_ch-kyria-v3-new.json'
kle_dst_json = 'de_ch-kyria-v3-new.kle.json'


# src: https://mechanische-tastaturen.net/qmk-und-via-guide/qmk-via-keycodes-fuer-deutsche-zeichen/
MATCH_EN_DE_CH = {
    'KC_Z': 'Y',
    'KC_Y': 'Z',
    'KC_LBRC': 'Ü',
    'KC_SCLN': 'Ö',
    'KC_QUOT': 'Ä',
    'KC_DOT': '. :',
    'KC_COMM': ', ;',
    'KC_SLSH': '-_',
    'KC_TAB': "<i class='kb kb-Line-Start-End'></i>",
}


def prettify(qmk_keycode):
    i = ''
    if qmk_keycode == 'KC_RCTL':
        return (i, 'CTRL')
    elif qmk_keycode == 'KC_RCTL':
        return (i, 'CTRL')
    elif qmk_keycode == 'KC_LSFT':
        i = '&uArr;'
        return (i, 'Shift')

    if qmk_keycode == 'KC_TRNS':
        pass
    elif qmk_keycode == 'KC_NO':
        pass  # i = "<i class='fa fa-circle-o'></i>"
    elif qmk_keycode[:3] == 'KC_':
        if qmk_keycode in MATCH_EN_DE_CH.keys():
            i = MATCH_EN_DE_CH[qmk_keycode]
        elif len(qmk_keycode) == 4:
            i = qmk_keycode[3:4]
        else:
            print(qmk_keycode)
    else:
        print(qmk_keycode)
    return (i, )


KYRIA_MAP = [
    3, 8,
    2, 4, 7, 9,
    5, 6,
    0, 1, 10, 11,
    15, 20,
    14, 16, 19, 21,
    17, 18,
    12, 13, 22, 23,
    28, 37,
    26, 27, 35, 36,
    29, 34,
    24, 25, 38, 39
]

with open(qmk_src_json) as fp:
    parsed_data = json.load(fp)
    assert parsed_data['keyboard'] == "splitkb/kyria/rev3"
kle_layout_fname = parsed_data['keyboard'].replace('/', '') + '.json'
with open(kle_layout_fname) as fp:
    kle_data = json.load(fp)

layers = 4  # len(parsed_data['layers'])
for i, j in enumerate(KYRIA_MAP):
    key_codes = [prettify(parsed_data['layers'][layer][j])
                 for layer in range(layers)]
    key_code = "\n".join(key[0] for key in key_codes)
    try:
        key_code += "\n" + key_codes[0][1]
    except IndexError:
        pass  # It's not there

    k_cnt = 0
    for k1 in kle_data[1:]:
        for k2 in range(len(k1)):
            if isinstance(k1[k2], str):
                if k_cnt == i:
                    k1[k2] = key_code
                    k_cnt = 42_000  # break to outermost

                else:
                    k_cnt += 1


# pp.pprint(parsed_data['layers'])
# pp.pprint(kle_data)
print(len(parsed_data['layers']))

with open(kle_dst_json, 'w+') as fp:
    json.dump(kle_data, fp)
