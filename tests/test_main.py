import random

from .test_sql_app import client


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


def test_factory():
    # 회원 등록
    member = test_create_member()
    # 회원 목록 검증
    test_read_members()
    # 회원 조회 검증
    test_read_member(member.get('id'))

    # 상품 등록
    product = test_create_product()
    # 상품 목록 검증
    test_read_products()
    # 상품 조회 검증
    test_read_product(product.get('id'))

    # 주문 - 주문 상품 등록
    order = test_create_order(member.get('id'), product.get('id'), product.get('price'), random.randint(1, 5))

    # 주문 조회 검증
    test_read_order(order.get('id'))
    # 주문 목록 검증
    test_read_orders()


def test_read_members():
    response = client.get("/members/")
    print(response.json())
    assert response.status_code == 200
    return response.json()


def test_read_member(member_id):
    response = client.get(f"/members/{member_id}")
    print(response.json())
    assert response.status_code == 200
    return response.json()


def test_create_member():
    params = {
        "name": "test119",
        "email": "test119@tt.com",
        "password": "hello!"
    }
    response = client.post("/members/", json=params)
    print(response.json())
    assert response.status_code == 200

    return response.json()


def test_read_orders():
    response = client.get("/orders/")
    print(response.json())
    assert response.status_code == 200


def test_read_order(order_id=1):
    response = client.get(f"/orders/{order_id}")
    print(response.json())
    assert response.status_code == 200


def test_create_order(member_id=1, product_id=1, order_product_price=100, order_product_cnt=1):
    params = {
        "order": {
            "title": f"종이컵 {order_product_cnt}개",
            "paid_price": order_product_price * order_product_cnt
        },
        "order_products": [
            {
                "title": "종이컵",
                "price": order_product_price,
                "total_price": order_product_price * order_product_cnt,
                "cnt": order_product_cnt,
                "product_id": product_id
            }
        ]
        # "title": f"종이컵 {order_product_cnt}개",
        # "status": "paid",
        # "paid_price": order_product_price * order_product_cnt,
        # "order_products": [
        #     {
        #         "title": "종이컵",
        #         "price": order_product_price,
        #         "total_price": order_product_price * order_product_cnt,
        #         "cnt": order_product_cnt,
        #         "status": "paid",
        #         "product_id": product_id
        #     }
        # ]
    }
    response = client.post(f"/members/{member_id}/orders/", json=params)
    print(response.json())
    assert response.status_code == 200

    return response.json()


def test_create_product():
    params = {
        "title": "종이컵",
        "description": "종이컵컵컵",
        "category": "생필품",
        "price": 3000,
        "is_active": True
    }
    response = client.post("/products/", json=params)
    print(response.json())
    assert response.status_code == 200

    return response.json()


def test_read_products():
    response = client.get(f"/products/")
    print(response.json())
    assert response.status_code == 200


def test_read_product(product_id=1):
    response = client.get(f"/products/{product_id}")
    print(response.json())
    assert response.status_code == 200
