
from models.base import Catalog
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.conftest import before


def test_empty_catalog(client: TestClient):
    resp = client.get('/catalog')

    assert resp.status_code == 200, resp.content

    payload = resp.json()
    assert len(payload['items']) == 0, payload


def test_catalog(dbsession: Session, client: TestClient):
    dbsession.add(
        Catalog(
            name='Jon Snow shirt',
            size='XL',
            color='black',
            price=19.99,
            brand='Winter',
            category='Is coming'
        )
    )
    dbsession.commit()
    resp = client.get('/catalog')

    assert resp.status_code == 200, resp.content

    payload = resp.json()
    assert len(payload['items']) == 1, payload

    item = payload['items'][0]

    assert item['name'] == 'Jon Snow shirt'
    assert item['size'] == 'XL'
    assert item['color'] == 'black'
    assert item['price'] == 19.99
    assert item['brand'] == 'Winter'
    assert item['category'] == 'Is coming'


def test_catalog_filter_name(dbsession: Session, client: TestClient):
    dbsession.add_all([
        Catalog(
            name='Jon Snow shirt',
            size='XL',
            color='black',
            price=19.99,
            brand='Winter',
            category='Is coming'
        ),
        Catalog(
            name='MKBHD',
            size='XL',
            color='black',
            price=39.99,
            brand='MKBHD',
            category='Category',
            created_at=before(hours=1)
        ),
        Catalog(
            name='MKBHD',
            size='L',
            color='black',
            price=39.99,
            brand='MKBHD',
            category='Category',
            created_at=before(hours=2)
        )
    ])
    dbsession.commit()
    resp = client.get("/catalog?name=MKBHD")

    assert resp.status_code == 200, resp.content

    payload = resp.json()
    assert len(payload['items']) == 2, payload

    first_item, second_item = payload['items']

    assert first_item['name'] == second_item['name'] == 'MKBHD'
    assert first_item['price'] == second_item['price'] == 39.99
    assert first_item['price'] == second_item['price'] == 39.99

    assert first_item['size'] == 'XL'
    assert second_item['size'] == 'L'


def test_catalog_filter_name_and_size(dbsession: Session, client: TestClient):
    dbsession.add_all([
        Catalog(
            name='Jon Snow shirt',
            size='XL',
            color='black',
            price=19.99,
            brand='Winter',
            category='Is coming'
        ),
        Catalog(
            name='MKBHD',
            size='XL',
            color='black',
            price=39.99,
            brand='MKBHD',
            category='Category',
        ),
        Catalog(
            name='MKBHD',
            size='L',
            color='black',
            price=39.99,
            brand='MKBHD',
            category='Category',
            created_at=before(hours=2)
        ),
        Catalog(
            name='MKBHD',
            size='L',
            color='gray',
            price=39.99,
            brand='MKBHD',
            category='Category',
            created_at=before(hours=3)
        )
    ])
    dbsession.commit()
    resp = client.get("/catalog?name=MKBHD&size=L")

    assert resp.status_code == 200, resp.content

    payload = resp.json()
    assert len(payload['items']) == 2, payload

    first_item, second_item = payload['items']

    assert first_item['name'] == second_item['name'] == 'MKBHD'
    assert first_item['price'] == second_item['price'] == 39.99
    assert first_item['price'] == second_item['price'] == 39.99

    assert first_item['size'] == second_item['size'] == 'L'

    assert first_item['color'] == 'black'
    assert second_item['color'] == 'gray'
