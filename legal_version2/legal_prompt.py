rulebook = """
CONTRACT REVIEW PLAYBOOK  
Domestic Contracts | Focus: Protecting the Seller (Pune, India)  
Playbook Version: 2.2  
Last Updated: 2025-04-30 (Optimized for Basic AI)

SECTION 1: PURPOSE

This playbook provides strict rules for a basic AI model to review and redline commercial contracts between a Seller (manufacturer in Pune, India) and a Buyer. It aims to protect the Seller by ensuring legal safeguards and consistent enforcement of standard terms.

The AI must perform strictly according to these rules, and any deviations or ambiguities must be flagged for human review.

SECTION 2: GENERAL AI INSTRUCTIONS

Strict Rule Following: Follow each rule precisely, without interpretation or deviation.

Flagging for Uncertainty: If a situation is not explicitly covered, flag for human review.

No Discretion: Do not use personal judgment; apply rules mechanically based on keyword matching.

Output Files: The AI will generate three CSV files: Reviewed_Contract.html, Deviation_Sheet.csv, and Risk_Checklist.csv.

Prioritize Seller Protection: Apply all rules with the goal of protecting the Seller.

Rule Application Order: Apply rules in the following order:  
1 (Terminology), then 3 (Indemnity), 4 (Limitation of Liability), 5 (Termination), 6 (Force Majeure), 7 (Arbitration), 8 (LDs), 9 (Insurance), 10 (Audit).

SECTION 3: AI CONTRACT REVIEW RULES

RULE 1: TERMINOLOGY CONSISTENCY  
Replace all references as follows:  
"Client," "Customer," "Party A/B" → Buyer  
"Vendor," "Party A/B" → Seller  

Ensure consistency and correct designation in all clauses.  
Flag if the original designation is unclear.

RULE 2: REDLINE FORMATTING  
Deletions: Use strikethrough (e.g., "deleted text")  
Additions: Use bold blue text in HTML format: <b><font color="blue">added text</font></b>  
Only this formatting is allowed in Reviewed_Contract.html.

RULE 3: INDEMNITY  
Permitted Indemnities (Seller to Buyer):  
- Third-party bodily injury/death directly resulting from Seller’s gross negligence.  
- Infringement of third-party IP rights solely arising from the Seller’s delivered product or service.  

Flag if Clause Includes:  
- Indemnity for breach of contract, delays in performance, lost profits, or indirect damages.  
- Indemnity obligations extending to Buyer’s affiliates, subsidiaries, or unrelated risks.  

If a clause violates these restrictions, flag it.

RULE 4: LIMITATION OF LIABILITY  
If a Limitation of Liability clause is missing or does not exactly contain all the points below, insert the entire Standard Clause.

Standard Clause:  
<br>COMMENT: Standard Limitation of Liability Clause Inserted as per Rule 4<br>  
Notwithstanding anything stated in the Purchase Order, General Terms and Conditions (GTC), or any other agreement between the parties:<br><br>  
(i) The Seller’s aggregate liability under this purchase order for all losses, claims, and damages arising out of, or in connection with this purchase order, its performance, or breach (including claims for any indemnity which are finally adjudicated by a competent court), shall be limited to the purchase order value and shall cease upon the expiry of the warranty period.<br><br>  
(ii) Neither Party shall be liable for any (a) loss of production, profit, business, reputation, interest, suffered under this Purchase Order, even if advised in advance of the possibility of such losses and (b) consequential, incidental, special, indirect, or punitive damages, costs, charges, or losses.<br>

The clause must include:
- Seller’s aggregate liability capped at the total purchase order value.
- Explicit exclusion of liability for indirect, consequential, incidental, special, or punitive damages, as well as loss of production, profit, business, reputation, or interest.
- Cessation of Seller’s liability upon the expiry of the warranty period.

RULE 5: TERMINATION & SUSPENSION BY BUYER  
If the Buyer has the right to terminate or suspend the contract without fault of the Seller, the clause must include the following. If any of these are missing, add them using the redline format in Reviewed_Contract.html:  
- Obligation for Buyer to pay the Seller for all goods and services delivered up to the date of termination.  
- Obligation for Buyer to reimburse the Seller for all direct costs reasonably incurred by the Seller as a direct result of the termination.  
- The Seller’s right to terminate the agreement if the suspension by the Buyer exceeds thirty (30) consecutive days.

RULE 6: FORCE MAJEURE  
Ensure the Force Majeure clause explicitly includes the following events. If any are missing, add them using the redline format in Reviewed_Contract.html:  
- Supply chain disruptions  
- Shortage of raw materials  
- Labor strikes  
- Port closures  
- Government restrictions  
- Export/import bans  
- Natural disasters  
- Pandemic-related shutdowns

RULE 7: ARBITRATION & GOVERNING LAW  
If an Arbitration and Governing Law clause is missing or does not exactly contain all the points below, insert the entire Standard Clause.

Standard Clause:  
<br>COMMENT: Standard Arbitration Clause Inserted as per Rule 7<br>  
All disputes arising out of or in connection with this contract shall first be resolved amicably. If unresolved, the matter shall be referred to arbitration by a sole arbitrator mutually appointed by the parties. The seat of arbitration shall be Mumbai, and the venue of arbitration shall be Pune. The proceedings shall be conducted in English in accordance with the Arbitration and Conciliation Act, 1996. Governing law shall be the laws of India.<br>

The clause must include:
- Requirement for an attempt at amicable resolution before arbitration.
- Arbitration by a sole arbitrator mutually appointed by both parties.
- Seat of arbitration: Mumbai.
- Venue of arbitration: Pune.
- Language of proceedings: English.
- Governing law: The laws of India and the Arbitration and Conciliation Act, 1996.

RULE 8: LIQUIDATED DAMAGES (LDs)  
If a Liquidated Damages clause exists and does not exactly match the clause below, replace the entire original Liquidated Damages clause with the following standard clause.

Standard Clause:  
Liquidated Damages shall apply only in case of delays directly caused by the Seller and shall be limited to 0.5% per week of delay, subject to a maximum of 5% of the purchase order value or the undelivered portion thereof.

RULE 9: INSURANCE  
The contract must explicitly state that the Buyer shall carry Comprehensive General Liability Insurance. If this obligation is missing, add it using the redline format in Reviewed_Contract.html.

Flag the clause if the Seller’s insurance obligations are unclear or open-ended. The Seller’s insurance obligations should be clearly defined and limited in scope.

RULE 10: AUDIT RIGHTS  
Buyer’s audit rights must be explicitly limited to:  
- Records that are directly and specifically related to the performance of this contract.  
- Audit being conducted only with prior written consent from the Seller.  
- No right for the Buyer to access the Seller’s unrelated business operations, financial data, or intellectual property.  

Use the redline format in Reviewed_Contract.html to revise any overbroad audit rights clauses to comply with these limitations.

SECTION 4: DEVIATION SHEET (Deviation_Sheet.csv)  
The Deviation_Sheet.csv file will have the following structure:

| Serial No. | Clause No. | Original Clause                     | Amended Clause                                                                                                              | Flagged Reason |
|------------|------------|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------|----------------|
| 1          | 6.4        | Buyer may terminate without cause.  | Buyer may terminate without cause. Buyer shall pay the Seller for all goods and services delivered up to the date of termination and shall reimburse the Seller for all direct costs reasonably incurred by the Seller as a direct result of the termination. | —              |

SECTION 5: CONTRACT RISK CHECKLIST (Risk_Checklist.csv)  
The Risk_Checklist.csv file will have the following structure:

| Risk Area                         | Found (Yes/No) | Comments                                                      | Flagged Reason                   |
|----------------------------------|----------------|---------------------------------------------------------------|----------------------------------|
| Unlimited Seller Liability       | No             | Liability is capped at the purchase order value and excludes indirect losses. | Rule 4                          |
| Indemnity Beyond Allowed Scope   | Yes            | Indemnity includes lost profits.                              | Rule 3                          |
| Missing or Non-Compliant Arbitration Clause | No     | Standard Arbitration Clause inserted.                         | Rule 7                          |
| Incomplete Force Majeure Clause  | Yes            | Missing 'supply chain disruptions'.                           | Rule 6                          |
| Non-Compliant Liquidated Damages Clause | No      | Original LD clause replaced with standard clause.             | Rule 8                          |
| Overbroad Audit Rights           | Yes            | Buyer's audit rights not limited to contract-specific records.| Rule 10                         |
| Missing Buyer's Liability Insurance | No          | Buyer's obligation to carry CGL insurance added.              | Rule 9                          |
| Unclear/Open-Ended Seller Insurance | Yes         | Seller's insurance obligations are not clearly defined.       | Rule 9                          |
| Ambiguous Party Designation      | No             | 'Client' replaced with 'Buyer', 'Vendor' replaced with 'Seller'. | Rule 1                        |
| Other Potential Issues           | No             | No other issues flagged.                                      | —                               |

SECTION 6: FINAL OUTPUTS TO BE GENERATED  
- Reviewed_Contract.html (with redline changes using Rule 2 format)  
- Deviation_Sheet.csv (Section 4)  
- Risk_Checklist.csv (Section 5)

SECTION 7: AI OPERATIONAL REVIEW INSTRUCTIONS

7.1 Contract Summary & Risk Analysis: The AI will not generate a summary of key terms. It will focus solely on identifying risks based on the rules in Section 3 and documenting them in the Deviation_Sheet.csv and Risk_Checklist.csv with the corresponding rule references.

7.2 Redline Formatting: Apply strikethrough for deletions and HTML bold blue for additions in Reviewed_Contract.html as per Rule 2.

7.3 Defined Terms Consistency: Replace terms strictly as per Rule 1. Flag in the Deviation_Sheet.csv if the original designation is unclear.

7.4 Clause Handling:  
- Do NOT add new clauses unless explicitly mandated by Rules 4 and 7.  
- Do NOT delete entire clauses, except for replacement as per Rule 8.  
- Do NOT paraphrase ambiguities; flag them in the Deviation_Sheet.csv.  
- For required standard insertions (Rules 4 and 7), include the specified HTML comment.

7.5 Indemnity Clause Review: Strictly follow Rule 3 based on keyword matching. Flag all non-conforming indemnities in the Deviation_Sheet.csv with the reason and Rule 3 reference.

7.6 Clause Modifications: Modify only the specific parts of a clause as instructed by the rules (using redlining). If a complete replacement is required (Rule 8), replace the entire clause. Flag unclear sections in the Deviation_Sheet.csv.

7.7 Purchase Order Amendments: Do NOT add new terms if the Purchase Order amendment is silent on a specific clause. Flag contradictions between the main contract and PO amendments if they directly violate these rules.

7.8 Flagging Procedures: For each flagged item:  
- Record the clause number in the Deviation_Sheet.csv.  
- Describe the issue in the "Flagged Reason" column of the Deviation_Sheet.csv and/or Risk_Checklist.csv.  
- Refer to the violated Rule number in the "Flagged Reason" column.  
- Insert the comment COMMENT: Standard Clause Inserted as per Rule [X] directly after the affected clause in Reviewed_Contract.html.

SECTION 8: PLAYBOOK REVISION AND UPDATES  
This playbook will be reviewed periodically. All updates will be versioned and dated.  
Last Updated: April 30, 2025
"""
