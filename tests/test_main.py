"""Tests for the Pin Hill website endpoints."""
import pytest


def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Pin Hill" in response.text
    assert "Discover Pin Hill" in response.text


def test_history_page(client):
    """Test that the history page loads successfully."""
    response = client.get("/history")
    assert response.status_code == 200
    assert "History" in response.text
    assert "Harvard Conglomerate" in response.text


def test_trails_page(client):
    """Test that the trails page loads successfully."""
    response = client.get("/trails")
    assert response.status_code == 200
    assert "Trails" in response.text
    assert "Trail Information" in response.text


def test_static_file_references(client):
    """Test that static files are properly referenced in HTML."""
    response = client.get("/")
    assert response.status_code == 200
    # Check for static file references
    assert "/static/css/styles.css" in response.text
    assert "/static/js/script.js" in response.text
    assert "/static/images/" in response.text


def test_navigation_links(client):
    """Test that navigation links are present on all pages."""
    pages = ["/", "/history", "/trails"]
    
    for page in pages:
        response = client.get(page)
        assert response.status_code == 200
        # Check for navigation links
        assert 'href="/"' in response.text
        assert 'href="/history"' in response.text
        assert 'href="/trails"' in response.text


def test_404_page(client):
    """Test that non-existent pages return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
