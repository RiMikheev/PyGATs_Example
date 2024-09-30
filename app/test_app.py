import pytest

import app

@pytest.fixture
def client():
  return app.app.test_client()

def test_root(client):
  response = client.get("/")
  assert b'doctype html' in response.data

def test_form(client):
  name = "my_super_test"
  response = client.get("/", query_string={"name": name})
  assert name.encode() in response.data

def test_admin(client):
  response = client.get("/admin")
  assert b'DOCTYPE html' in response.data

@pytest.mark.parametrize('f, l, u, e, a', [('', '', '', '', ''),
                                           ('admin', '', '', '', ''),
                                           ('', 'admin', '', '', ''),
                                           ('', '', 'admin', '', ''),
                                           ('', '', '', 'admin', ''),
                                           ('', '', '', '', 'admin')])
def test_admin_bad_form(client, f, l, u, e, a):
  data = {'firstname' : f,
          'lastname' : l,
          'username' : u,
          'email' : e,
          'addres' : a}
  response = client.post("/admin", data=data)
  assert 'Ошибка'.encode() in response.data

def test_admin_form(client):
  data = {'firstname' : 'Roman',
          'lastname' : 'Mikheev',
          'username' : 'RIMikheev',
          'email' : 'mixeew.roman2000@mail.ru',
          'addres' : 'Sarov'}
  response = client.post("/admin", data=data)
  assert 'Запись сделана'.encode() in response.data
