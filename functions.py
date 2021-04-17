import re
import ujson
import urllib.parse


def editData(id_name, newData):
    try:
        file = open('data.json', 'r')
        try:
            data = ujson.loads(file.readline())
        except:
            data = {}
        data[id_name] = newData

        file.close()
        file = open('data.json', 'w')

        file.writelines(ujson.dumps(data))
        file.close()

        return True
    except:
        return False


def getData(id_name):
    try:
        file = open('data.json')
        data = ujson.loads(file.readline())

        return data[str(id_name)]
    except:
        return None


def getUserId(scheme):
    try:
        parse = urllib.parse.urlparse(scheme).path
        if scheme is not parse:
            parse = str(parse)
            return parse if parse[1] != "/" else parse[1:]

        reg = re.findall(r'\[id(\d*)\|.*]', scheme)[0]
        if reg is not None:
            return reg

        return scheme
    except:
        return scheme