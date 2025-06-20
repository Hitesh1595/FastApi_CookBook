from contextlib import asynccontextmanager
from app.db_connection import (
    ping_mongo_db_server,
    ping_elasticsearch_server,
    ping_redis_server
)
from app import third_point_endpoint
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from app import main_search



@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_mongo_db_server(),
    await ping_elasticsearch_server()
    await ping_redis_server()
    db = mongo_database()
    # creating indexin mongo db
    await db.songs.create_index({"album.release_year": -1})
    await db.songs.create_index({"artist": "text"})
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(third_point_endpoint.router)
app.include_router(main_search.router)

from bson import ObjectId
from fastapi import Body, Depends
from app.database import mongo_database
from fastapi.encoders import ENCODERS_BY_TYPE


ENCODERS_BY_TYPE[ObjectId] = str


@app.post("/song")
async def add_song(
    song: dict = Body(
        example={
            "title": "My Song",
            "artist": "My Artist",
            "genre": "My Genre",
        },
    ),
    mongo_db=Depends(mongo_database),
):
    await mongo_db.songs.insert_one(song)

    return {
        "message": "Song added successfully",
        "id": song.get("_id"),
    }

@app.get("/songs")
async def get_songs(
    db=Depends(mongo_database),
):
    songs = await db.songs.find().to_list(None)
    return songs



@app.get("/song/{song_id}")
async def get_song(song_id: str, db=Depends(mongo_database)):
    song = await db.songs.find_one(
        {
            "_id": ObjectId(song_id) if ObjectId.is_valid(song_id) else None
        }
    )
    if not song:
        raise HTTPException(
            status_code=404, detail="Song not found"
        )
    return song



@app.put("/song/{song_id}")
async def update_song(
    song_id: str,
    updated_song: dict,
    db=Depends(mongo_database),
):
    result = await db.songs.update_one(
        {
            "_id": ObjectId(song_id) if ObjectId.is_valid(song_id) else None
        },
        {"$set": updated_song},
    )
    if result.modified_count == 1:
        return {"message": "Song updated successfully"}

    raise HTTPException(
        status_code=404, detail="Song not found"
    )


@app.delete("/song/{song_id}")
async def delete_song(song_id: str, db=Depends(mongo_database)):
    result = await db.songs.delete_one(
        {
            "_id": ObjectId(song_id) if ObjectId.is_valid(song_id) else None
        }
    )
    if result.deleted_count == 1:
        return {"message": "Song deleted successfully"}

    raise HTTPException(
        status_code=404, detail="Song not found"
    )


class Playlist(BaseModel):
    name: str
    songs: list[str] = []



@app.post("/playlist")
async def create_playlist(
    playlist: Playlist = Body(
        example={
            "name": "My Playlist",
            "songs": ["song_id"],
        }
    ),
    db=Depends(mongo_database),
):
    result = await db.playlists.insert_one(
        playlist.model_dump()
    )
    return {
        "message": "Playlist created successfully",
        "id": str(result.inserted_id),
    }



@app.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str, db=Depends(mongo_database)):
    playlist = await db.playlists.find_one(
        {
            "_id": ObjectId(playlist_id) if ObjectId.is_valid(playlist_id) else None
        }
    )
    if not playlist:
        raise HTTPException(
            status_code=404, detail="Playlist not found"
        )

    songs = await db.songs.find(
        {
            "_id": {
                "$in": [
                    ObjectId(song_id) for song_id in playlist["songs"]
                ]
            }
        }
    ).to_list(None)

    return {"name": playlist["name"], "songs": songs}


from app.db_connection import logger

# The explained_query variable holds information about the query
# such as the query execution
# or index used for the search.

@app.get("/songs/year")
async def get_songs_by_released_year(
    year: int,
    db=Depends(mongo_database),
):
    query = db.songs.find({"album.release_year": year})
    explained_query = await query.explain()
    logger.info(
        "Index used: %s",
        explained_query.get("queryPlanner", {})
        .get("winningPlan", {})
        .get("inputStage", {})
        .get("indexName", "No index used"),
    )

    songs = await query.to_list(None)
    return songs


@app.get("/songs/artist")
async def get_songs_by_artist(
    artist: str, db=Depends(mongo_database)
):
    query = db.songs.find(
        {"$text": {"$search": artist}}
    )
    explained_query = await query.explain()
    logger.info(
        "Index used: %s",
        explained_query.get("queryPlanner", {})
        .get("winningPlan", {})
        .get("indexName", "No index used"),
    )

    songs = await query.to_list(None)
    return songs
