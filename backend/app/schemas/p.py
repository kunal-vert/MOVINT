from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict




class RegisterTravelerRequest(BaseModel):
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

    photo_url: Optional[str] = Field(
        default=None,
        description="Path to uploaded photo — set by system after photo capture"
    )


    criminal_record: bool = Field(
        default=False,
        description="Declared or verified criminal record flag"
    )

    entry_checkpoint_id: UUID = Field(
        description="UUID of the entry checkpoint where traveler is registering"
    )

    # lol => permit field-----------------------

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

    permit_type: Optional[str] = Field(
        default=None, max_length=200,
        description="ILP / RAP / Research Permit / Press Visa"
    )
    permit_issued_by: Optional[str] = Field(default=None, max_length=255)

    permit_valid_from: datetime

    permit_valid_to: datetime

    permit_permitted_states: Optional[List[str]] = Field(default=None)

    #jounrey fields

    declared_states: Optional[List[str]] = Field(
        default=None,
        description="States traveler declares they will visit"
    )

    expected_exit_at: datetime = Field(
        description="Visa expiry / declared departure. Must be future."
    )





     # validator

    @field_validator("passport_id")
    @classmethod
    def passport_must_be_uppercase(cls, v: str) -> str:
        passport_after_validation = v.strip().upper()
        return passport_after_validation

    

    @field_validator("nationality", "full_name")
    @classmethod
    def strip_whitespace_for_NAT_and_name(cls, v:str) -> str :
        after_validation = v.strip()
        return after_validation
    

    
    @field_validator("date_of_birth")
    @classmethod
    def date_must_be_past(cls, v:date) -> date:
        today = date.today()
      
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age <= 18:
            raise ValueError("Traveler must be at least 18 years old Ladle.....")
        return v


    @field_validator("expected_exit_at")
    @classmethod
    def exit_in_future(cls, v:datetime) -> datetime:
        if v <= datetime.now():
            raise ValueError(
                "expected_exit_at must be a future datetime"
            )

        return v

    @model_validator(mode="after")
    def permit_dates_check(self) -> RegisterTravelerRequest:
        if self.permit_valid_to <= self.permit_valid_from:
            raise ValueError(
                'permit_valid_to  must be after permit_valid_from'
            )
        return self




    
    

    

    
    
class TravelerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    passport_id:     str
    full_name:       str
    nationality:     str
    date_of_birth:   date
    gender:          Optional[str]
    photo_url:       Optional[str]
    watch_flag:      bool   
    criminal_record: bool   
    created_at:      datetime



class PermitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    visa_type:        str       
    visa_number:      Optional[str]
    occupation:       str       
    type:             Optional[str]
    issued_by:        Optional[str]
    permit_valid_from: datetime
    permit_valid_to:   datetime
    permitted_states: Optional[List[str]]




class JourneyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status:              str         
    current_risk_score:  int
    entered_at:          datetime
    exited_at:           Optional[datetime]
    expected_exit_at:    datetime
    declared_states:     Optional[List[str]]
    created_at:          datetime



   



class RegisterTravelerResponse(BaseModel):
    traveler:              TravelerOut
    journey:               List[JourneyOut]
    permit:                PermitOut
    is_returning_traveler: bool   
    past_journey_count:    int    
    initial_risk_score:    int     
    message:               str 


class TravelerSummary(BaseModel):
    """Lightweight traveler row for the list/tracking view."""
    passport_id:             str
    full_name:               str
    nationality:             str
    watch_flag:              bool
    criminal_record:         bool
    current_journey_status:  Optional[str]
    current_risk_score:      Optional[int]
    total_journeys:          int
    entered_at:              Optional[datetime]
    expected_exit_at:        Optional[datetime]


class TravelerListResponse(BaseModel):
    """Paginated list of tracked nationals."""
    total_count: int
    pages:        int
    per_pages:    int
    travelers:   List[TravelerSummary]
