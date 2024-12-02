from dataclasses import asdict
from typing import List

import asyncpg
from asyncpg import Connection, UniqueViolationError
from quart import g, abort

from model.cards import Card, CardInput, CardAlreadyExistsException


async def get_cards(connection: Connection) -> List[Card]:
    results = await connection.fetch_all(
        """
        SELECT * FROM cards;
        """
    )
    return [Card(**result) for result in results]


async def get_card(card_id: int, connection: Connection) -> Card | None:
    result = await connection.fetch_one(
        """
        SELECT * 
          FROM cards 
        WHERE id = :id;
        """,
        {"id": card_id},
    )
    return Card(**result) if result else None


async def create_card(data: CardInput, connection: Connection) -> Card:
    try:
        result = await connection.fetch_one(
            """
        INSERT INTO cards 
          (question, answer)
        VALUES 
          (:question, :answer)
        RETURNING id, question, answer
        """,
            asdict(data),
        )
        return Card(**result)
    except asyncpg.PostgresError as e:
        if type(e) == UniqueViolationError:
            raise CardAlreadyExistsException(data.question)
        else:
            raise e


async def update_card(
    card_id: int, card_input: CardInput, connection: Connection
) -> Card | None:
    result = await connection.fetch_one(
        """
        UPDATE cards 
           SET question = :question, 
               answer   = :answer
         WHERE id       = :id
        RETURNING id, question, answer
        """,
        {"id": card_id, "question": card_input.question, "answer": card_input.answer},
    )

    return Card(**result) if result else None


async def delete_card(card_id: int, connection: Connection) -> Card | None:
    card = await connection.fetch_one(
        """
            DELETE FROM cards
             WHERE id = :id;
            """,
        {"id": card_id},
    )
    return card
