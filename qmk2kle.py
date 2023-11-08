import json


qmk_src_json = 'de_ch-kyria-v3-new.json'
kle_dst_json = 'de_ch-kyria-v3-new.kle.json'


def prettify(qmk_keycode):
    i = ''
    if qmk_keycode[:3] == 'KC_':
        if len(qmk_keycode) == 4:
            i = qmk_keycode[3:4]
    return i + "\n"


KYRIA_MAP = [
    3, 8
]

with open(qmk_src_json) as fp:
    parsed_data = json.load(fp)
    assert parsed_data['keyboard'] == "splitkb/kyria/rev3"
kle_layout_fname = parsed_data['keyboard'].replace('/', '') + '.json'
with open(kle_layout_fname) as fp:
    kle_data = json.load(fp)

layers = len(parsed_data['layers'])
for i, j in enumerate(KYRIA_MAP):
    key_code = ""
    for layer in range(layers):
        key_code += prettify(parsed_data['layers'][layer][j])
    print(key_code)

    k_cnt = 0
    for k1 in kle_data[1:]:
        for k2 in range(len(k1)):
            if isinstance(k1[k2], str):
                if k_cnt == i:
                    k1[k2] = key_code
                    k_cnt = 42_000

                else:
                    k_cnt += 1


#import pprint as pp
#pp.pprint(parsed_data['layers'])
#pp.pprint(kle_data)
#print(len(parsed_data['layers']))

with open(kle_dst_json, 'w+') as fp:
    json.dump(kle_data, fp)
