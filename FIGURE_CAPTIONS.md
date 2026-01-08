# Figure Captions

## Algorithmic Bias Framework - All Generated Visualizations

**Nyx Dynamics LLC | January 2026**

---

## Clinical Framework Visualizations

### Figure C1: trajectory_no_intervention.png

**Title:** Algorithmic Harm - Mental Health Trajectory Without Clinical Intervention

**Caption:** Four-panel visualization of a moderate-risk client's 24-month trajectory without therapeutic intervention. **Panel A (Mental Health):** Mental health score begins at 65/100 and demonstrates gradual decline as algorithmic rejections accumulate, approaching but not crossing the depression threshold (40) in this simulation. The trajectory illustrates how repeated systemic rejection erodes psychological wellbeing even in clients with protective factors. **Panel B (Algorithmic Score):** Algorithmic standing declines from 45 to approximately 42 as rejection-generated negative data compounds. **Panel C (Shame and Avoidance):** Shame (red) increases with each rejection while behavioral avoidance (orange) rises in response to shame, creating a secondary feedback loop that reduces job-seeking behavior. **Panel D (Cumulative Rejections):** Stair-step pattern shows rejection accumulation over time, with each rejection contributing to both psychological harm and algorithmic score degradation.

---

### Figure C2: trajectory_combined_intervention.png

**Title:** Algorithmic Harm - Mental Health Trajectory With Combined Clinical Intervention

**Caption:** Four-panel visualization demonstrating the effect of combined intervention (psychoeducation + cognitive reframe + advocacy) initiated at month 3. **Panel A (Mental Health):** Green vertical line marks intervention onset. Mental health stabilizes and shows modest improvement compared to no-intervention trajectory, remaining well above depression threshold. **Panel B (Algorithmic Score):** Advocacy component produces direct improvement in algorithmic standing (+10 points), breaking the feedback loop between rejection and score degradation. **Panel C (Shame and Avoidance):** Psychoeducation reduces shame accumulation by validating external causation; cognitive reframe reduces avoidance behavior, enabling continued adaptive engagement with employment systems. **Panel D (Cumulative Rejections):** Reduced avoidance leads to continued applications, but improved algorithmic score reduces rejection rate, resulting in better outcomes despite continued system engagement.

---

### Figure C3: intervention_comparison.png

**Title:** Comparative Outcomes Across Intervention Modalities at 24 Months

**Caption:** Two-panel comparison of five intervention conditions. **Panel A (Trajectories):** Mental health trajectories over 24 months for no intervention (red), psychoeducation only (blue), cognitive reframe only (orange), advocacy/legal only (purple), and combined approach (green). All interventions initiated at month 3 (green dotted line). Combined approach (green) produces highest final mental health score, while single-modality interventions show intermediate effects. Depression threshold (gray dashed line at 40) serves as clinical reference. **Panel B (Final Outcomes):** Bar chart comparing final mental health scores (blue) and algorithmic scores (purple) at 24 months across conditions. Combined intervention achieves best outcomes on both dimensions (MH=67.6, Alg=45.0), demonstrating the necessity of addressing both psychological and systemic factors simultaneously. Clinical implication: Neither psychological intervention alone nor advocacy alone produces optimal outcomes; integrated treatment is recommended.

---

## Barrier Analysis Visualizations

### Figure B1: individual_barrier_effects.png

**Title:** Counterfactual Analysis of Individual Barrier Removal Effects

**Caption:** Horizontal bar chart displaying the marginal effect of removing each of the 11 barriers individually from the algorithmic bias barrier system. Bars are color-coded by layer: Data Integration (green), Data Accuracy (blue), Institutional (red). **Critical finding:** All individual effects approach 0% improvement in success probability. This counterintuitive result occurs because the barrier system operates as a multiplicative model—removing any single barrier has minimal impact when remaining barriers continue to block success. The "barrier trap" phenomenon demonstrates that the system exhibits high redundancy; addressing individual barriers (e.g., improving credit report accuracy alone, or providing legal aid alone) fails to produce meaningful improvement. Shapley value analysis reveals true attribution: Legal Knowledge Gap (11.5%), Rapid Data Transmission (10.6%), Systemic Bias (10.3%) are top contributors when accounting for interaction effects.

---

### Figure B2: stepwise_comparison.png

**Title:** Stepwise Cumulative Barrier Removal Strategy Comparison

**Caption:** Line plot comparing five barrier removal strategies across 11 removal steps. Strategies include: Forward (Layer 1→2→3, green), Backward (Layer 3→2→1, red), Optimal (greedy by marginal impact, purple), Cost-Optimal (greedy by cost-effectiveness, orange), and Random (average of 10 randomized orderings, gray). **Key finding:** All strategies show near-horizontal trajectories until the final 2-3 barriers are removed, at which point success probability rises sharply to ~100%. This convergence pattern—regardless of removal order—demonstrates the synergistic nature of the barrier system. **Policy implication:** Piecemeal interventions addressing 3, 5, or even 8 barriers produce minimal benefit; only comprehensive systemic reform removing all barriers achieves meaningful improvement. The mathematical equivalence of all strategies suggests that reform sequencing matters less than reform completeness.

---

### Figure B3: layer_effects.png

**Title:** Effect of Barrier Layer and Combination Removal

**Caption:** Two-panel analysis of layer-level barrier removal. **Panel A (Effect by Combination):** Bar chart showing success probability improvement when removing barrier layers individually or in combination. Single-layer removal achieves <1% improvement. Dual-layer combinations achieve 3-8% improvement. Only removal of all three layers (Data Integration + Data Accuracy + Institutional) achieves the full 95% improvement. Color gradient (light to dark green) indicates increasing intervention scope. **Panel B (Cost-Effectiveness):** Scatter plot with total removal cost on x-axis and effect on y-axis. Bubble size indicates number of barriers removed. The nonlinear relationship demonstrates that partial interventions achieve minimal benefit at proportional cost, while comprehensive reform—though more expensive (~$14,000 total)—achieves dramatically better cost-effectiveness. **Implication:** Investment should target comprehensive reform rather than incremental improvements.

---

### Figure B4: interaction_heatmap.png

**Title:** Layer Interaction Effects Matrix

**Caption:** Heatmap displaying individual and pairwise interaction effects between the three barrier layers. **Diagonal elements:** Individual layer effects when removed in isolation (Data Integration: 0.0%, Data Accuracy: 0.0%, Institutional: 0.3%). **Off-diagonal elements:** Pairwise interaction effects representing synergy beyond additive expectations. Positive values (green shading) indicate synergistic interactions where joint removal exceeds the sum of individual effects. The Data Integration × Institutional interaction (+7.6%) is the strongest pairwise effect. **Three-way interaction (not shown in matrix):** 87.6% of the total effect is attributable to the three-way interaction term, meaning the barriers function as a coordinated system rather than independent obstacles. This synergy explains why algorithmic discrimination is resistant to single-target interventions, paralleling multi-drug resistance in infectious disease treatment.

---

### Figure B5: shapley_attribution.png

**Title:** Shapley Value Attribution of Success Improvement

**Caption:** Horizontal bar chart displaying Shapley values for each barrier, representing the fair allocation of total improvement attributable to each barrier when accounting for all possible removal orderings. Bars color-coded by layer: Data Integration (green), Data Accuracy (blue), Institutional (red). **Top attributions:** Legal Knowledge Gap (11.5%), Rapid Data Transmission (10.6%), Systemic Bias in Algorithms (10.3%). Unlike marginal effects (which approach 0%), Shapley values reveal true causal contribution by averaging marginal contributions across all possible coalition orderings. **Clinical/Policy use:** Shapley values identify highest-value intervention targets when comprehensive reform is not immediately feasible. Addressing Legal Knowledge Gap (e.g., through legal aid, rights education) and Rapid Data Transmission (e.g., through data portability regulations) may provide greater marginal benefit than other single interventions.

---

## WMD and Shame Machine Visualizations

### Figure W1: wmd_assessment_radar.png

**Title:** Weapons of Math Destruction Assessment Radar Chart

**Caption:** Radar (spider) chart visualizing the algorithmic bias system's scores on Cathy O'Neil's three WMD criteria. **Axes:** Opacity (0.80/1.0 - SEVERE), Scale (1.00/1.0 - SEVERE), Damage (1.00/1.0 - SEVERE). Orange dashed line indicates the threshold for WMD classification (0.6 on each dimension). The algorithmic employment/credit/housing screening system exceeds threshold on all three criteria, yielding an overall WMD score of 0.93 and classification as a Weapon of Math Destruction. **Interpretation:** The system is opaque (scoring logic hidden from subjects), operates at massive scale (260M affected, 500M decisions/year), and causes significant damage (affects all major life domains with feedback loops creating irreversibility). Per O'Neil's framework, this system warrants immediate regulatory attention, mandatory transparency requirements, and third-party auditing.

---

### Figure W2: shame_analysis.png

**Title:** Shame Machine Analysis - Four-Panel Assessment

**Caption:** Four-panel visualization applying O'Neil's Shame Machine framework to algorithmic discrimination. **Panel A (Shame Direction):** Bar chart showing 100% of algorithmic shame events "punch down" on vulnerable individuals rather than "punching up" at powerful institutions. This toxic shame pattern shifts blame from system design to individual failure. **Panel B (Profit Extraction):** Comparison of institutional profit ($93K sample) versus individual cost ($662K sample) per shame event cluster, yielding an externality ratio of 1:7.1—for every dollar institutions save, individuals lose $7.10. **Panel C (Vulnerability Exploitation):** Horizontal bars showing vulnerability scores (0-1) for each decision type where algorithms punch down. Clinical trial exclusion (0.85) and housing rejection (0.80) target the most vulnerable populations. **Panel D (Responsibility Shift):** Histogram of responsibility shift magnitude across documented cases. Mean of 0.90 indicates nearly complete transfer of blame from institution to individual, consistent with O'Neil's thesis that shame machines allow institutions to externalize responsibility for systemic problems.

---

## Data Visualization Summary

| Repository | Figure | Key Finding |
|------------|--------|-------------|
| Clinical | C1-C3 | Combined intervention (psychoeducation + cognitive + advocacy) produces best outcomes |
| Barrier Analysis | B1-B5 | 87.6% three-way interaction explains piecemeal reform failure |
| WMD/Shame | W1-W2 | System qualifies as WMD; 100% punch-down ratio; 1:7.1 externality |

---

*Generated: January 8, 2026*
*Nyx Dynamics LLC*
