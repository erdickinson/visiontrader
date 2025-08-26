from __future__ import annotations
from typing import Literal
from schemas import ActionDecision

State = Literal["FLAT","ARMED","IN_POSITION"]

class TraderStateMachine:
    def __init__(self):
        self.state: State = "FLAT"

    def step(self, decision: ActionDecision) -> State:
        a = decision.action
        if self.state == "FLAT":
            if a == "ARM":
                self.state = "ARMED"
            elif a == "ENTER":
                self.state = "IN_POSITION"
        elif self.state == "ARMED":
            if a == "ENTER":
                self.state = "IN_POSITION"
            elif a in ("CANCEL","WAIT"):
                self.state = "FLAT"
        elif self.state == "IN_POSITION":
            if a in ("EXIT","CANCEL"):
                self.state = "FLAT"
        return self.state
