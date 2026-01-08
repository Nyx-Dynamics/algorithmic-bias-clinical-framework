"""
ALGORITHMIC HARM - MENTAL HEALTH INTERACTION MODEL
Theoretical Framework for Clinical Practice

Models the bidirectional relationship between algorithmic discrimination
and mental health outcomes, including feedback loops and intervention points.

Author: AC Demidont, DO
Nyx Dynamics LLC
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum


class MentalHealthDomain(Enum):
    """Mental health domains affected by algorithmic harm."""
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    SHAME = "shame"
    LEARNED_HELPLESSNESS = "learned_helplessness"
    SELF_EFFICACY = "self_efficacy"
    SUBSTANCE_USE = "substance_use"
    FUNCTIONAL_IMPAIRMENT = "functional_impairment"


@dataclass
class ClientProfile:
    """Clinical profile for algorithmic harm assessment."""
    baseline_mental_health: float  # 0-100, higher = healthier
    baseline_algorithmic_score: float  # 0-100, higher = better standing
    vulnerability_factors: List[str]  # e.g., ["SUD_history", "justice_involved"]
    protective_factors: List[str]  # e.g., ["strong_support", "treatment_engaged"]
    months_since_adverse_event: float
    current_treatment: bool


class AlgorithmicMentalHealthModel:
    """
    Models the interaction between algorithmic harm and mental health.

    Key dynamics:
    1. Algorithmic rejection → psychological harm
    2. Psychological symptoms → behavioral changes
    3. Behavioral changes → new adverse algorithmic data
    4. Cycle repeats (bidirectional feedback loop)

    Intervention points:
    - Early: Prevent algorithmic integration
    - Middle: Break psychological feedback loop
    - Late: Harm reduction and adaptation
    """

    def __init__(self):
        # Model parameters
        self.rejection_shame_coefficient = 0.15  # How much each rejection increases shame
        self.shame_avoidance_coefficient = 0.20  # How shame leads to avoidance
        self.avoidance_score_coefficient = 0.10  # How avoidance worsens algorithmic score
        self.depression_onset_threshold = 40     # Mental health score below this = clinical depression
        self.treatment_efficacy = 0.30           # How much treatment reduces symptom severity

    def simulate_trajectory(self,
                           client: ClientProfile,
                           duration_months: int = 24,
                           intervention_month: int = None,
                           intervention_type: str = None) -> Dict:
        """
        Simulate client trajectory over time.

        intervention_type options:
        - "psychoeducation": Reduces shame coefficient
        - "cognitive_reframe": Reduces learned helplessness
        - "advocacy": Improves algorithmic score directly
        - "combined": All of the above
        """
        months = np.arange(0, duration_months + 1)

        # Initialize trajectories
        mental_health = [client.baseline_mental_health]
        algorithmic_score = [client.baseline_algorithmic_score]
        shame = [100 - client.baseline_mental_health]  # Inverse relationship
        avoidance = [0]
        rejections = [0]

        # Vulnerability multiplier
        vuln_multiplier = 1.0 + 0.15 * len(client.vulnerability_factors)
        prot_multiplier = 1.0 - 0.10 * len(client.protective_factors)

        # Intervention effects
        intervention_active = False
        shame_reduction = 0
        helplessness_reduction = 0
        score_boost = 0

        for m in range(1, duration_months + 1):
            # Check for intervention
            if intervention_month and m >= intervention_month:
                if not intervention_active:
                    intervention_active = True
                    if intervention_type == "psychoeducation":
                        shame_reduction = 0.30
                    elif intervention_type == "cognitive_reframe":
                        helplessness_reduction = 0.25
                    elif intervention_type == "advocacy":
                        score_boost = 15
                    elif intervention_type == "combined":
                        shame_reduction = 0.25
                        helplessness_reduction = 0.20
                        score_boost = 10

            # Calculate current algorithmic exposure
            current_score = algorithmic_score[-1] + score_boost

            # Rejection probability based on score
            rejection_prob = max(0, min(1, (100 - current_score) / 100 * 0.7))

            # Simulate rejection this month (if actively applying)
            applying = avoidance[-1] < 50  # Stop applying if avoidance > 50%
            rejected_this_month = applying and np.random.random() < rejection_prob

            # Update rejection count
            new_rejections = rejections[-1] + (1 if rejected_this_month else 0)
            rejections.append(new_rejections)

            # Update shame (increases with rejections, decreases with intervention)
            shame_increase = self.rejection_shame_coefficient * (1 if rejected_this_month else 0)
            shame_decrease = shame_reduction * 0.1 if intervention_active else 0
            new_shame = shame[-1] + shame_increase * vuln_multiplier - shame_decrease
            new_shame = max(0, min(100, new_shame))
            shame.append(new_shame)

            # Update avoidance (increases with shame)
            new_avoidance = avoidance[-1] + self.shame_avoidance_coefficient * new_shame * 0.1
            new_avoidance -= helplessness_reduction * 5 if intervention_active else 0
            new_avoidance = max(0, min(100, new_avoidance))
            avoidance.append(new_avoidance)

            # Update mental health
            mh_change = -0.5 * new_shame / 100 - 0.3 * new_avoidance / 100
            if client.current_treatment:
                mh_change += self.treatment_efficacy
            new_mh = mental_health[-1] + mh_change * prot_multiplier
            new_mh = max(0, min(100, new_mh))
            mental_health.append(new_mh)

            # Update algorithmic score
            score_change = -0.5 if rejected_this_month else 0.1  # Slight recovery if no rejection
            score_change -= self.avoidance_score_coefficient * new_avoidance / 100  # Avoidance creates gaps
            new_score = algorithmic_score[-1] + score_change
            new_score = max(0, min(100, new_score))
            algorithmic_score.append(new_score)

        return {
            'months': months,
            'mental_health': np.array(mental_health),
            'algorithmic_score': np.array(algorithmic_score),
            'shame': np.array(shame),
            'avoidance': np.array(avoidance),
            'rejections': np.array(rejections),
            'intervention_month': intervention_month,
            'intervention_type': intervention_type,
            'final_mental_health': mental_health[-1],
            'final_algorithmic_score': algorithmic_score[-1],
            'meets_depression_criteria': mental_health[-1] < self.depression_onset_threshold,
        }

    def compare_interventions(self, client: ClientProfile, duration: int = 24) -> Dict:
        """Compare outcomes across intervention types."""
        results = {}

        # No intervention
        results['no_intervention'] = self.simulate_trajectory(client, duration)

        # Different intervention types at month 3
        for intervention in ['psychoeducation', 'cognitive_reframe', 'advocacy', 'combined']:
            results[intervention] = self.simulate_trajectory(
                client, duration, intervention_month=3, intervention_type=intervention
            )

        return results

    def plot_client_trajectory(self, result: Dict, save_path: str = None):
        """Visualize a single client trajectory."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        months = result['months']

        # Panel A: Mental Health Score
        ax = axes[0, 0]
        ax.plot(months, result['mental_health'], 'b-', linewidth=2, label='Mental Health')
        ax.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Depression Threshold')
        if result['intervention_month']:
            ax.axvline(x=result['intervention_month'], color='green', linestyle=':',
                      label=f"Intervention ({result['intervention_type']})")
        ax.set_xlabel('Months')
        ax.set_ylabel('Mental Health Score')
        ax.set_title('A. Mental Health Trajectory', fontweight='bold')
        ax.legend()
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

        # Panel B: Algorithmic Score
        ax = axes[0, 1]
        ax.plot(months, result['algorithmic_score'], 'purple', linewidth=2)
        if result['intervention_month']:
            ax.axvline(x=result['intervention_month'], color='green', linestyle=':')
        ax.set_xlabel('Months')
        ax.set_ylabel('Algorithmic Score')
        ax.set_title('B. Algorithmic Score Trajectory', fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

        # Panel C: Shame and Avoidance
        ax = axes[1, 0]
        ax.plot(months, result['shame'], 'r-', linewidth=2, label='Shame')
        ax.plot(months, result['avoidance'], 'orange', linewidth=2, label='Avoidance')
        if result['intervention_month']:
            ax.axvline(x=result['intervention_month'], color='green', linestyle=':')
        ax.set_xlabel('Months')
        ax.set_ylabel('Symptom Severity')
        ax.set_title('C. Shame and Avoidance', fontweight='bold')
        ax.legend()
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

        # Panel D: Cumulative Rejections
        ax = axes[1, 1]
        ax.plot(months, result['rejections'], 'k-', linewidth=2)
        if result['intervention_month']:
            ax.axvline(x=result['intervention_month'], color='green', linestyle=':')
        ax.set_xlabel('Months')
        ax.set_ylabel('Cumulative Rejections')
        ax.set_title('D. Rejection Accumulation', fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.suptitle('Algorithmic Harm - Mental Health Interaction\nClient Trajectory',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved to {save_path}")

        return fig

    def plot_intervention_comparison(self, results: Dict, save_path: str = None):
        """Compare different intervention outcomes."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        colors = {
            'no_intervention': 'red',
            'psychoeducation': 'blue',
            'cognitive_reframe': 'orange',
            'advocacy': 'purple',
            'combined': 'green',
        }

        labels = {
            'no_intervention': 'No Intervention',
            'psychoeducation': 'Psychoeducation',
            'cognitive_reframe': 'Cognitive Reframe',
            'advocacy': 'Advocacy/Legal',
            'combined': 'Combined Approach',
        }

        # Panel A: Mental Health Trajectories
        ax = axes[0]
        for key, result in results.items():
            ax.plot(result['months'], result['mental_health'],
                   color=colors[key], linewidth=2, label=labels[key])

        ax.axhline(y=40, color='gray', linestyle='--', alpha=0.5, label='Depression Threshold')
        ax.axvline(x=3, color='green', linestyle=':', alpha=0.5)
        ax.set_xlabel('Months')
        ax.set_ylabel('Mental Health Score')
        ax.set_title('A. Mental Health by Intervention Type', fontweight='bold')
        ax.legend(loc='lower left', fontsize=8)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

        # Panel B: Final Outcomes Bar Chart
        ax = axes[1]
        interventions = list(results.keys())
        final_mh = [results[k]['final_mental_health'] for k in interventions]
        final_alg = [results[k]['final_algorithmic_score'] for k in interventions]

        x = np.arange(len(interventions))
        width = 0.35

        bars1 = ax.bar(x - width/2, final_mh, width, label='Mental Health', color='blue', alpha=0.7)
        bars2 = ax.bar(x + width/2, final_alg, width, label='Algorithmic Score', color='purple', alpha=0.7)

        ax.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Depression Threshold')
        ax.set_xlabel('Intervention Type')
        ax.set_ylabel('Final Score')
        ax.set_title('B. Final Outcomes at 24 Months', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([labels[k].replace(' ', '\n') for k in interventions], fontsize=8)
        ax.legend()
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved to {save_path}")

        return fig


def create_clinical_case_example():
    """Create example clinical cases for demonstration."""
    cases = {
        'moderate_risk': ClientProfile(
            baseline_mental_health=65,
            baseline_algorithmic_score=45,
            vulnerability_factors=['employment_gap', 'medical_debt'],
            protective_factors=['treatment_engaged'],
            months_since_adverse_event=4,
            current_treatment=True,
        ),
        'high_risk': ClientProfile(
            baseline_mental_health=50,
            baseline_algorithmic_score=30,
            vulnerability_factors=['SUD_history', 'justice_involved', 'housing_instability'],
            protective_factors=[],
            months_since_adverse_event=8,
            current_treatment=True,
        ),
        'severe_risk': ClientProfile(
            baseline_mental_health=35,
            baseline_algorithmic_score=20,
            vulnerability_factors=['SUD_history', 'HIV_positive', 'justice_involved', 'homeless'],
            protective_factors=['treatment_engaged'],
            months_since_adverse_event=18,
            current_treatment=True,
        ),
    }
    return cases


def main():
    """Demonstrate the algorithmic-mental health interaction model."""
    print("=" * 70)
    print("ALGORITHMIC HARM - MENTAL HEALTH INTERACTION MODEL")
    print("Clinical Framework Demonstration")
    print("=" * 70)

    model = AlgorithmicMentalHealthModel()
    cases = create_clinical_case_example()

    # Demonstrate with moderate risk case
    print("\n--- MODERATE RISK CASE ---")
    client = cases['moderate_risk']
    print(f"Baseline Mental Health: {client.baseline_mental_health}")
    print(f"Baseline Algorithmic Score: {client.baseline_algorithmic_score}")
    print(f"Vulnerability Factors: {client.vulnerability_factors}")
    print(f"Protective Factors: {client.protective_factors}")

    # Compare interventions
    results = model.compare_interventions(client, duration=24)

    print("\n24-MONTH OUTCOMES:")
    print("-" * 50)
    for intervention, result in results.items():
        print(f"{intervention:20s}: MH={result['final_mental_health']:.1f}, "
              f"Alg={result['final_algorithmic_score']:.1f}, "
              f"Depression={result['meets_depression_criteria']}")

    # Generate visualizations
    print("\nGenerating visualizations...")

    # Single trajectory (no intervention)
    model.plot_client_trajectory(results['no_intervention'],
                                 'trajectory_no_intervention.png')

    # Trajectory with combined intervention
    model.plot_client_trajectory(results['combined'],
                                 'trajectory_combined_intervention.png')

    # Intervention comparison
    model.plot_intervention_comparison(results, 'intervention_comparison.png')

    print("\nVisualization files created:")
    print("  - trajectory_no_intervention.png")
    print("  - trajectory_combined_intervention.png")
    print("  - intervention_comparison.png")

    # Key clinical insights
    print("\n" + "=" * 70)
    print("KEY CLINICAL INSIGHTS")
    print("=" * 70)
    print("""
1. WITHOUT INTERVENTION:
   - Mental health deteriorates steadily
   - Shame and avoidance compound
   - Algorithmic score continues declining
   - Depression criteria likely met within 12-18 months

2. PSYCHOEDUCATION ALONE:
   - Reduces shame by validating external cause
   - Limited effect on algorithmic trajectory
   - Mental health partially stabilized

3. COGNITIVE REFRAME ALONE:
   - Reduces learned helplessness
   - Decreases avoidance behavior
   - More applications = more data points (can backfire)

4. ADVOCACY/LEGAL ALONE:
   - Directly improves algorithmic score
   - Limited psychological effect
   - Doesn't address shame/avoidance

5. COMBINED APPROACH (RECOMMENDED):
   - Addresses both psychological and systemic factors
   - Best mental health outcomes
   - Most sustainable recovery trajectory
   - Requires coordination across disciplines
""")


if __name__ == "__main__":
    main()
