from pydantic import BaseModel, Field




class PostDetailsTraveler(BaseModel):
    passport_id: str = Field(
        min_length=7,
        max_length=50,

        description= "passport_id must be valid dude!/ karen!"
    )







class GetDetailsTraveler(BaseModel):
    pass




class GetPastRecord(BaseModel):
    pass



class PostCheckPostEvents(BaseModel):
    pass




class GetCheckPostEvents(BaseModel):
    pass



