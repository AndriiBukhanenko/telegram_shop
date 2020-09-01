

def clean_inf(descriprion):
    import re
    r = re.compile("[а-яА-Я -.,_0-9]+")
    russian = [w for w in filter(r.match, descriprion)]

    text = ''.join(russian)[:970] + '... (подробнее на нашем сайте)' if len(''.join(russian)) > 970 else ''.join(
        russian)

    if 'media' in descriprion:
        img = descriprion.split('media')
        if '.jpg' in descriprion:
            img = img[1].split('.jpg')
        if '.png' in descriprion:
            img = img[1].split('.png')
        img = ''.join([w for w in filter(r.match, img[0])])
        text = text.replace(img, "")
    text = text.replace('"', "")
    text = text.replace('_000_', "")
    text = text.replace(' . ', "")
    text = text.replace('- 18', "")
    text = text.replace('-', "")
    text = text.replace('....', "")
    text = text.replace(' 1.5 ', "")
    text = text.replace('  ', "")

    return text