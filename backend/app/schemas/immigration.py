from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict




class TravelerIn(BaseModel):
    passport_id: str = Field(
        min_length=7,
        max_length=50,

        description= "passport_id must be valid dude!/ karen!.  e.g. GBP-874221X"
    )

     
    nationality: str = Field(
        min_length=2,
        max_length=30,
        description="Country of citizenship. e.g. British, Russian"
    )

    full_name: str = Field(
        min_length=2,
        max_length=50,
        description="Full name as on passport"
    )


    date_of_birth: date = Field(
        # date not datetime — birth date has no time component
        description="DOB. Format: YYYY-MM-DD"
    )


    gender: Optional[str] = Field(
        default="unknown",
        max_length=15,
        description="male / female / unknown"
    )


    occupation: str = Field(
        min_length=2,
        max_length=50,
        description="Declared occupation. e.g. Botanist, Journalist"
    )


    visa_type: str = Field(
        min_length=2,
        max_length=100,
        description="Tourist Visa / Research Visa / Journalist Visa / Business Visa"
    )


    visa_number: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Visa document number if available"
    )


    photo_url: Optional[str] = Field(
        default=None,
        description="Path to uploaded photo — set by system after photo capture"
    )


    criminal_record: bool = Field(
        default=False,
        description="Declared or verified criminal record flag"
    )

    @field_validator("passport_id")
    @classmethod
    def passport_must_be_uppercase(cls, v: str) -> str:
        passport_after_validation = v.strip().upper()
        return passport_after_validation

    

    @field_validator("nationality", "full_name")
    @classmethod
    def strip_whitespace_for_NAT_and_name(cls, v:str):
        after_validation = v.strip()
        return after_validation

    
    

    







class GetDetailsTraveler(BaseModel):
    pass




class GetPastRecord(BaseModel):
    pass



class PostCheckPostEvents(BaseModel):
    pass




class GetCheckPostEvents(BaseModel):
    pass



