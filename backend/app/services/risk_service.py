from app.db.models import Checkpoint, CheckpointEvent, Journey, Permit, Traveler


def RiskCalc(pastTrackdata: Journey, Currentdata: Traveler, whileGoingIssue: CheckpointEvent, CurrentLoc: Checkpoint ):
    pass