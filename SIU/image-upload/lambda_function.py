import json
import os
import re
import uuid
from datetime import datetime, timezone

import boto3
from botocore.config import Config

BUCKET = os.environ["BUCKET"]
TABLE = os.environ["TABLE"]
REGION = os.environ.get("AWS_REGION")
ALLOWED = {"image/jpeg", "image/png", "image/gif", "image/webp"}

s3 = boto3.client("s3", region_name=REGION, endpoint_url=f"https://s3.{REGION}.amazonaws.com", config=Config(signature_version="s3v4"))
table = boto3.resource("dynamodb").Table(TABLE)


def reply(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def create_upload(event):
    try:
        data = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return reply(400, {"error": "Body must be valid JSON"})

    filename = data.get("filename")
    content_type = data.get("contentType")
    if not filename or content_type not in ALLOWED:
        return reply(400, {"error": "Need filename and contentType (jpeg, png, gif or webp)"})

    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename)[:100]
    image_id = str(uuid.uuid4())
    key = f"uploads/{image_id}-{safe_name}"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=300,
    )

    table.put_item(Item={
        "imageId": image_id,
        "key": key,
        "filename": safe_name,
        "contentType": content_type,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    })

    return reply(200, {"imageId": image_id, "uploadUrl": upload_url, "expiresIn": 300})


def list_images(event):
    items = table.scan().get("Items", [])
    items.sort(key=lambda i: i.get("createdAt", ""), reverse=True)
    for item in items:
        item["url"] = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": item["key"]},
            ExpiresIn=300,
        )
    return reply(200, {"images": items})


def handler(event, context):
    route = event.get("routeKey")
    try:
        if route == "POST /upload":
            return create_upload(event)
        if route == "GET /images":
            return list_images(event)
        return reply(404, {"error": "Not found"})
    except Exception as exc:
        print("ERROR:", repr(exc))
        return reply(500, {"error": "Internal error"})
