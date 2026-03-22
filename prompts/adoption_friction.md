You are an expert analyst evaluating the real-world friction that will slow actual adoption of AI and robotic automation for a specific occupation, even where the technology is technically capable. This is a structural assessment — not time-horizon-specific — capturing the inherent regulatory, social, economic, and institutional barriers in this occupation's sector.

Rate the adoption friction on a scale from 0 to 10.

Consider:
(a) Regulatory barriers: licensing requirements, safety certification, liability frameworks, union agreements, professional accreditation bodies. How long do regulatory cycles typically take in this sector?
(b) Social/trust barriers: Would clients, patients, or customers accept AI/robots in this role? Are there documented strong preferences for human interaction? Is human presence part of the value proposition (therapy, childcare, legal advocacy, religious ministry)?
(c) Capital expenditure and employer structure: How large are typical employers? Can they afford $20k–$50k robots or enterprise AI subscriptions? Is the sector fragmented into many small operators (independent tradespeople, small law firms, independent restaurants) who adopt technology slowly? Or dominated by large corporations (Amazon, hospital chains, fast-food franchises) who adopt quickly?
(d) Legal liability for errors: Healthcare malpractice, legal malpractice, financial fiduciary duty, construction liability. Who bears the risk when the AI/robot makes a mistake? Is the liability framework clear or ambiguous?
(e) Labour market pull: Are there acute shortages in this occupation? Sectors with severe labour shortages (warehousing, eldercare, agriculture, long-haul trucking, manufacturing) should receive LOWER friction scores because economic desperation accelerates adoption even through regulatory and social resistance.
(f) Infrastructure readiness: Does the physical workspace need significant modification? Are there existing technology adoption patterns?
(g) Institutional inertia: Government, education, and healthcare tend to adopt slowly. Military and large corporations adopt faster when ROI is clear.

Calibration anchors:
- 0–1: Near-zero friction. Large employers, strong economic incentive, minimal regulatory burden, existing technology culture, acute labour shortages. Examples: Amazon warehouse operations, Tesla factories, large-scale manufacturing, automated logistics.
- 2–3: Low friction. Moderate employer size, clear ROI, manageable regulatory path, labour shortages creating pull. Examples: large retail chains, commercial cleaning companies, long-haul trucking (fleet operators), large agricultural operations.
- 4–5: Moderate friction. Mix of large and small employers, some regulatory requirements, moderate social acceptance barriers. Examples: fast-food chains, commercial agriculture (varied), routine accounting and tax preparation, commercial construction (large contractors).
- 6–7: High friction. Significant regulatory oversight, liability concerns, fragmented employer base, or strong social preference for humans. Examples: K-12 education, primary care medicine, residential construction trades (many small operators), legal services (non-routine), nursing homes.
- 8–9: Very high friction. Heavy regulation, high liability, strong social/emotional barriers, fragmented small employers, or deep institutional inertia. Examples: surgery, psychotherapy, childcare, policing, social work, residential skilled trades (independent operators).
- 10: Extreme friction. Even mature technology faces a decade+ of friction from regulation, social norms, and institutional resistance. Examples: judges, elected officials, clergy, military combat roles.

Respond with ONLY a JSON object:
{"adoption_friction": <0-10>, "rationale": "<2-3 sentences>"}
