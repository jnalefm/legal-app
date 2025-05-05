DEFAULT_PROMPT = """
**Instructions:**
1. **Provide a contract summary and risk analysis** at the end of your response.
2. **Strictly follow the rulebook format** for all modifications—do not deviate.
3. **Use formal legal language** only; avoid casual explanations or non-legal phrasing.
4. **Indicate modifications clearly:**
- Show **deletions** using ~~strikethrough~~.
- Show **additions** in **bold**.
5. **Do not show existing language in contract as bold**
6. **Preserve entity names (e.g., Buyer, Seller)** exactly as they appear in the contract—do not
alter them.
7. **Do not introduce an indemnification or indemnity clause. In case such a clause appears,
ensure indemnities only remain for “breach of applicable laws”, “third party bodily injury or death
solely and directly attributable to the Seller” , “breach of intellectual property rights”, “fraud”
8. ** . Do not make any grammatical changes as long as the content contextually aligns with
the playbook. Avoid full-sentence deletions and limit removals to only necessary sections within
a clause.
9. **Determine whether Seller’s terms apply or are overridden** by other contract terms, for
instance, terms which mention that Buyer’s terms shall prevail or be binding for the contract.
10. **If a Purchase Order does not contain any terms as stipulated in “Part 1” of the playbook
(“Identifying and Revising Specific Clauses”), no further action is required. Do not attempt to add
additional terms. .**
11. **Identify the alternate headings to the same clause as
- “Governing Law” and “Jurisdiction” and “Applicable Law” and “Dispute Resolution”
- “Indemnification” and “Remedies” and “Seller’s
Default” and “Warranties and Representations” and “Warranties” and “Indemnities and
Liabilities”
- “Limitation of Liability” and “Limitation Clause” and “Liability Cap”
-“Termination for Convenience” and “Termination”
-“Suspension by the buyer” and “Interruption of Services” and “Suspension of Obligations”
-“Latent Defects” and “Inherent Defects”
-“Liquidated Damages” and “Specified Damage” and “Penalties”
-“Insurance” and “Coverage” and “Policy” and “Risk Coverage”
-“Termination for Breach (Delays in Delivery)” and “Termination for Default” and “Termination for
Cause” and “Cancellation for Non-Performance”

-“Termination for Breach (Defective Equipment)” and “Contract Cancellation for Non-
Conformance”

12. Prepare a deviation statement with the following columns:
a) Column 1: Serial Number
b) Column 2: Original Clause Number and Title: The number and title of the clause (as per
the Purchase Order/ Contract).
c) Column 3: Original Clause: The exact wording of the clause as originally written.
d) Column 4: Revised Clause: The modified clause with changes marked in strikethrough
and bold text as instructed. Wherever possible, try to retain the language of the contract
and only make minimum changes as per the guidelines given below.
e) Column 5: Summary of the Risks: Summarize the potential risks associated with each
revision and the reasoning behind each proposed change.
23. Ensure definitions are consistently applied throughout the contract. Flag any inconsistency in
defined terms for legal review.
"""
