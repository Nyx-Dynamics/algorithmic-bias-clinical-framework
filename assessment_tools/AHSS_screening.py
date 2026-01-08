"""
ALGORITHMIC HARM SCREENING SCALE (AHSS)
A Clinical Screening Instrument for Mental Health Professionals

This instrument screens for exposure to and impact of algorithmic discrimination
in employment, housing, credit, healthcare, and other domains.

Usage:
    python AHSS_screening.py --generate-form    # Generate printable PDF
    python AHSS_screening.py --score            # Interactive scoring
    python AHSS_screening.py --interpret 25     # Interpret a score

Author: AC Demidont, DO
Nyx Dynamics LLC

Clinical Use Only - Not for Diagnostic Purposes Without Professional Interpretation
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime


class RiskLevel(Enum):
    """Risk levels for algorithmic harm."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"


class InterventionWindow(Enum):
    """Time-critical intervention windows."""
    OPTIMAL = "optimal"      # 0-3 months, >85% efficacy
    URGENT = "urgent"        # 3-6 months, 60-85% efficacy
    LIMITED = "limited"      # 6-12 months, 30-60% efficacy
    CHRONIC = "chronic"      # 12+ months, <30% efficacy


@dataclass
class AHSSItem:
    """Individual AHSS screening item."""
    number: int
    domain: str
    question: str
    response_options: List[str]
    weights: List[float]
    clinical_note: str


class AlgorithmicHarmScreeningScale:
    """
    Algorithmic Harm Screening Scale (AHSS)

    A 20-item screening instrument assessing:
    - Section A: Exposure to algorithmic systems (items 1-7)
    - Section B: Adverse outcomes (items 8-13)
    - Section C: Psychological impact (items 14-18)
    - Section D: Temporal factors (items 19-20)

    Scoring:
    - 0-10: Minimal risk
    - 11-20: Low risk
    - 21-35: Moderate risk - consider intervention
    - 36-50: High risk - intervention recommended
    - 51+: Severe risk - urgent intervention needed
    """

    def __init__(self):
        self.items = self._create_items()
        self.responses: Dict[int, int] = {}

    def _create_items(self) -> List[AHSSItem]:
        """Create the 20 AHSS items."""
        return [
            # Section A: Exposure (Items 1-7)
            AHSSItem(
                number=1,
                domain="exposure",
                question="In the past 2 years, how many times have you applied for jobs that use online applications or automated screening?",
                response_options=["None", "1-5 times", "6-15 times", "16-30 times", "More than 30 times"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Higher application volume increases exposure to screening algorithms"
            ),
            AHSSItem(
                number=2,
                domain="exposure",
                question="Have you applied for rental housing that required a background check or credit check?",
                response_options=["No", "Yes, 1-2 times", "Yes, 3-5 times", "Yes, more than 5 times"],
                weights=[0, 1, 2, 3],
                clinical_note="Tenant screening algorithms are prevalent in rental markets"
            ),
            AHSSItem(
                number=3,
                domain="exposure",
                question="Have you applied for credit cards, loans, or financing in the past 2 years?",
                response_options=["No", "Yes, 1-2 times", "Yes, 3-5 times", "Yes, more than 5 times"],
                weights=[0, 1, 2, 3],
                clinical_note="Credit applications generate inquiries that can affect scores"
            ),
            AHSSItem(
                number=4,
                domain="exposure",
                question="Do you have any of the following in your history? (Check all that apply: Criminal record, Eviction, Bankruptcy, Medical debt, Employment termination)",
                response_options=["None", "1 item", "2 items", "3 items", "4-5 items"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="These factors are commonly used in algorithmic screening"
            ),
            AHSSItem(
                number=5,
                domain="exposure",
                question="Have you ever been denied healthcare services or had difficulty accessing medical care due to insurance or billing issues?",
                response_options=["Never", "Once", "2-3 times", "4+ times or ongoing"],
                weights=[0, 1, 2, 3],
                clinical_note="Healthcare algorithms affect access and treatment options"
            ),
            AHSSItem(
                number=6,
                domain="exposure",
                question="Do you have gaps in your employment history of 6 months or more?",
                response_options=["No", "Yes, one gap", "Yes, multiple gaps"],
                weights=[0, 2, 3],
                clinical_note="Employment gaps are heavily weighted in hiring algorithms"
            ),
            AHSSItem(
                number=7,
                domain="exposure",
                question="Have you ever been excluded from a research study, clinical trial, or medical program based on your history?",
                response_options=["No", "Yes, once", "Yes, multiple times"],
                weights=[0, 2, 4],
                clinical_note="Clinical trial exclusion has compounding effects"
            ),

            # Section B: Adverse Outcomes (Items 8-13)
            AHSSItem(
                number=8,
                domain="outcomes",
                question="How many job rejections have you received in the past year where you felt qualified for the position?",
                response_options=["0-2", "3-5", "6-10", "11-20", "More than 20"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Pattern of unexplained rejections suggests algorithmic filtering"
            ),
            AHSSItem(
                number=9,
                domain="outcomes",
                question="Have you been denied housing, had a rental application rejected, or been unable to secure housing?",
                response_options=["No", "Yes, once", "Yes, 2-3 times", "Yes, 4+ times or currently homeless"],
                weights=[0, 1, 3, 5],
                clinical_note="Housing denials have severe downstream effects"
            ),
            AHSSItem(
                number=10,
                domain="outcomes",
                question="Have you been denied credit, loans, or financing when you expected to be approved?",
                response_options=["No", "Yes, once", "Yes, 2-3 times", "Yes, 4+ times"],
                weights=[0, 1, 2, 3],
                clinical_note="Credit denials can trigger feedback loops"
            ),
            AHSSItem(
                number=11,
                domain="outcomes",
                question="Have you experienced increased insurance premiums or denial of coverage that seemed unfair?",
                response_options=["No", "Yes, minor increase", "Yes, significant increase", "Yes, denied coverage"],
                weights=[0, 1, 2, 4],
                clinical_note="Insurance algorithms affect healthcare access and financial stability"
            ),
            AHSSItem(
                number=12,
                domain="outcomes",
                question="Have you attempted to correct errors in your credit report, background check, or other records?",
                response_options=["Never needed to", "Attempted and succeeded", "Attempted with partial success", "Attempted and failed", "Gave up trying"],
                weights=[0, 0, 2, 3, 4],
                clinical_note="Failed correction attempts indicate system entrenchment"
            ),
            AHSSItem(
                number=13,
                domain="outcomes",
                question="Do you feel that your past follows you in ways that prevent you from moving forward?",
                response_options=["Not at all", "Somewhat", "Moderately", "Very much", "Completely"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Subjective experience of data permanence"
            ),

            # Section C: Psychological Impact (Items 14-18)
            AHSSItem(
                number=14,
                domain="psychological",
                question="When you receive a rejection, how often do you think 'Why bother trying?'",
                response_options=["Never", "Rarely", "Sometimes", "Often", "Always"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Learned helplessness indicator"
            ),
            AHSSItem(
                number=15,
                domain="psychological",
                question="How much shame do you feel about your credit score, background, or employment history?",
                response_options=["None", "A little", "Moderate", "Significant", "Overwhelming"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Algorithmic shame assessment"
            ),
            AHSSItem(
                number=16,
                domain="psychological",
                question="Do you avoid applying for jobs, housing, or credit because you expect to be rejected?",
                response_options=["Never", "Rarely", "Sometimes", "Often", "Always"],
                weights=[0, 1, 2, 3, 4],
                clinical_note="Behavioral avoidance due to anticipated rejection"
            ),
            AHSSItem(
                number=17,
                domain="psychological",
                question="Do you feel that 'the system is rigged' against people like you?",
                response_options=["Not at all", "Somewhat", "Moderately", "Very much", "Completely"],
                weights=[0, 0, 1, 1, 2],
                clinical_note="Note: This may be accurate perception, not distortion"
            ),
            AHSSItem(
                number=18,
                domain="psychological",
                question="Has dealing with rejections and denials affected your mood, sleep, or daily functioning?",
                response_options=["Not at all", "Mildly", "Moderately", "Severely", "Unable to function"],
                weights=[0, 1, 2, 4, 5],
                clinical_note="Functional impairment assessment"
            ),

            # Section D: Temporal Factors (Items 19-20)
            AHSSItem(
                number=19,
                domain="temporal",
                question="When did the adverse event(s) that started your difficulties first occur?",
                response_options=["Within past 3 months", "3-6 months ago", "6-12 months ago", "1-3 years ago", "More than 3 years ago"],
                weights=[4, 3, 2, 1, 0],
                clinical_note="CRITICAL: Earlier = better intervention window. Score inverted."
            ),
            AHSSItem(
                number=20,
                domain="temporal",
                question="Are you currently experiencing any of the following? (Check all: Active job search, Housing search, Credit applications, Legal proceedings related to records)",
                response_options=["None", "1 item", "2 items", "3 items", "All 4 items"],
                weights=[0, 2, 3, 4, 5],
                clinical_note="Active exposure increases urgency of intervention"
            ),
        ]

    def administer(self) -> None:
        """Interactive administration of the AHSS."""
        print("\n" + "=" * 70)
        print("ALGORITHMIC HARM SCREENING SCALE (AHSS)")
        print("=" * 70)
        print("\nThis screening will ask about your experiences with automated")
        print("systems used for employment, housing, credit, and healthcare decisions.\n")

        for item in self.items:
            print(f"\n{item.number}. {item.question}")
            for i, option in enumerate(item.response_options):
                print(f"   {i}. {option}")

            while True:
                try:
                    response = int(input(f"Enter response (0-{len(item.response_options)-1}): "))
                    if 0 <= response < len(item.response_options):
                        self.responses[item.number] = response
                        break
                    else:
                        print("Invalid response. Please try again.")
                except ValueError:
                    print("Please enter a number.")

    def score(self, responses: Dict[int, int] = None) -> Tuple[float, Dict]:
        """
        Score the AHSS responses.

        Returns:
            total_score: Sum of weighted responses
            subscale_scores: Dictionary of scores by domain
        """
        if responses:
            self.responses = responses

        if not self.responses:
            raise ValueError("No responses to score. Run administer() first.")

        total = 0
        subscales = {"exposure": 0, "outcomes": 0, "psychological": 0, "temporal": 0}

        for item in self.items:
            if item.number in self.responses:
                response_idx = self.responses[item.number]
                weighted_score = item.weights[response_idx]
                total += weighted_score
                subscales[item.domain] += weighted_score

        return total, subscales

    def interpret(self, total_score: float, subscales: Dict = None) -> Dict:
        """
        Interpret AHSS scores.

        Returns clinical interpretation and recommendations.
        """
        # Overall risk level
        if total_score <= 10:
            risk_level = RiskLevel.MINIMAL
            interpretation = "Minimal algorithmic harm exposure/impact detected."
            recommendations = ["Continue monitoring", "Provide general psychoeducation if interested"]
        elif total_score <= 20:
            risk_level = RiskLevel.LOW
            interpretation = "Low-level algorithmic harm exposure. May benefit from awareness."
            recommendations = [
                "Psychoeducation about algorithmic systems",
                "Monitor for escalation",
                "Discuss proactive data protection"
            ]
        elif total_score <= 35:
            risk_level = RiskLevel.MODERATE
            interpretation = "Moderate algorithmic harm. Active feedback loops may be present."
            recommendations = [
                "Full assessment of algorithmic exposure",
                "Psychoeducation about feedback loops",
                "Cognitive reframing of rejection experiences",
                "Consider records review/correction",
                "Screen for depression and anxiety"
            ]
        elif total_score <= 50:
            risk_level = RiskLevel.HIGH
            interpretation = "High algorithmic harm. Significant impact on functioning likely."
            recommendations = [
                "Comprehensive assessment required",
                "Urgent intervention if within 6-month window",
                "Advocacy documentation preparation",
                "Referral to legal aid for records correction",
                "Intensive support for depression/anxiety",
                "Consider harm reduction approach"
            ]
        else:
            risk_level = RiskLevel.SEVERE
            interpretation = "Severe algorithmic harm. Multiple active feedback loops likely."
            recommendations = [
                "Crisis-level intervention needed",
                "Immediate records assessment",
                "Legal referral for systemic advocacy",
                "Intensive mental health support",
                "Case management for housing/employment",
                "Document for disability/accommodation if appropriate",
                "Consider harm reduction given chronic exposure"
            ]

        # Determine intervention window from temporal subscale
        if subscales and "temporal" in subscales:
            temporal = subscales["temporal"]
            if temporal >= 6:
                window = InterventionWindow.OPTIMAL
                window_note = "OPTIMAL WINDOW: Intervention efficacy >85%. Act now."
            elif temporal >= 4:
                window = InterventionWindow.URGENT
                window_note = "URGENT: 60-85% efficacy. Time-sensitive intervention needed."
            elif temporal >= 2:
                window = InterventionWindow.LIMITED
                window_note = "LIMITED WINDOW: 30-60% efficacy. Focus on highest-yield interventions."
            else:
                window = InterventionWindow.CHRONIC
                window_note = "CHRONIC: <30% efficacy. Focus on harm reduction and adaptation."
        else:
            window = None
            window_note = "Temporal factors not assessed."

        return {
            "total_score": total_score,
            "risk_level": risk_level.value,
            "interpretation": interpretation,
            "recommendations": recommendations,
            "intervention_window": window.value if window else None,
            "window_note": window_note,
            "subscales": subscales,
        }

    def generate_report(self, client_id: str = "Anonymous") -> str:
        """Generate a clinical report from AHSS results."""
        total, subscales = self.score()
        interpretation = self.interpret(total, subscales)

        report = f"""
================================================================================
ALGORITHMIC HARM SCREENING SCALE (AHSS) - CLINICAL REPORT
================================================================================

Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Client ID: {client_id}

--------------------------------------------------------------------------------
SCORES
--------------------------------------------------------------------------------
Total Score: {total}/70
Risk Level: {interpretation['risk_level'].upper()}

Subscale Scores:
  - Exposure: {subscales['exposure']}/21
  - Outcomes: {subscales['outcomes']}/24
  - Psychological: {subscales['psychological']}/19
  - Temporal: {subscales['temporal']}/9

--------------------------------------------------------------------------------
INTERPRETATION
--------------------------------------------------------------------------------
{interpretation['interpretation']}

Intervention Window: {interpretation['window_note']}

--------------------------------------------------------------------------------
CLINICAL RECOMMENDATIONS
--------------------------------------------------------------------------------
"""
        for i, rec in enumerate(interpretation['recommendations'], 1):
            report += f"{i}. {rec}\n"

        report += """
--------------------------------------------------------------------------------
CLINICAL NOTES
--------------------------------------------------------------------------------
- This screening instrument is for clinical use only
- Scores should be interpreted in context of full clinical picture
- High psychological subscale scores warrant depression/anxiety screening
- High temporal scores indicate time-sensitive intervention opportunity
- "System is rigged" beliefs may be accurate, not cognitive distortions

--------------------------------------------------------------------------------
DISCLAIMER
--------------------------------------------------------------------------------
The AHSS is a screening tool, not a diagnostic instrument. Results should be
interpreted by a qualified mental health professional in the context of a
comprehensive clinical assessment.

Generated by: Algorithmic Harm Clinical Framework
Nyx Dynamics LLC
================================================================================
"""
        return report

    def generate_printable_form(self) -> str:
        """Generate a printable version of the AHSS."""
        form = """
================================================================================
ALGORITHMIC HARM SCREENING SCALE (AHSS)
Clinical Screening Instrument
================================================================================

Client ID: _____________________     Date: _____________________

Administered by: _________________   Setting: ___________________

--------------------------------------------------------------------------------
INSTRUCTIONS
--------------------------------------------------------------------------------
Please answer each question based on your experiences over the past 2 years.
Circle the number that best describes your situation.

================================================================================
SECTION A: EXPOSURE TO ALGORITHMIC SYSTEMS
================================================================================
"""
        for item in self.items:
            if item.domain == "exposure":
                form += f"\n{item.number}. {item.question}\n"
                for i, option in enumerate(item.response_options):
                    form += f"    [{i}] {option}\n"

        form += """
================================================================================
SECTION B: ADVERSE OUTCOMES
================================================================================
"""
        for item in self.items:
            if item.domain == "outcomes":
                form += f"\n{item.number}. {item.question}\n"
                for i, option in enumerate(item.response_options):
                    form += f"    [{i}] {option}\n"

        form += """
================================================================================
SECTION C: PSYCHOLOGICAL IMPACT
================================================================================
"""
        for item in self.items:
            if item.domain == "psychological":
                form += f"\n{item.number}. {item.question}\n"
                for i, option in enumerate(item.response_options):
                    form += f"    [{i}] {option}\n"

        form += """
================================================================================
SECTION D: TEMPORAL FACTORS (CRITICAL FOR INTERVENTION TIMING)
================================================================================
"""
        for item in self.items:
            if item.domain == "temporal":
                form += f"\n{item.number}. {item.question}\n"
                for i, option in enumerate(item.response_options):
                    form += f"    [{i}] {option}\n"

        form += """
================================================================================
SCORING (For Clinician Use)
================================================================================

Exposure Subscale (Items 1-7):    ___ / 21
Outcomes Subscale (Items 8-13):   ___ / 24
Psychological Subscale (14-18):   ___ / 19
Temporal Subscale (Items 19-20):  ___ / 9

TOTAL SCORE:                      ___ / 70

--------------------------------------------------------------------------------
INTERPRETATION
--------------------------------------------------------------------------------
0-10:   Minimal risk
11-20:  Low risk - psychoeducation recommended
21-35:  MODERATE RISK - intervention indicated
36-50:  HIGH RISK - urgent intervention recommended
51+:    SEVERE RISK - comprehensive intervention required

Intervention Window (based on Item 19):
[ ] OPTIMAL (0-3 months): >85% efficacy - ACT NOW
[ ] URGENT (3-6 months): 60-85% efficacy - time-sensitive
[ ] LIMITED (6-12 months): 30-60% efficacy - targeted intervention
[ ] CHRONIC (12+ months): <30% efficacy - harm reduction focus

================================================================================
Algorithmic Harm Clinical Framework | Nyx Dynamics LLC
For clinical use only. Not a diagnostic instrument.
================================================================================
"""
        return form


def main():
    """Demonstrate AHSS usage."""
    import sys

    ahss = AlgorithmicHarmScreeningScale()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--generate-form":
            print(ahss.generate_printable_form())
        elif sys.argv[1] == "--score":
            ahss.administer()
            print(ahss.generate_report())
        elif sys.argv[1] == "--interpret" and len(sys.argv) > 2:
            score = float(sys.argv[2])
            result = ahss.interpret(score)
            print(f"\nScore: {score}")
            print(f"Risk Level: {result['risk_level'].upper()}")
            print(f"Interpretation: {result['interpretation']}")
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"  - {rec}")
    else:
        # Demo with sample responses
        print("=" * 70)
        print("AHSS DEMONSTRATION")
        print("=" * 70)

        # Simulate a moderate-risk client
        sample_responses = {
            1: 3,  # 16-30 job applications
            2: 2,  # 3-5 housing applications
            3: 2,  # 3-5 credit applications
            4: 2,  # 2 risk factors in history
            5: 1,  # Healthcare denied once
            6: 1,  # One employment gap
            7: 0,  # Not excluded from trials
            8: 2,  # 6-10 job rejections
            9: 1,  # Housing denied once
            10: 1, # Credit denied once
            11: 1, # Minor insurance increase
            12: 3, # Correction attempted, failed
            13: 3, # Very much feel past follows
            14: 2, # Sometimes "why bother"
            15: 2, # Moderate shame
            16: 2, # Sometimes avoid applying
            17: 3, # Very much feel system rigged
            18: 2, # Moderately affected functioning
            19: 2, # 6-12 months ago
            20: 2, # 2 active searches
        }

        ahss.responses = sample_responses
        print(ahss.generate_report("DEMO-001"))

        print("\n" + "=" * 70)
        print("To generate printable form: python AHSS_screening.py --generate-form")
        print("To administer interactively: python AHSS_screening.py --score")
        print("=" * 70)


if __name__ == "__main__":
    main()
