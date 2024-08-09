
#all This file contains the CRUD operations for the Item model using Supabase

import os
from supabase import create_client, Client
from fastapi import HTTPException

#all Import the keys from the .env file
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

#all: Import the Item model
supabase: Client = create_client(url, key)


#all: Import the Item model
class ItemCRUD:
    def __init__(self, supabase_client):
        self.supabase = supabase_client


    #! Create the item
    def create_item(self, item: Item):
        response = self.supabase.table("items").insert(item.dict()).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return response.data[0]

    #! Read all items
    def read_item(self, item_id: int):
        response = self.supabase.table("items").select("*").eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        return response.data[0]

    #! Update the item
    def update_item(self, item_id: int, item: Item):
        response = self.supabase.table("items").update(item.dict()).eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return response.data[0]

    #! Delete the item
    def delete_item(self, item_id: int):
        response = self.supabase.table("items").delete().eq("id", item_id).execute()
        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)
        return {"message": "Item deleted successfully"}