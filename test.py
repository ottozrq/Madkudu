import requests, json


def test(file_name):
    url = 'http://localhost:5000'
    f = open(file_name, 'r')
    j = json.loads(f.read())
    uid = j['user_id']
    reqs = j['requests']
    resp = j['response']
    for req in reqs:
        r = requests.post(url + '/v1/page', json=req)
        assert json.loads(r.text)['result'] is True
    r_res = requests.get(url + '/v1/user/' + uid)
    assert json.loads(r_res.text) == resp
    r_del = requests.delete(url + '/v1/user/' + uid)
    assert json.loads(r_del.text)['result'] is True


if __name__ == '__main__':
    test('test1.json')
    test('test2.json')
    print('----- All Tests are passed -----')
