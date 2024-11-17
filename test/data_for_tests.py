REQUEST_SET = [
    ("http://www.example.com", {"id": 1}, "etag1", '{"hello": "world"}'),
    ("http://www.goggles.com", {"course_id": 2}, "etag2", '{"id": 2}'),
    (
        "http://www.giggle.com",
        {"course_id": 666},
        "etag3",
        "<html><p>Hello World!</p></html>",
    ),
    ("http://www.goggles.com", None, "etag4", '{"id": 2}'),
]
