# Discovery Benchmark Report

**Overall Score:** 79.7%

**Pass:** 52 | **Review:** 0 | **Fail:** 13

## Category Scores
- **wishlist behavior:** 40.0%
- **purchase barriers:** 66.7%
- **purchase intent:** 100.0%
- **purchase postponement:** 97.9%
- **uncertainty:** 100.0%
- **fit/size:** 66.7%
- **price:** 99.4%
- **quality/trust:** 100.0%
- **comparison behavior:** 98.5%
- **external research:** 99.6%
- **workarounds:** 100.0%
- **user segmentation:** 33.3%
- **cross-source analysis:** 33.3%
- **quantitative analysis:** 79.1%
- **opportunity identification:** 83.0%
- **non-monetary opportunities:** 100.0%
- **insufficient_evidence:** 100.0%
- **causal questions:** 50.0%

## Expected Mode Scores
- **answerable:** 84.4%
- **partially_answerable:** 49.6%
- **insufficient_evidence:** 94.4%

## Failures

### q02 (partially_answerable)
**Q:** How often do users review their wishlist before making a final purchase?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that there is no evidence to answer the question about how often users review their wishlist before making a purchase, and correctly issued a refusal.

### q06 (partially_answerable)
**Q:** Are shipping delays a major pre-purchase barrier compared to quality issues?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the provided evidence does not contain enough information to compare shipping delays to quality issues, accurately pointed out the contents of the single evidence card, cited the conversation ID properly, and correctly marked the response as having insufficient evidence.

### q18 (partially_answerable)
**Q:** Are fit issues more prominent in formal wear (suits/blazers) than in casual clothing?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly states that the evidence is insufficient to make a comparative claim between formal wear and casual clothing regarding fit issues. It accurately cites the deterministic metrics and the relevant indirect evidence ID while avoiding any unsupported claims or hallucinations.

### q34 (answerable)
**Q:** How do the barriers faced by users in the 'decision' stage differ from those in the 'discovery' stage?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the evidence lacks data for the 'discovery' stage, accurately cited the IDs for the provided evidence, properly distinguished between direct and indirect evidence, and made no unsupported claims.

### q35 (insufficient_evidence)
**Q:** Do high-intent users complain more about pricing or delivery times?
**Det Failures:** ['Expected insufficient_evidence refusal, but copilot answered.']
**Judge Feedback:** The copilot correctly identified that the evidence is insufficient to answer whether high-intent users complain more about pricing or delivery times. It accurately cited the deterministic metrics, correctly noted the presence of pricing complaints versus the complete lack of delivery time mentions, and cited conversation IDs properly.

### q38 (partially_answerable)
**Q:** Are trust issues mentioned more frequently on the App Store or YouTube?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the dataset only contains Google Play reviews and completely lacks YouTube data, appropriately refusing to answer the comparison question based on insufficient evidence.

### q39 (answerable)
**Q:** What is the average star rating of the Google Play reviews in this dataset compared to App Store?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the dataset does not contain star ratings or App Store reviews, handling the out-of-bounds question appropriately.

### q40 (answerable)
**Q:** Across the 172 conversations, what is the distribution of evidence-quality tiers?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the specific breakdown of evidence-quality tiers across all conversations is not explicitly stated in the dataset, while accurately citing the available evidence cards and limitations.

### q56 (partially_answerable)
**Q:** What evidence supports the claim that hidden fees cause cart abandonment?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that there is no direct evidence supporting the claim that hidden fees cause cart abandonment. It accurately cited the relevant indirect records and properly distinguished between direct and indirect evidence without making unsupported causal leaps.

### q57 (partially_answerable)
**Q:** Do fake reviews directly cause users to buy from competitors?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly recognized that there was no evidence provided to answer whether fake reviews directly cause users to buy from competitors, and appropriately refused to answer.

### q61 (partially_answerable)
**Q:** What evidence directly connects wishlist behavior to purchase decisions?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that the provided evidence does not contain wishlist behavior data and correctly stated that no such evidence is present, properly refusing to hallucinate an answer.

### q64 (answerable)
**Q:** What additional data would we need to determine which opportunity would have the biggest impact on wishlist-to-purchase conversion?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly identified that there is no evidence provided to answer the question about wishlist-to-purchase conversion data and appropriately refused.

### q65 (answerable)
**Q:** What can this dataset tell us about wishlist-to-purchase conversion, and what can it not tell us?
**Det Failures:** ['Unexpected refusal. Copilot should have attempted an answer.']
**Judge Feedback:** The copilot correctly recognized that there was no evidence provided to answer the question about wishlist-to-purchase conversion, and appropriately issued a refusal.