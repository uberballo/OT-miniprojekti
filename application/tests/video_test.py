import pytest
import re
from application import db
from application.videos.models import Video


def test_new_video_page_works(client, app):
    assert client.get("/videos/new/").status_code == 200


def test_create_video_form_works(client, app):
    client.post(
        "/videos/",
        data={"url": "https://www.youtube.com/watch?v=c87FAvVSgJo"})

    with app.app_context():
        video = Video.query.first()
        assert video.title == "It's pizza time!"


def test_create_video_form_prevent_wrong_url(client, app):
    response = client.post(
        "/videos/",
        data={"url": "https://www.youtube.com/watch?v=c87"},
        follow_redirects=True)

    assert b"Wrong url, url must be typed like" in response.data


def test_remove_video_works(client, app):
    client.post(
        "/videos/",
        data={"url": "https://www.youtube.com/watch?v=c87FAvVSgJo"})

    with app.app_context():
        video_to_remove = Video.query.first()
        assert Video.query.count() == 1

        response = client.post(
            f"/videos/remove/{video_to_remove.id}",
            follow_redirects=True)

        assert b"List of videos" in response.data
        assert Video.query.count() == 0
