import re

from app.main import app  # đổi đúng đường dẫn tới FastAPI app của bạn

CAMEL = re.compile(r"^[a-z][a-zA-Z0-9]*$")


def test_all_schema_fields_are_camel_case():
    schemas = app.openapi()["components"]["schemas"]
    bad = []
    for name, schema in schemas.items():
        for field in schema.get("properties", {}):
            if not CAMEL.match(field):
                bad.append(f"{name}.{field}")
    assert not bad, f"Field không phải camelCase: {bad}"
