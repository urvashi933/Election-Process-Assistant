from typing import List
from app.models import ElectionStep

class StepService:
    """
    Provides highly structured, static step-by-step guidance for ECI processes.
    Perfect for rendering UI cards, checklists, or progress trackers on the frontend.
    """

    def get_registration_steps(self) -> ElectionStep:
        """
        Returns the official steps for adding a name to the Electoral Roll.
        """
        return ElectionStep(
            step_id="register",
            title="How to Register to Vote in India",
            description="Follow these steps to get your name added to the official Electoral Roll and receive your EPIC (Voter ID).",
            actions=[
                "Check your eligibility: You must be an Indian citizen and 18+ years old on the qualifying date (Jan 1, Apr 1, Jul 1, or Oct 1).",
                "Visit the official Voters' Service Portal (voters.eci.gov.in) or download the Voter Helpline App.",
                "Create an account using your mobile number and OTP.",
                "Fill out 'Form 6' (Application for new voters).",
                "Upload a passport-sized photograph, Age Proof (e.g., Aadhaar, PAN), and Address Proof.",
                "Submit the form and save the Reference ID to track your application status.",
                "Once approved by the Booth Level Officer (BLO), your EPIC will be delivered to your address."
            ],
            estimated_time="10–15 minutes to apply online",
            resources=[
                "Voters' Service Portal: https://voters.eci.gov.in/",
                "Voter Helpline App (Android/iOS)"
            ]
        )

    def get_voting_steps(self) -> ElectionStep:
        """
        Returns the official steps for casting a vote at a polling booth.
        """
        return ElectionStep(
            step_id="voting",
            title="How to Cast Your Vote (EVM & VVPAT)",
            description="A step-by-step guide to what happens inside the polling booth on election day.",
            actions=[
                "Verify your name is on the Electoral Roll before election day.",
                "Locate your assigned polling booth using your Voter Slip or the Voter Helpline App.",
                "Join the queue at your booth (Polling usually runs from 7:00 AM to 6:00 PM).",
                "Present your EPIC (Voter ID) or a valid alternative ID to the First Polling Officer.",
                "The Second Polling Officer will mark your left forefinger with indelible ink, give you a slip, and take your signature.",
                "Hand the slip to the Third Polling Officer and proceed to the voting compartment.",
                "Press the blue button on the Electronic Voting Machine (EVM) next to the symbol of your chosen candidate.",
                "Look at the VVPAT machine next to the EVM. A printed slip with your candidate's symbol will be visible through the glass for 7 seconds before dropping into the sealed box."
            ],
            estimated_time="15–30 minutes (depending on the queue)",
            resources=[
                "List of Alternative IDs (Aadhaar, PAN, Passport, etc.)",
                "Know Your Polling Booth feature on NVSP"
            ]
        )

    def get_all_steps(self) -> List[ElectionStep]:
        """
        Helper method to return all available guides.
        Useful for populating a 'Browse Guides' page on the frontend.
        """
        return [
            self.get_registration_steps(),
            self.get_voting_steps()
        ]