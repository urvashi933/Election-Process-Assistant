from typing import List
from app.models import ElectionStep

class StepService:
    def get_registration_steps(self) -> ElectionStep:
        return ElectionStep(
            step_id="register",
            title="How to Register to Vote in India",
            description="Follow these steps to get your name added to the Electoral Roll.",
            actions=[
                "Check eligibility (Indian citizen, 18+ years on qualifying date)",
                "Visit Voters' Service Portal (voters.eci.gov.in) or Voter Helpline App",
                "Fill Form 6 for new voter registration",
                "Upload required documents (Age & Address proof)",
                "Submit and track your reference number"
            ],
            estimated_time="10–15 minutes",
            resources=["voters.eci.gov.in", "Voter Helpline App"]
        )

    def get_voting_steps(self) -> ElectionStep:
        return ElectionStep(
            step_id="voting",
            title="How to Vote using an EVM",
            description="Steps to cast your vote at the polling booth.",
            actions=[
                "Check your name in the Electoral Roll",
                "Visit your assigned polling booth (usually 7 AM – 6 PM)",
                "Show your EPIC (Voter ID) or valid alternative ID to the polling officer",
                "Get your finger marked with indelible ink",
                "Press the blue button on the EVM next to your chosen candidate",
                "Verify your vote via the VVPAT slip (visible for 7 seconds)"
            ],
            estimated_time="10–20 minutes",
            resources=["Voter Slip", "Election Commission Guidelines"]
        )