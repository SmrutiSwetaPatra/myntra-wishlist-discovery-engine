def test_health_check(client):
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_wishlist(client):
    response = client.get("/api/wishlist/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 3

def test_get_product(client):
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "brand" in data

def test_analyze_decision(client):
    response = client.post("/api/decision/analyze", json={"product_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert "ai_summary" in data
    assert "recommendation" in data
    assert data["product_id"] == 1

def test_compare_products(client):
    response = client.post("/api/compare/", json={"product_ids": [1, 2]})
    assert response.status_code == 200
    data = response.json()
    assert "key_differences" in data
    assert "recommendation" in data
    assert data["product_ids"] == [1, 2]

def test_analytics_event(client):
    response = client.post("/api/analytics/events", json={
        "event_type": "wishlist_item_added",
        "user_id": 1,
        "product_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "wishlist_item_added"
    
    # Check insights
    insights = client.get("/api/analytics/insights")
    assert insights.status_code == 200
    assert len(insights.json()) > 0
