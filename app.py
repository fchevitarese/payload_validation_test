from flask import request
from marshmallow import ValidationError

from schemas.apolice_schema import Payload1Schema, Payload2Schema

from tasks import validate_house_payload, validate_car_payload

from rq import Queue
from redis import Redis

from app_instance import create_app

app = create_app()

redis_conn = Redis(host="redis", port=6379)

queues = {
    "house": Queue("house_payload", connection=redis_conn),
    "car": Queue("car_payload", connection=redis_conn),
}


@app.route("/payload", methods=["POST"])
def handle_payload():
    payload = request.get_json()

    try:
        if not payload:
            return {"error": "Empty payload"}, 400

        if "item" not in payload:
            raise ValidationError("Item é um campo obrigatório")

        is_house_payload = False
        if "endereço" in payload["item"]:
            schema = Payload1Schema()
            is_house_payload = True
        else:
            schema = Payload2Schema()

        validated_payload = schema.load(payload)
        if is_house_payload:
            q = queues.get("house")
            job = q.enqueue(validate_house_payload, validated_payload)
        else:
            q = queues.get("car")
            job = q.enqueue(validate_car_payload, validated_payload)

        return {"message": f"Payload enqueued successfully - Job id {job.id}"}
    except ValidationError as err:
        return {"error": err.messages}, 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
