from typing import List

from quart import Quart, g, abort
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response

from config.conf import DB_URL
from model.cards import CardInput, Card, CardAlreadyExistsException
from server.api.cards import create_card, get_card, get_cards, update_card, delete_card

app = Quart(__name__)
QuartDB(app=app, url=DB_URL)
QuartSchema(app)


@app.get("/cards")
async def get() -> List[Card]:
    return await get_cards(g.connection)


@app.get("/cards/<int:card_id>")
async def get_one(card_id: int) -> Card | None:
    result = await get_card(card_id, g.connection)
    if not result:
        abort(404)
    return result


@app.post("/cards")
@validate_request(CardInput)
@validate_response(Card)
async def post(data: CardInput) -> Card | None:
    try:
        return await create_card(data, g.connection)
    except CardAlreadyExistsException as e:
        abort(409, e)


@app.put("/cards/<int:card_id>")
@validate_request(CardInput)
@validate_response(Card)
async def put(card_id: int, data: CardInput) -> Card | None:
    result = await update_card(card_id, data, g.connection)
    if not result:
        abort(404)
    return result


@app.delete("/cards/<int:card_id>")
async def delete(card_id: int) -> Card | None:
    result = await delete_card(card_id, g.connection)
    if not result:
        abort(404)
    return result
