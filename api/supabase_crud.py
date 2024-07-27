
import os
from supabase import create_client, Client
from fastapi import HTTPException

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

class ItemCRUD:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def create_item(self, item: Item):
        response = self.supabase.table("items").insert(item.dict()).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return response.data[0]

    def read_item(self, item_id: int):
        response = self.supabase.table("items").select("*").eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]

    def update_item(self, item_id: int, item: Item):
        response = self.supabase.table("items").update(item.dict()).eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return response.data[0]

    def delete_item(self, item_id: int):
        response = self.supabase.table("items").delete().eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return {"message": "Item deleted successfully"}