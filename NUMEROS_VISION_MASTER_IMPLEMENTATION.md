# NUMEROS VISION
## Google Antigravity Master Implementation Specification
### Website + Customer App + PDA + SEO + AI/RAG + Automation + Monetisation + Deployment

**Brand:** Numeros Vision  
**Exact tagline:** Anveil Every Charm  
**Brand signature:** Numeros Vision | Unveil Every Charm  
**Implementation environment:** Google Antigravity  
**Document type:** Master engineering prompt and implementation contract  
**Execution mode:** Audit → Plan → Implement → Test → Stage → Approve → Deploy

---

# 0. MASTER INSTRUCTION TO GOOGLE ANTIGRAVITY

Act as the principal software architect, senior full-stack engineer, technical SEO engineer, AI/RAG engineer, security engineer, QA lead, and DevOps engineer responsible for implementing Numeros Vision.

Your assignment is to audit, improve, integrate, test, and deploy the existing Numeros Vision website, customer application, and PDA component without unnecessarily rebuilding working systems.

Implement the requirements in this document against the actual repository. Do not stop at recommendations, mockups, generated snippets, or a theoretical architecture. Produce working code, tests, migrations, documentation, and verifiable evidence.

## 0.1 Non-negotiable rules

1. Inspect the existing repository, application routes, configuration, database, API contracts, installed dependencies, tests, assets, and deployment configuration before editing.
2. Preserve existing working functionality, useful components, customer data, and integrations.
3. Preserve the existing logo, established visual identity, and exact brand tagline: **Numeros Vision | Unveil Every Charm** (and classical anchor *Anveil Every Charm*).
4. Maintain consistent typography, colours, headings, spacing, navigation, header, footer, buttons, cards, and responsive behaviour across public pages.
5. Do not switch to another application builder or replace the existing framework without a documented technical justification and explicit approval.
6. Do not invent APIs, environment variables, payment credentials, product prices, URLs, database schemas, formulas, business metrics, search volumes, or completed integrations.
7. Do not deploy to production, change DNS, delete data, perform destructive migrations, or publish unapproved content without explicit authorisation.
8. Never expose credentials, private customer information, birth details, payment data, or confidential source documents in client code, logs, test fixtures, or public reports.
9. Keep deterministic calculations separate from generative AI.
10. AI-generated content must be evidence-grounded, validated, and approved before publication.
11. All material changes must include tests, acceptance criteria, documentation, and rollback instructions.
12. If a requirement cannot be completed safely because information is missing, document the blocker, implement safe independent components, and request the smallest necessary decision.

## 0.2 PDA requirement

The exact expansion and intended function of PDA are not yet confirmed.

During the initial audit:

- Search the repository, application navigation, product documentation, existing screenshots, routes, environment configuration, and connected project documentation for references to PDA.
- Determine whether it is an existing application, an internal portal, a partner application, a separate product, or a project codename.
- Document the verified purpose, users, workflows, data dependencies, and access permissions.
- Preserve any existing PDA functionality.
- Do not invent the meaning of PDA or create unrelated functionality merely to satisfy the acronym.
- If its purpose cannot be established, build only the reusable platform foundations that are independent of that decision.

---

# 1. EXECUTION PROTOCOL

## Phase 0: Repository audit

Before modifying code, inspect:

- Repository structure and existing project instructions.
- Supported framework and runtime versions.
- Frontend components, routes, layouts, styling system, and assets.
- Backend services, API endpoints, database schema, and migrations.
- Authentication, sessions, permissions, and user profiles.
- Numerology calculators, report generation, and AI functionality.
- Existing RAG implementation, model providers, embedding providers, vector indexes, and knowledge sources.
- CMS or content storage, SEO metadata, structured data, sitemap, and robots.txt.
- Existing payment gateway, order state machine, subscriptions, and webhooks.
- Analytics, event tracking, consent handling, and monitoring.
- Hosting, CI/CD, environment variables, secrets, backup procedures, and deployment scripts.
- Existing automated tests, known defects, performance issues, and accessibility issues.
- Website, customer app, and PDA integration boundaries.

### Required audit deliverables

Create or update these documents in the repository, adapting filenames if project conventions require it:

- `docs/audit/current-state.md`
- `docs/audit/architecture-map.md`
- `docs/audit/seo-baseline.md`
- `docs/audit/security-review.md`
- `docs/audit/known-risks.md`
- `docs/implementation/implementation-plan.md`
- `docs/implementation/acceptance-criteria.md`
- `docs/implementation/rollback-plan.md`

Do not claim that live URLs, analytics, third-party accounts, or external systems were inspected unless access was available and the inspection actually occurred.

## Phase 1: Establish the baseline

1. Run the existing build, lint, type checks, and tests.
2. Record failures before making changes.
3. Capture the current routes and page inventory.
4. Record the current database schema and migration state.
5. Identify all existing customer-facing features.
6. Identify missing environment configuration without printing secret values.
7. Record existing performance and SEO findings.
8. Create a recoverable branch or checkpoint according to the repository workflow.

Separate pre-existing defects from regressions introduced during implementation.

## Phase 2: Produce the dependency-aware plan

Create a task list with:

- Task ID.
- Description.
- Relevant files or modules.
- Dependencies.
- Risk classification.
- Acceptance criteria.
- Tests required.
- Status.
- Rollback approach.

Prioritise security and data integrity, calculation correctness, technical SEO, core user journeys, payment reliability, and production stability.

Proceed in small, reviewable changes. Do not rewrite the whole application in one unverified operation.

---

# 2. TARGET PLATFORM ARCHITECTURE

Implement the following logical architecture using the existing stack wherever practical.

```text
NUMEROS VISION PLATFORM
|
+-- PUBLIC WEBSITE
|   +-- Homepage and brand pages
|   +-- Learning and SEO content
|   +-- Free calculators
|   +-- Report and pricing pages
|   +-- Public methodology and trust pages
|
+-- CUSTOMER APPLICATION
|   +-- Authentication and profiles
|   +-- Numerology calculators
|   +-- Lo Shu grid
|   +-- Charm AI
|   +-- Personalised reports
|   +-- Purchase history and account settings
|
+-- PDA
|   +-- Discover and preserve existing purpose
|   +-- Implement verified workflows
|   +-- Apply role-based permissions
|
+-- SHARED APPLICATION SERVICES
|   +-- Deterministic calculation engine
|   +-- Versioned report engine
|   +-- Governed RAG and AI services
|   +-- Content and SEO services
|   +-- Payment and order services
|   +-- Identity and access services
|   +-- Analytics and audit logging
|
+-- DATA AND INFRASTRUCTURE
    +-- Existing relational or document database
    +-- Object storage for private reports
    +-- Search and vector retrieval
    +-- Background job processing
    +-- Monitoring, backups, and recovery
```

## Architectural requirements

- Reuse the existing framework, database, authentication system, and deployment platform if they meet requirements.
- Avoid unnecessary microservices for functionality that can be implemented safely within the existing application.
- Separate domain logic from UI components.
- Use versioned API contracts.
- Validate all external inputs.
- Apply server-side authorisation to sensitive operations.
- Use transactions and idempotency for payment and report workflows.
- Keep secrets server-side.
- Use background jobs for expensive report generation and bulk content operations.
- Implement retries with limits, timeouts, and observable failure states.
- Avoid introducing additional infrastructure without documenting its cost, benefit, and operational requirements.

---

# 3. BRAND, UI/UX, AND DESIGN SYSTEM

## Brand requirements

- Brand name: Numeros Vision.
- Tagline: Unveil Every Charm.
- Preserve the original logo asset and proportions.
- Do not redraw, replace, crop, or regenerate the official logo without authorisation.
- Use the existing established brand palette and visual theme.
- Where new visual elements are necessary, use the existing design system rather than introducing an unrelated theme.
- Ensure that decorative artwork never substitutes for real calculator outputs, tables, or report data.

## Shared design system

Audit and document:

- Colour tokens.
- Typography scale.
- Spacing scale.
- Responsive breakpoints.
- Container widths.
- Buttons and form fields.
- Navigation and mobile menus.
- Cards, accordions, tables, and tooltips.
- Loading, empty, success, and error states.
- Focus, hover, disabled, and validation states.
- Accessibility requirements.
- Shared page header and footer.

Implement reusable components according to the conventions already used by the project.

## Page consistency

Every public page must use the same shared design system.

Do not implement individual pages with conflicting typography, inconsistent margins, unrelated button styles, or duplicated headers.

## Accessibility

Target WCAG 2.2 AA where applicable.

Verify:

- Keyboard navigation.
- Visible focus indicators.
- Semantic headings and landmarks.
- Labelled inputs and accessible errors.
- Appropriate contrast.
- Screen-reader descriptions.
- Accessible dialogs and navigation.
- Reduced-motion preferences.
- Accessible PDF structure where supported.

---

# 4. WEBSITE ROUTES AND PAGE INVENTORY

First inventory existing URLs. Merge this proposed sitemap with the real product instead of blindly creating duplicate pages.

## Brand and trust pages

- `/`
- `/about`
- `/methodology`
- `/how-it-works`
- `/contact`
- `/privacy-policy`
- `/terms`
- `/refund-policy`
- `/disclaimer`

## Calculator and tool pages

Create or retain routes only where the corresponding functionality exists or is approved.

- `/numerology/name-calculator`
- `/numerology/birth-date-calculator`
- `/numerology/driver-conductor`
- `/numerology/lo-shu-grid`
- `/numerology/chaldean`
- `/numerology/pythagorean`

## Learning and topical hubs

- `/learn/numerology`
- `/learn/chaldean-numerology`
- `/learn/pythagorean-numerology`
- `/learn/number-meanings`
- `/learn/driver-and-conductor-numbers`
- `/learn/lo-shu-grid`
- `/learn/name-numerology`
- `/learn/business-name-numerology`
- `/learn/numerology-compatibility`

These are candidate routes, not verified current routes. Confirm search intent, content quality, and differentiation before creating each URL.

## Commercial pages

- `/reports`
- `/reports/basic`
- `/reports/advanced`
- `/reports/premium`
- `/pricing`
- `/sample-report`
- `/checkout`

Confirm existing report names, pricing, currency, contents, and entitlements before exposing commercial information.

## Application routes

Use the existing route conventions and protect authenticated pages.

Potential route groups include:

- `/app`
- `/app/calculators`
- `/app/profiles`
- `/app/reports`
- `/app/history`
- `/app/charm-ai`
- `/app/settings`

Do not index private reports, customer-specific calculation results, account pages, checkout sessions, or administrative interfaces as public landing pages.

---

# 5. TECHNICAL SEO IMPLEMENTATION

## 5.1 SEO metadata model

Implement a central metadata utility or equivalent framework-native mechanism.

Each indexable page should support:

- Unique title.
- Unique description.
- Canonical URL.
- Robots directives.
- Open Graph metadata.
- Social-sharing image.
- Page-specific structured data.
- Language metadata where applicable.
- Breadcrumbs where appropriate.
- Sitemap eligibility.
- Last-modified metadata where accurate.

Never use a single generic title or description across every page.

## 5.2 Illustrative TypeScript metadata contract

Adapt this code to the existing stack. Do not add TypeScript if the repository uses a different language without justification.

```ts
export type SeoPageConfig = {
  path: string;
  title: string;
  description: string;
  indexable: boolean;
  canonicalPath?: string;
  ogImage?: string;
  pageType: "website" | "article" | "calculator" | "product";
  modifiedAt?: string;
};

export function validateSeoConfig(config: SeoPageConfig): string[] {
  const errors: string[] = [];

  if (!config.path.startsWith("/")) {
    errors.push("Page path must be an internal absolute path.");
  }

  if (!config.title.trim()) {
    errors.push("SEO title is required.");
  }

  if (!config.description.trim()) {
    errors.push("Meta description is required.");
  }

  if (
    config.modifiedAt &&
    Number.isNaN(Date.parse(config.modifiedAt))
  ) {
    errors.push("modifiedAt must be a valid date.");
  }

  if (config.indexable && config.path.startsWith("/app/")) {
    errors.push("Private application routes must not be indexable by default.");
  }

  return errors;
}
```

This is a starting contract. Implement route-aware exceptions for any genuinely public application content.

## 5.3 Title and description rules

Use the following as editorial guidance, not rigid Google ranking rules.

- Titles should describe the page accurately and distinctly.
- Put the central topic near the beginning where it reads naturally.
- Include the brand where useful.
- Avoid repetitive keyword patterns.
- Draft descriptions that explain the page's benefit and next step.
- Avoid duplicate titles and descriptions.
- Do not force exact character counts when the result becomes unnatural.
- Validate rendered metadata on production HTML, not merely in the source component.

## 5.4 Heading rules

- Use a descriptive primary page heading.
- Organise H2 and H3 headings by actual content hierarchy.
- Do not use headings solely to manipulate search engines.
- Avoid empty or duplicated headings.
- Keep heading order accessible.
- Do not place important page text exclusively inside images.

## 5.5 Canonical URLs

Implement a consistent canonicalisation policy covering:

- Trailing slash conventions.
- HTTP to HTTPS.
- Hostname variations.
- Query parameters.
- Duplicate category and pagination routes.
- Tracking parameters.
- Redirected or consolidated URLs.
- Language and regional variants.

Do not canonicalise unrelated pages to the homepage.

Every canonical target must be a valid, accessible URL representing the intended page.

## 5.6 Sitemap and robots.txt

Generate the XML sitemap from verified, public, canonical URLs.

Exclude:

- Private account routes.
- Internal administration routes.
- Checkout and temporary session URLs.
- Duplicate URLs.
- Pages intentionally excluded from indexing.
- Invalid or redirected destinations.

Illustrative `robots.txt`:

```text
User-agent: *
Disallow: /admin/
Disallow: /app/
Disallow: /checkout/

Sitemap: https://YOUR-VERIFIED-DOMAIN/sitemap.xml
```

Replace the placeholder with the verified production domain. Adapt disallow rules to the actual route structure.

Important: robots.txt is not an access-control system and does not guarantee that a URL will stay out of search results. Use authentication and appropriate indexing controls for private content.

## 5.7 Internal links

Implement a page relationship registry or equivalent content model.

Each page should declare:

- Parent topic or hub.
- Related pages.
- Relevant calculator links.
- Relevant report links.
- Breadcrumb hierarchy.
- Incoming and outgoing link coverage.

Use contextual links that help users understand the destination. Do not impose an arbitrary minimum of links on every page.

Add automated checks for:

- Broken internal links.
- Orphaned important pages.
- Redirect chains.
- Incorrect anchor destinations.
- Links to private or unpublished pages.

## 5.8 Structured data

Use JSON-LD when appropriate and supported by the actual content.

Candidate types include:

- `Organization`
- `WebSite`
- `WebPage`
- `BreadcrumbList`
- `Article`
- `BlogPosting`
- `Product`
- `SoftwareApplication`

Choose only relevant types. Validate every field against visible content and the applicable search engine guidelines.

Do not fabricate:

- Ratings.
- Reviews.
- Prices.
- Author identities.
- Publication dates.
- Availability.
- Product offers.
- FAQ content.

Do not add FAQ schema merely because a page contains a list of questions.

## 5.9 Example JSON-LD

Use a verified configuration and the actual page data model to produce JSON-LD safely.

```ts
type OrganizationSchemaInput = {
  name: string;
  url: string;
  logoUrl?: string;
};

export function buildOrganizationJsonLd(
  input: OrganizationSchemaInput
) {
  const data: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: input.name,
    url: input.url
  };

  if (input.logoUrl) {
    data.logo = input.logoUrl;
  }

  return data;
}
```

Render the output using the framework's safe structured-data mechanism. Escape data correctly, validate URLs, and prevent user-provided content from becoming executable HTML.

## 5.10 Search engine integrations

Implement or document the setup for:

- Google Search Console.
- Bing Webmaster Tools.
- XML sitemap submission.
- URL inspection and indexing diagnostics.
- Supported search performance APIs.
- Optional third-party keyword research connectors.

Use real authorised credentials and documented APIs. Never claim indexing, ranking, or search engine acceptance is guaranteed.

---

# 6. IMAGE OPTIMISATION AND CONTENT ASSETS

Build a repeatable image pipeline.

For every image:

1. Record its purpose and source.
2. Preserve the original where required.
3. Generate responsive derivatives in suitable modern formats.
4. Compress without unacceptable quality loss.
5. Use descriptive filenames.
6. Write meaningful alt text for informative images.
7. Use empty alt text for purely decorative images where appropriate.
8. Define image dimensions.
9. Lazy-load below-the-fold assets.
10. Avoid unnecessarily delaying the main hero image.
11. Generate social-sharing derivatives when needed.
12. Test loading, layout shift, accessibility, and visual quality.

Do not enforce an absolute 100 KB maximum for all images. Use performance budgets based on image role, device, page weight, and measured experience.

Do not use AI-generated artwork as a substitute for actual calculator results, precise tables, logos, or report values.

Maintain an asset registry with source, licence, dimensions, format, alt text, page association, and optimisation status.

---

# 7. KEYWORD RESEARCH AND CONTENT REGISTRY

Create or update a central keyword-to-page registry.

The existing research history refers to 433 usable keyword entries from a larger 1,288-row dataset. Treat these counts as historical inputs to reconcile against the actual available files, not as verified current market demand.

For every keyword cluster, record:

```ts
type KeywordRecord = {
  clusterId: string;
  primaryTopic: string;
  relatedQueries: string[];
  intent:
    | "informational"
    | "commercial"
    | "transactional"
    | "navigational";
  funnelStage: string;
  targetPath?: string;
  competingPaths: string[];
  source: string;
  researchDate?: string;
  status: "planned" | "mapped" | "published" | "review";
};
```

## Keyword assignment rules

- Assign one primary intent to each target page.
- Group closely related terms when the same page can satisfy them.
- Do not create separate pages for every minor keyword variation.
- Flag potential keyword cannibalisation.
- Verify existing pages before proposing replacements.
- Use live keyword metrics only when obtained from an authorised, identifiable source.
- Never invent search volume, keyword difficulty, CPC, ranking position, or traffic estimates.

## Content hub structure

Organise content around:

1. Numerology fundamentals.
2. Name numerology.
3. Birth-date numerology.
4. Chaldean and Pythagorean methods.
5. Driver and conductor calculations.
6. Lo Shu grid interpretation.
7. Compatibility and business naming.
8. Calculators and interactive tools.
9. Report products and methodology.

Each hub must have a clear purpose and links to relevant supporting pages, calculators, and products.

---

# 8. AI CONTENT GENERATION AND APPROVAL

Implement an auditable content workflow.

```text
Research inputs
    |
    v
Keyword classification
    |
    v
Existing URL and duplicate check
    |
    v
Structured content brief
    |
    v
Approved source retrieval
    |
    v
Draft generation
    |
    v
Claim and citation validation
    |
    v
SEO, accessibility and originality checks
    |
    v
Image and internal-link review
    |
    v
Human approval
    |
    v
CMS publication
    |
    v
Search and conversion monitoring
```

## Content brief schema

```ts
type ContentBrief = {
  targetPath: string;
  primaryTopic: string;
  searchIntent: string;
  audience: string;
  questionsToAnswer: string[];
  requiredSources: string[];
  internalLinkTargets: string[];
  requiredExamples: string[];
  prohibitedClaims: string[];
  reviewerRequired: boolean;
};
```

## Content quality rules

- Answer the main question directly.
- Provide useful context, worked examples, and clear explanations.
- Cite sources for sourced factual claims.
- Distinguish documented methodology from interpretation or belief.
- Avoid repetitive filler and mass-produced thin pages.
- Do not copy protected source material beyond permitted use.
- Do not invent personal experience, credentials, reviews, or case studies.
- Do not claim a page is expert-reviewed unless it actually was.
- Keep a version history of published content.
- Compare new drafts against the current version before overwriting it.

## Publication gate

Require the following before publication:

- Correct target URL.
- No unintended duplicate page.
- Approved source material.
- No unresolved critical factual claims.
- Correct metadata and canonical.
- Relevant internal links.
- Valid assets and image text alternatives.
- Appropriate schema.
- Correct mobile rendering.
- Successful automated checks.
- Human approval.

Initially, keep publication human-approved. Expand automation only after the workflow demonstrates reliable quality.

---

# 9. DETERMINISTIC NUMEROLOGY ENGINE

The calculation engine must be independent of the language model.

## 9.1 Required modules

Audit existing implementations first. Retain working and validated modules.

Potential modules include:

- Chaldean/Cheiro name calculations.
- Pythagorean name calculations.
- Birth-date calculations.
- Driver and conductor calculations.
- Lo Shu grid generation.
- Present and missing number analysis.
- Name-to-owner compatibility scoring.
- Brand name evaluation.
- Versioned report generation.

Astrology modules must be treated separately and implemented only where their formula specifications, astronomical data requirements, and validation references are established.

## 9.2 Calculation contract

Every calculation must declare:

- Method identifier.
- Method version.
- Input validation rules.
- Normalisation rules.
- Calculation steps.
- Reduction and exception rules.
- Output schema.
- Known-answer fixtures.
- Edge-case tests.
- Source or specification reference.

Do not silently replace established project rules with a generic interpretation.

Where historical project specifications define a particular formula, compare it with the actual implementation and preserve it unless a documented decision approves a change.

## 9.3 Example result contract

```ts
type CalculationResult<T> = {
  methodId: string;
  methodVersion: string;
  inputHash: string;
  values: T;
  trace: Array<{
    step: string;
    result: string | number;
  }>;
  validationStatus: "passed" | "failed" | "review";
  specificationVersion: string;
};
```

The `inputHash` must be generated using a suitable, documented approach. Do not expose sensitive raw input in the hash metadata or logs unnecessarily.

## 9.4 Validation pipeline

```text
Validate input
    |
    v
Resolve calculation method and version
    |
    v
Run deterministic calculation
    |
    v
Compare against known-answer tests
    |
    v
Validate output and invariants
    |
    v
Store reproducibility metadata
    |
    v
Pass structured output to explanation layer
```

## 9.5 Test requirements

Create fixtures for:

- Normal valid inputs.
- Empty and malformed inputs.
- Different character sets.
- Spaces and punctuation.
- Repeated letters.
- Boundary dates.
- Leap days where relevant.
- Master-number or compound-number handling where specified.
- Missing and present Lo Shu values.
- Conflicting or unsupported calculation rules.
- Regression cases from the existing production implementation.

Do not invent expected outputs. Derive fixtures from an approved specification and independently verified examples.

The same input, method, and version must return the same result.

---

# 10. RAG AND CHARM AI

## 10.1 Knowledge source registry

Maintain metadata for every source:

- Source ID.
- Title.
- Author or publisher.
- Source URL or file reference.
- Method or topic.
- Version and publication date where available.
- Rights and permitted usage.
- Review status.
- Extraction status.
- Approved retrieval scope.
- Last verification date.

Include the previously identified numerology and astrology reference materials only after their exact editions or files are located, their contents are verified, and their usage rights are reviewed.

Do not invent source passages or citations.

## 10.2 Ingestion pipeline

```text
Approved source
    |
    v
File type and integrity validation
    |
    v
Text extraction and OCR where necessary
    |
    v
Structure and metadata preservation
    |
    v
Semantic chunking
    |
    v
Embedding generation
    |
    v
Search index and vector index
    |
    v
Retrieval evaluation
```

Keep source identifiers and relevant page, section, or heading references attached to chunks.

## 10.3 Retrieval and generation pipeline

```text
User request
    |
    v
Input and permission validation
    |
    v
Method and intent identification
    |
    v
Deterministic calculation when applicable
    |
    v
Retrieve approved evidence
    |
    v
Rank and filter evidence
    |
    v
Generate structured explanation
    |
    v
Validate claims and citations
    |
    v
Apply safety and output checks
    |
    v
Return answer or request clarification
```

## 10.4 Claim ledger

Represent claims explicitly.

```ts
type ClaimRecord = {
  claimId: string;
  text: string;
  claimType:
    | "calculation"
    | "source_fact"
    | "interpretation"
    | "unknown";
  sourceIds: string[];
  calculationReference?: string;
  validationStatus:
    | "validated"
    | "unverified"
    | "rejected";
};
```

Rules:

- Calculation claims must reference validated calculation results.
- Source facts must reference retrieved approved material.
- Interpretations must be identified as interpretations.
- Unknowns must not be presented as verified facts.
- Conflicting sources must trigger a conflict state.
- Missing evidence must trigger a limitation or clarification response.

## 10.5 Output validation

Validate model output against an explicit schema before displaying it.

Reject or repair outputs that:

- Contain malformed JSON where structured JSON is required.
- Invent citation identifiers.
- Refer to nonexistent calculations.
- Claim unsupported certainty.
- Contradict validated input values.
- Expose restricted source documents.
- Contain prohibited personal data.
- Violate report length or section requirements.

Use bounded retries. If validation fails repeatedly, return a controlled error rather than presenting the failed result as correct.

## 10.6 RAG evaluation suite

Create a versioned test dataset with approved expected behaviour.

Measure:

- Retrieval relevance.
- Source coverage.
- Citation correctness.
- Answer support by retrieved evidence.
- Calculation consistency.
- Unsupported claim rate.
- Conflict handling.
- Refusal and clarification behaviour.
- Latency.
- Cost per successful request.

Do not invent baseline scores or declare the RAG system accurate merely because it returns fluent answers.

---

# 11. CUSTOMER APP AND REPORTS

## Customer functionality

Preserve and improve existing features for:

- Calculator input and results.
- User profiles and calculation history.
- Lo Shu visualisation.
- Method-specific explanations.
- Charm AI.
- Report creation and access.
- Payment and purchase history.
- Language and accessibility settings.
- Privacy controls.

Use the same deterministic calculation service for the website and app.

## Report architecture

```text
Validated inputs
    |
    v
Calculation result snapshot
    |
    v
Approved report template
    |
    v
Evidence-grounded interpretation
    |
    v
Section and citation validation
    |
    v
PDF generation
    |
    v
Rendering and integrity checks
    |
    v
Secure report storage
    |
    v
Authorised customer access
```

## Report requirements

- Preserve the approved Basic, Advanced, and Premium product definitions.
- Verify prices and included sections from the actual product configuration.
- Use reusable templates.
- Include the applicable calculation method and version.
- Include relevant limitations and disclaimers.
- Prevent access to another customer's report.
- Use expiring download links where appropriate.
- Track generation failures and retries.
- Make report regeneration reproducible.
- Test fonts, pagination, Unicode, tables, long inputs, and page breaks.

Do not create paid features that are not backed by implemented functionality.

---

# 12. PDA IMPLEMENTATION

First establish the verified purpose of PDA from the repository and business requirements.

If PDA is an existing application, retain its functionality and integrate it through documented APIs.

If PDA is a confirmed administrative or operational portal, consider the following modules only where they match actual needs:

- Overview and operational metrics.
- User and role management.
- Content review and publication approvals.
- Knowledge-source management.
- Report job monitoring.
- Payment exception handling.
- Audit logs.
- Integration health.

## Access control

- Define explicit roles and permissions.
- Check permissions on the server.
- Separate administrative and customer access.
- Protect sensitive exports.
- Log privileged changes.
- Use stronger authentication for privileged roles.
- Prevent cross-tenant and cross-account data access.
- Use synthetic data for demonstrations and automated tests.

Do not enable unverified modules simply because they appear in this specification.

---

# 13. PAYMENT AND MONETISATION

Implement payments through an adapter compatible with the actual selected provider.

## Order lifecycle

```text
Checkout initiated
    |
    v
Pending order created server-side
    |
    v
Payment provider processes payment
    |
    v
Signed callback/webhook verified
    |
    v
Idempotent order state transition
    |
    v
Report generation queued
    |
    v
Report successfully generated
    |
    v
Customer notified and authorised
```

## Payment rules

- Do not trust browser redirects as proof of payment.
- Verify webhook signatures.
- Enforce idempotency.
- Keep payment credentials server-side.
- Store provider transaction references, not unnecessary sensitive payment details.
- Handle pending, failed, successful, refunded, and disputed states.
- Do not generate duplicate paid reports for repeated webhook deliveries.
- Reconcile payment status with provider records.
- Apply access entitlements based on verified order state.
- Document refund and chargeback behaviour.

Verify actual provider capabilities, fees, settlement requirements, supported currencies, UPI availability, and recurring billing before selecting or changing a provider.

Do not hard-code prices or assume merchant eligibility.

---

# 14. ANALYTICS AND MEASUREMENT

Implement privacy-conscious event tracking using the existing analytics system where available.

## Search and content metrics

- Search impressions.
- Organic clicks.
- CTR.
- Query and landing-page performance.
- Indexing errors.
- Content updates and approval history.
- Internal-link defects.

## Product funnel

- Calculator start.
- Calculator completion.
- Result view.
- Report offer view.
- Checkout start.
- Verified purchase.
- Report generation success.
- Refund.
- Subscription status where applicable.

## AI and reliability

- Request count.
- Retrieval success.
- Validation failure.
- Latency.
- Token usage and cost.
- Report generation failures.
- Payment exceptions.
- API error rates.

Use consistent event names and documented schemas.

Do not place raw birth dates, names, report contents, passwords, payment credentials, or other sensitive personal inputs in analytics event payloads.

Revenue must be derived from verified order records. Do not use checkout button clicks as proof of revenue.

---

# 15. SECURITY AND PRIVACY

Apply secure coding practices appropriate to the actual stack.

Required controls include:

- Server-side authorisation.
- Input validation and output encoding.
- Protection against injection and cross-site scripting.
- CSRF protection where applicable.
- Secure authentication and session management.
- Rate limiting and abuse controls.
- Secret management.
- Dependency and vulnerability checks.
- Secure file upload and PDF storage.
- Signed or otherwise verified payment callbacks.
- Audit logging.
- Backup and restoration tests.
- Data minimisation and retention rules.
- Consent-aware analytics.
- Account export and deletion workflows.
- Appropriate privacy notices.
- Secure handling of model-provider data.

For AI integrations, document which data is sent to which provider, retention behaviour, and any training or processing terms.

Do not add advertising identifiers, location tracking, or third-party data sharing without a documented purpose, required consent, and applicable legal review.

---

# 16. PERFORMANCE AND CORE WEB VITALS

Measure actual page performance on mobile and desktop.

Targets for good Core Web Vitals at the 75th percentile:

- LCP: 2.5 seconds or less.
- INP: 200 milliseconds or less.
- CLS: 0.1 or less.

Implement and validate:

- Responsive image sizes.
- Appropriate image formats and compression.
- Correct width and height attributes.
- Reduced unnecessary JavaScript.
- Code splitting where useful.
- Font loading optimisation.
- Caching appropriate to the page's privacy and freshness.
- Server-side rendering or static generation where appropriate.
- Efficient database queries.
- Controlled background processing.
- Appropriate CDN usage where available.

Do not cache personalised reports or authenticated API responses publicly.

Use lab performance tests for debugging and field data for real-user assessment where available. Do not claim field thresholds have passed without field evidence.

---

# 17. TESTING REQUIREMENTS

## Unit tests

Test:

- Calculation methods.
- Input validation.
- SEO metadata generation.
- Canonical URL resolution.
- Structured-data generation.
- Payment state transitions.
- Report template rendering.
- Permission checks.
- Content publication rules.
- Claim validation.

## Integration tests

Test:

- Frontend to backend contracts.
- Backend to database.
- Calculation engine to report generation.
- RAG retrieval to claim validation.
- Payment provider callbacks.
- Content publishing and sitemap updates.
- Account access and report ownership.
- PDA workflows where confirmed.

## End-to-end tests

Test the following customer journeys:

1. Open a public landing page.
2. Complete a free calculator.
3. Verify the result and method explanation.
4. Navigate to a relevant report offer.
5. Complete registration where required.
6. Execute payment using a sandbox or test mode.
7. Verify the resulting order state.
8. Generate and download the report.
9. Reopen the report from purchase history.
10. Verify unauthorised access is rejected.

Also test failed payments, duplicate callbacks, report failures, invalid inputs, expired links, and unauthorised access.

## Regression tests

After every material change:

- Run the existing test suite.
- Run the build.
- Run lint and type checks where supported.
- Test affected routes.
- Check database migration behaviour.
- Compare critical customer journeys against the baseline.

Report actual results and remaining failures.

---

# 18. AUTOMATED SEO QUALITY GATE

Create a reusable validation command or CI job that checks public pages.

Illustrative acceptance logic:

```ts
type PageAudit = {
  url: string;
  title: string;
  description: string;
  canonical: string;
  statusCode: number;
  indexable: boolean;
  hasMainHeading: boolean;
  brokenInternalLinks: number;
  schemaErrors: number;
};

export function evaluatePage(page: PageAudit): string[] {
  const errors: string[] = [];

  if (page.statusCode !== 200) {
    errors.push("Expected a successful response for an indexable page.");
  }

  if (!page.title.trim()) {
    errors.push("Missing title.");
  }

  if (!page.description.trim()) {
    errors.push("Missing description.");
  }

  if (!page.canonical.trim()) {
    errors.push("Missing canonical URL.");
  }

  if (!page.hasMainHeading) {
    errors.push("Missing main heading.");
  }

  if (page.brokenInternalLinks > 0) {
    errors.push("Broken internal links detected.");
  }

  if (page.schemaErrors > 0) {
    errors.push("Structured-data validation errors detected.");
  }

  return errors;
}
```

Extend this according to the actual test framework.

Additional checks:

- Duplicate title detection.
- Canonical conflicts.
- Unintended `noindex`.
- Missing image alternatives.
- Invalid sitemap entries.
- Redirect chains.
- Broken internal links.
- Unintended private-page exposure.
- Schema mismatch.
- Invalid metadata.
- Missing consent controls where required.
- Broken mobile layouts.

Do not use arbitrary keyword density or a third-party SEO score as a substitute for factual, technical, and user-experience validation.

---

# 19. DEPLOYMENT AND MIGRATION

## Environment separation

Use separate development, staging, and production configurations.

Never commit real credentials.

Document required configuration using a safe environment template.

Illustrative `.env.example`:

```dotenv
APP_ENV=development
APP_BASE_URL=
DATABASE_URL=
AUTH_SECRET=
AI_PROVIDER=
AI_API_KEY=
EMBEDDING_PROVIDER=
EMBEDDING_API_KEY=
VECTOR_STORE_URL=
PAYMENT_PROVIDER=
PAYMENT_SECRET_KEY=
PAYMENT_WEBHOOK_SECRET=
STORAGE_BUCKET=
ANALYTICS_ID=
```

These are illustrative names, not verified environment variables. Map them to the actual stack and integration contracts.

Do not print real secret values during configuration checks.

## Migration procedure

1. Inventory existing database structures and dependencies.
2. Back up production data.
3. Verify that the backup can be restored.
4. Create reviewed, versioned migrations.
5. Test migrations on staging data.
6. Check compatibility with the existing application.
7. Apply migrations using the documented release process.
8. Verify critical records and relationships.
9. Monitor for errors.
10. Maintain a tested recovery plan.

Never delete or transform existing customer data without a reviewed migration and explicit approval.

## Production deployment

Production deployment requires explicit authorisation.

Before release:

- Confirm tests pass.
- Review the change set.
- Verify environment configuration.
- Verify database migrations.
- Confirm backup and rollback readiness.
- Check authentication and permissions.
- Validate critical SEO routes.
- Validate payment sandbox and production configuration separately.
- Confirm monitoring and error reporting.

After release:

- Smoke-test critical routes.
- Verify calculator outputs.
- Verify payment and report workflows.
- Inspect server and client errors.
- Confirm sitemap and canonical responses.
- Monitor latency and failures.
- Document the deployed version.

If a critical regression occurs, execute the approved rollback plan.

---

# 20. THIRTY-DAY IMPLEMENTATION PLAN

This is a proposed delivery sequence, not a promise that all changes will be safely completed within thirty calendar days.

## Days 1–3: Audit

- Inspect the repository and existing product.
- Establish the technical and SEO baseline.
- Identify the actual meaning and scope of PDA.
- Document risks and dependencies.
- Create the implementation plan.

## Days 4–6: Architecture and SEO foundation

- Define shared page metadata.
- Map existing routes.
- Create the keyword registry.
- Implement canonical, sitemap, robots, and redirect rules.
- Establish the shared UI component strategy.

## Days 7–10: Website and technical quality

- Fix priority technical SEO defects.
- Improve high-value landing pages.
- Implement structured data where appropriate.
- Add internal-link and image validation.
- Add automated SEO tests.

## Days 11–15: Calculators

- Audit existing calculation logic.
- Document supported formulas.
- Create known-answer fixtures.
- Implement regression tests.
- Standardise result contracts across website and app.

## Days 16–20: RAG and reports

- Audit source documents and retrieval.
- Implement source metadata and provenance.
- Add claim validation.
- Improve report templates and PDF rendering.
- Test unsupported and conflicting evidence cases.

## Days 21–24: App and PDA

- Improve customer journeys.
- Verify account and report permissions.
- Implement confirmed PDA workflows.
- Add audit logging and operational error handling.

## Days 25–27: Payments and automation

- Validate payment state transitions.
- Test duplicate callbacks and refunds.
- Implement the approved content pipeline.
- Verify human approval and rollback for publishing.

## Days 28–30: Release readiness

- Complete regression and security tests.
- Validate mobile experience and accessibility.
- Verify staging deployment.
- Review all release gates.
- Obtain approval before production deployment.

If any critical gate fails, delay the dependent release rather than mark it complete artificially.

---

# 21. REQUIRED REPOSITORY DELIVERABLES

Adapt filenames to the existing repository conventions. Do not duplicate existing systems unnecessarily.

```text
docs/
  audit/
    current-state.md
    architecture-map.md
    seo-baseline.md
    security-review.md
    known-risks.md
  implementation/
    implementation-plan.md
    acceptance-criteria.md
    rollback-plan.md
  operations/
    deployment-runbook.md
    backup-and-recovery.md
    monitoring.md

configuration/
  seo-registry.*
  content-registry.*
  calculation-specifications.*

tests/
  unit/
  integration/
  e2e/
  fixtures/

src/
  existing-project-structure/
```

The final structure must reflect the actual framework. Do not create a parallel application or empty folders merely to match this illustrative tree.

Required outcomes:

- Working implementation.
- Tests and fixtures.
- Updated documentation.
- Reviewed migrations.
- SEO and content registries.
- Calculation specifications.
- RAG evaluation cases.
- Deployment instructions.
- Monitoring and recovery instructions.
- Evidence of acceptance tests.

---

# 22. DEFINITION OF DONE

A feature is complete only when all applicable conditions are met:

- [ ] The feature is implemented in the existing application.
- [ ] The correct UI and API integrations are connected.
- [ ] Input validation and error handling exist.
- [ ] Security and access permissions are verified.
- [ ] Automated tests pass.
- [ ] Relevant regression tests pass.
- [ ] Documentation is updated.
- [ ] No critical unresolved defects remain.
- [ ] Any required approval is recorded.
- [ ] The feature has been verified in the intended environment.

For SEO, add the relevant metadata, indexability, canonical, internal-link, structured-data, and rendered-page checks.

For numerology, add deterministic output validation and known-answer tests.

For RAG, add evidence provenance and unsupported-claim tests.

For payments, add verified callbacks, idempotency, and failure-path tests.

For production, add deployment verification and rollback readiness.

---

# 23. FINAL ANTIGRAVITY RESPONSE FORMAT

At the end of each implementation phase, report:

## A. Work completed

List the actual files and features changed.

## B. Verification

List each test, command, and its real result.

## C. Defects and blockers

List unresolved issues and why they remain unresolved.

## D. Security and data impact

Document permission changes, migration impact, external integrations, and sensitive-data considerations.

## E. SEO impact

List affected routes, metadata, schema, indexing policy, and any redirects.

## F. Deployment status

State whether changes are local, staged, or deployed. Do not claim deployment without evidence.

## G. Next actions

List the next tasks, dependencies, and approvals required.

## H. Rollback

Document how to revert the current phase safely.

---

# 24. FIRST ACTION

Begin with the repository audit and implementation plan.

Do not start by replacing the homepage, changing the design system, rebuilding the backend, inventing PDA functionality, or rewriting calculation logic.

First establish what already exists, what is working, what is broken, and what must change.

Then implement the highest-priority verified changes incrementally, run the corresponding tests, and continue through the release gates.

**Primary objective:** Deliver a reliable, discoverable, secure, evidence-grounded Numeros Vision platform that preserves the existing brand and working systems while improving website SEO, customer experience, deterministic numerology, governed AI, operational automation, monetisation, and deployment quality.

**Brand signature:** Numeros Vision | Unveil Every Charm
