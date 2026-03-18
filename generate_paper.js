const { Document, Packer, Paragraph, TextRun, PageBreak, HeadingLevel, AlignmentType, ImageRun } = require("docx");
const fs = require("fs");
const path = require("path");

// Change to the script directory so relative paths work
process.chdir(path.dirname(__filename));

const document = new Document({
  sections: [{
    properties: {
      page: {
        margins: {
          top: 1440,
          right: 1440,
          bottom: 1440,
          left: 1440,
        },
        size: {
          width: 12240,
          height: 15840,
        },
      },
    },
    children: [
      // TITLE PAGE
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Measuring Gendered Interruption Patterns at the Supreme Court of Canada: A Computational Analysis of AI-Generated Transcripts",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Sabrin Saide (221178603)",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Matt Aydin (220185328)",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Gobind Dhugee (221173794)",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Legal Tech Coding",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Professor Rehaag",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Winter 2026",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Osgoode Hall Law School",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // TABLE OF CONTENTS
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Table of Contents",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "1. Introduction",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2. Literature Review",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3. Methodology",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4. Results",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "5. Access to Justice Implications",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6. Critical Reflection",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "7. Conclusion",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 1: INTRODUCTION (~400 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "1. Introduction",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Interruptions in judicial proceedings represent a critical proxy for power dynamics and gender equity within the courtroom. When one speaker interrupts another, particularly in formal settings like appellate courts, such interruptions can signal dominance, authority, and control over the discourse. The question of whether gender shapes interruption patterns in judicial settings has emerged as a significant area of empirical legal scholarship, particularly following the landmark 2017 study by Jacobi and Schweers examining the United States Supreme Court. Their findings were striking: female justices experienced approximately three times as many interruptions as their male counterparts, a disparity that prompted widespread discussion about gender dynamics at the highest levels of the judiciary.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Yet a significant gap has persisted in this research landscape. No equivalent computational analysis has been conducted on the Supreme Court of Canada, primarily because the SCC has not historically published transcripts of oral arguments. This limitation prevented researchers from examining gendered interruption patterns in the Canadian judicial context, leaving an important question unanswered: do the gender disparities documented in the American context replicate at Canada's highest court? This absence is particularly significant given documented differences between the SCC and SCOTUS, including bilingual proceedings and distinct procedural traditions.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This gap was transformed by the obiter.ai project, spearheaded by Wallace, which deployed artificial intelligence tools—specifically Whisper for speech-to-text transcription and Pyannote for speaker diarization—to generate transcripts for 121 SCC oral hearings spanning January 2020 through November 2022. This watershed moment made previously inaccessible judicial speech data available for empirical analysis.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This paper presents the first computational analysis of gendered interruption patterns at the Supreme Court of Canada. Using three complementary methods to detect interruptions—overlap detection, timing-based thresholds, and rapid judicial intervention criteria—we analyze 2,249 interruptions across 121 cases. We validate our detection pipeline through both manual review of stratified random samples and LLM-assisted classification that distinguishes hostile, clarifying, and procedural interruptions. We further examine the impact of COVID-19 hearing mode shifts on interruption dynamics and address whether gendered differences in speaking volume affect the analysis. Our central research question is straightforward: are female justices interrupted significantly more often than male justices at the SCC, controlling for volubility and the procedural role of the Chief Justice?",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 2: LITERATURE REVIEW (~600 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2. Literature Review",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2.1 US Supreme Court Research",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "The empirical study of gender dynamics at the US Supreme Court has flourished in recent years, with interruption serving as a key metric of participation parity. Jacobi and Schweers's 2017 analysis of oral arguments from 1990 through 2014 provided the first systematic evidence that female justices faced substantially higher interruption rates. Their finding that female justices were interrupted approximately three times as frequently as male justices received significant attention in legal academia and the broader public discourse. This work was methodologically rigorous, employing direct observation and manual coding of interruption events.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Feldman and Gill's 2019 research extended this inquiry by investigating the relationship between volubility and interruption. They demonstrated that justices who spoke more frequently (higher word counts) tended to experience fewer interruptions, suggesting that one's conversational participation level influences how others engage with one's speech. This finding is critical methodologically because it indicates that raw interruption counts may need normalization to account for differential speaking rates. Patton and Smith's 2017 work further enriched this literature by examining the linguistic content of interruptions, distinguishing between hostile and cooperative interruption types.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2.2 Canadian Context and the Wallace Watershed",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Prior to Wallace's 2023 obiter.ai project, no scholarly research had examined gendered interruption patterns at the Supreme Court of Canada. This absence reflected a fundamental constraint: the SCC did not publish transcripts of oral arguments, making systematic discourse analysis impossible. Wallace's deployment of automated transcription and speaker diarization technology fundamentally transformed this landscape, generating a dataset of 121 hearing transcripts spanning a three-year period.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2.3 Key Institutional Differences between SCC and SCOTUS",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "The Supreme Court of Canada differs from its American counterpart in several methodologically significant ways. Most notably, the SCC conducts proceedings in both French and English, creating unique challenges for transcript parsing and interruption detection. Additionally, the Chief Justice at the SCC plays an explicit procedural role in managing oral arguments, which may influence interruption patterns relative to the American context. Understanding these institutional particularities is essential for appropriate interpretation of our findings.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "2.4 Linguistic Theory of Interruptions",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Linguistic scholarship on interruption provides crucial theoretical grounding for empirical analysis. Zimmerman and West's foundational 1975 work established that interruptions could serve multiple conversational functions and that gender shaped interruption patterns in mixed-gender conversations. Tannen's 1994 analysis of gender and discourse further nuanced this understanding, arguing that what appears as interruption in formal settings may reflect culturally and gendered-shaped communication norms. This theoretical literature suggests that simple binary classifications of interruption versus non-interruption may inadequately capture the nuanced reality of conversational dynamics.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 3: METHODOLOGY (~700 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3. Methodology",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.1 Data Collection",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Our dataset comprises 121 Supreme Court of Canada oral argument transcripts generated by the obiter.ai project, spanning January 2020 through November 2022. These transcripts were produced using the Whisper automatic speech recognition system and Pyannote speaker diarization software. The temporal scope encompasses both pre-pandemic, pandemic, and early post-pandemic periods, allowing us to examine whether hearing modality (in-person, remote, hybrid) influences interruption patterns.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.2 Transcript Parsing and Gender Coding",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "We employed regular expression-based extraction to parse speaker names and associated speech segments from raw transcripts. Bilingual name resolution required custom logic to match French and English variants of judicial names. Gender was coded based on judicial rosters and public records; we recognize that binary gender classification is imperfect but proceeded with this approach given the existing composition of the court during the study period. Non-justice speakers (counsel, amicus representatives) were excluded from the analysis to maintain focus on justice-to-justice and justice-to-counsel interruption patterns.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.3 Three-Method Interruption Detection",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "We employed three complementary approaches to identify interruptions. First, overlap detection flagged instances where two speakers' speech segments overlapped temporally, indicating simultaneous speech. Second, timing-based thresholds identified cases where a second speaker commenced speech within 15 seconds of the first speaker's turn end, suggesting potential interruption of planned speech. Third, rapid judicial intervention criteria flagged instances where a justice spoke 50 or fewer words in response to another speaker's extended remarks, suggesting possible procedural intervention or interruption. These three methods capture different aspects of what might constitute an interruption in judicial discourse.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.4 Statistical Analysis",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "We computed interruption rates by normalizing raw counts to per-1,000-word units for each justice. Descriptive statistics including means, standard deviations, and medians were calculated separately by gender. We conducted Welch's t-tests and Mann-Whitney U tests to examine whether male and female justices experienced significantly different interruption rates. Effect sizes were calculated using Cohen's d. Regression analysis employed negative binomial regression to model interruption counts while controlling for volubility (word count) and Chief Justice status. Outlier identification used z-scores, with values exceeding 2.5 flagged for qualitative analysis.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.5 Hearing Mode Classification",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Hearings were classified as in-person, remote (via videoconference), or hybrid based on metadata from the obiter.ai dataset. This classification allowed us to examine whether hearing modality influenced interruption rates, particularly given the significant shift to remote proceedings during the COVID-19 pandemic.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "3.6 Validation and Quality Assurance",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "We implemented multi-stage validation to ensure accuracy of interruption detection. First, manual validation involved stratified random sampling of 30 flagged interruptions and 30 non-flagged instances from the dataset. Trained research assistants reviewed these samples, examining 5-turn context windows to assess accuracy. Precision was calculated as the proportion of algorithmically flagged items confirmed as true interruptions by human reviewers. Recall was calculated as the proportion of missed instances—items the algorithm failed to flag but that human reviewers identified as interruptions.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Second, we conducted LLM-assisted validation using GPT-4o-mini to classify flagged interruptions into three substantive categories, drawing on the linguistic literature on conversational interruptions (Zimmerman and West 1975, Tannen 1994). We defined hostile interruptions as power-asserting acts where the interrupter cuts off the speaker mid-thought to challenge, dismiss, or redirect them, conveying dominance or impatience. Clarifying interruptions involve a justice interjecting to ask a genuine question, seek elaboration, or test a legal proposition, serving the purpose of understanding the argument even if they technically cut off the speaker. Procedural interruptions involve hearing management, typically by the Chief Justice, to manage time, direct the order of speakers, or handle administrative matters. This typology is analytically important because the access-to-justice implications differ markedly depending on whether interruptions are hostile (suggesting bias) or clarifying and procedural (suggesting engaged judicial inquiry and effective case management). Of the confirmed interruptions in our LLM validation, 47 percent were clarifying, 44 percent were procedural, and only 9 percent were hostile, suggesting that the vast majority of SCC interruptions serve legitimate judicial purposes.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 4: RESULTS (~700 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4. Results",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.1 Primary Finding: No Significant Gender Difference",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "The central finding of this analysis is striking in its divergence from the US Supreme Court literature: we detect no statistically significant difference in interruption rates between male and female justices at the SCC. Male justices experienced an average of 2.58 interruptions per 1,000 words spoken, while female justices experienced 2.51 interruptions per 1,000 words. This difference is negligible and not statistically significant (Welch's t-test p = 0.92; Mann-Whitney U test p = 0.48). The effect size, as measured by Cohen's d, is 0.057, indicating trivial practical significance. These results held consistent across multiple analytical approaches, including unadjusted and regression-adjusted models.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.2 Chief Justice Outlier",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Our analysis identified one substantial outlier: Chief Justice Wagner exhibited a z-score of 2.98 for interruption rate, substantially exceeding the expected range. This outlier reflects Wagner's procedural role in managing oral arguments—Chief Justices receive and initiate more conversational turns than associate justices, and these turns are often procedural rather than substantive in nature. When we controlled for Chief Justice status in our regression models, the gender effect remained non-significant, and the Chief Justice variable emerged as a significant predictor of interruption rates. This finding underscores the importance of controlling for institutional role in analyzing judicial speech patterns.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.3 Hearing Mode and COVID-Era Effects",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "A striking and statistically significant finding emerged regarding hearing modality. In-person hearings exhibited an average interruption rate of 2.23 per 1,000 words. When the court transitioned to remote proceedings via videoconference, the interruption rate dropped to 1.53 per 1,000 words (p = 0.019). Hybrid hearings showed an even lower rate of 1.25 per 1,000 words (p = 0.036 compared to in-person). This suggests that physical co-presence facilitates or enables interruption, while remote and hybrid formats reduce overlapping speech and interruptions. The finding may reflect technical factors (delayed audio in videoconference settings) or behavioral adaptation to new communication modalities.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.4 Quantitative Scope of Analysis",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Across 121 oral argument cases, our algorithms detected 2,249 distinct interruption events. This substantial corpus enabled robust statistical inference and allows us to speak with confidence about gender-based patterns in the Canadian judiciary during this period.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.5 Gendered Word-Count Dynamics and Speaking Rates",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "An important methodological question, raised by Professor Rehaag during feedback, concerns whether there are gendered dynamics in the number of words spoken by justices. Our choice to normalize interruptions per 1,000 words (following Feldman and Gill 2019) has consequences: if male justices systematically speak more than female justices, normalization could deflate their interruption rates relative to female justices, potentially masking a raw-count difference. We investigated this question by computing average words per turn and total words per case, broken down by gender. While we observed some numerical differences in raw word counts between male and female justices, these differences were not statistically significant. More importantly, we verified our results using three independent approaches: per-1,000-word normalized rates, raw unnormalized counts, and regression models with log-transformed word count as a covariate. All three approaches yielded the same conclusion: no significant gender difference in interruption patterns. This triangulation confirms that the null gender finding is robust to the normalization choice and is not an artifact of controlling for volubility.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "4.6 Visualization of Results",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "The following figures present our key quantitative findings graphically:",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        text: "",
        spacing: { line: 480, lineRule: "auto" },
      }),
      // Embed chart: Interruptions by Gender
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "Figure 1: Interruption Rates by Justice Gender",
            font: "Times New Roman",
            size: 22,
            italics: true,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new ImageRun({
            type: "png",
            data: fs.readFileSync(path.join(__dirname, "output", "interruptions_by_gender.png")),
            transformation: { width: 450, height: 315 },
            altText: { title: "Chart", description: "Interruptions by gender", name: "chart1" },
          }),
        ],
      }),
      new Paragraph({ text: "", spacing: { line: 480, lineRule: "auto" } }),
      // Embed chart: Justice Comparison
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "Figure 2: Individual Justice Interruption Rates",
            font: "Times New Roman",
            size: 22,
            italics: true,
          }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new ImageRun({
            type: "png",
            data: fs.readFileSync(path.join(__dirname, "output", "justice_comparison.png")),
            transformation: { width: 450, height: 315 },
            altText: { title: "Chart", description: "Justice comparison", name: "chart2" },
          }),
        ],
      }),
      new Paragraph({ text: "", spacing: { line: 480, lineRule: "auto" } }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 5: ACCESS TO JUSTICE IMPLICATIONS (~500 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "5. Access to Justice Implications",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This research demonstrates how artificial intelligence technologies can render previously invisible judicial behavior visible and analyzable, fundamentally advancing access to justice in both narrow and broad senses. As Farrow (2014) argues, access to justice encompasses not only access to courts and legal representation but also access to information about how legal institutions function. For decades, the SCC's oral hearings were essentially a black box: journalists could attend in person, but the detailed, word-by-word interactions between justices and counsel were invisible to public scrutiny, to legal researchers, and to future counsel preparing to appear before the Court. The obiter.ai transcription project transformed these sealed proceedings into a dataset amenable to empirical analysis, representing a significant advance in judicial transparency.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Our finding that no statistically significant gender difference exists in interruption rates is itself valuable access to justice information. It suggests that at least on this metric, the SCC does not exhibit the gender disparities documented in the American context. This null finding can inform legal education, bar association guidance, and counsel preparation. Lawyers preparing for oral arguments at the SCC can be reassured that gender-based interruption disparities do not characterize the court.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "More concretely, counsel appearing before the SCC could utilize this methodology to study individual justice questioning patterns. Understanding whether a particular justice tends to ask clarifying versus hostile questions, and under what circumstances they interrupt, could inform strategic preparation. Legal aid organizations could analyze these data to examine whether certain types of parties—unrepresented litigants, small organizations, or marginalized communities—receive systematically different treatment in terms of judicial engagement and questioning patterns. Law societies could apply this methodology to assess whether judicial conduct in lower courts reflects bias in questioning patterns, creating a new lens for judicial conduct investigations.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Critically, the open-source nature of the obiter.ai tools democratizes legal research and reduces barriers for under-resourced legal organizations. Law school clinics, public interest organizations, and smaller firms can deploy these same transcription and analysis techniques without substantial financial investment. This stands in contrast to commercial litigation analytics platforms available only to wealthy firms, thereby reducing the information asymmetry that undermines access to justice.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Finally, transparency in judicial proceedings is itself an access to justice imperative. As Salyzyn (2012) argues in the context of gender representation in the legal profession, making patterns of inequality visible is a prerequisite for addressing them. The public has a fundamental right to understand how its highest court operates, and computational analysis of judicial behavior advances this transparency principle. Even our null finding serves access to justice: it provides empirical reassurance that at least on the dimension of interruption patterns, the SCC does not exhibit the gender disparities documented in the American context. This information has practical value for counsel preparing for SCC appearances, for law students studying appellate advocacy, and for policymakers evaluating judicial conduct standards.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 6: CRITICAL REFLECTION (~700 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6. Critical Reflection",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.1 Ethical Concerns with AI Transcription",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Automatic speech recognition systems, including Whisper, exhibit well-documented systematic biases. Recognition accuracy varies substantially by speaker accent, gender, age, and language. Non-native English speakers and speakers of regional varieties of English experience higher error rates than native speakers of standard varieties. These systematic errors raise significant ethical concerns when such technologies are deployed in legal settings where accuracy is paramount. The possibility of differential transcription error by gender or accent could skew results in ways we cannot fully characterize.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.2 Professional Implications and Judicial Independence",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Systematic analysis of individual justices' questioning patterns and interruption rates raises questions about judicial independence and professional norms. While transparency is valuable, there is a risk that quantifying judicial behavior in such granular detail could have chilling effects on judicial deliberation or create perverse incentives. Justices may modify their natural questioning patterns if aware that their behavior is being measured and compared. This raises important questions about the appropriate balance between transparency and judicial autonomy.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.3 Bilingual and Linguistic Challenges",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "The SCC's bilingual nature creates unique transcription challenges. Whisper's performance on French differs from its performance on English, and code-switching—seamless alternation between French and English within single utterances—challenges speaker diarization systems. Additionally, simultaneous interpretation segments create false overlaps in raw transcripts that must be carefully identified and excluded. These linguistic complexities mean that our interruption detection, particularly in bilingual segments, may be less reliable than in pure English segments.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.4 COVID-19 as a Confounding Variable",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Our dataset encompasses a period of substantial institutional disruption due to the pandemic. The shift from in-person to remote and hybrid hearings reflects not merely technological change but broader shifts in judicial behavior, counsel strategy, and organizational dynamics. We cannot cleanly separate hearing modality effects from period effects or from justice selection effects (which cases were heard in person versus remotely may not be random).",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.5 Limitations of Computational Approaches to Interruptions",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Tannen's 1994 work on gender and discourse reminds us that what appears as interruption in a formal setting may reflect culturally and gendered-shaped communication norms. Some individuals and groups use overlapping speech as a marker of engagement and solidarity, while others view it as rudeness. Simple computational classification of interruption versus non-interruption may inadequately capture this nuance. Our three-method approach partially addresses this concern by distinguishing between overlap, timing-based interruptions, and rapid interventions, but it remains fundamentally limited in semantic understanding of conversational intent.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.6 Systematic AI Transcript Errors and Their Implications",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "A critical concern emerges when considering the relationship between transcription accuracy and the phenomena we measure. Overlapping speech—precisely what creates interruptions—presents the most difficult acoustic environment for speech recognition. When two speakers speak simultaneously, Whisper's accuracy declines substantially, and speaker diarization becomes unreliable. This means that our interruption detection may be systematically biased in unknowable ways: we may miss interruptions in difficult acoustic environments while false-flagging ambiguous segments. Additionally, bilingual segments and diarization errors could systematically bias results if male and female justices differ in their acoustic characteristics or code-switching patterns.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.7 Generative AI Disclosure",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This research project has benefited from generative AI assistance throughout its lifecycle, from code development to analysis pipeline construction to paper drafting. We disclose this transparently because understanding the role of AI in knowledge production is crucial for evaluating research quality and potential biases. All results, code, and conclusions have been reviewed and validated by the human authors.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.8 Economic Considerations and Accessibility",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Access to transcripts and analytical tools remains economically stratified. While the obiter.ai project democratizes access relative to commercial platforms, substantial barriers remain for smaller organizations lacking technical expertise. The tools require Python programming knowledge, comfort with statistical analysis, and computational resources. Future work should focus on lowering these barriers through user-friendly interfaces and institutional support.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "6.9 Future Directions: Video-Based Analysis",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "A promising avenue for future research involves multimodal analysis of SCC proceedings using video recordings. Modern multimodal large language models such as GPT-4o, Gemini, and Claude can analyze both audio waveforms and visual cues to detect interruptions with greater precision than text-based approaches. Fed video directly, these models could identify overlapping speech from audio characteristics while simultaneously analyzing facial expressions, gestural cues, and other nonverbal signals that accompany interruptions. This approach could improve upon our current 68 percent precision and extend analytical capabilities to courts and proceedings without text transcripts, democratizing empirical judicial analysis even further.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // SECTION 7: CONCLUSION (~300 words)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "7. Conclusion",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This paper presents the first computational analysis of gendered interruption patterns at the Supreme Court of Canada, utilizing transcripts from 121 oral hearings spanning January 2020 through November 2022. Our central finding diverges markedly from documented patterns at the US Supreme Court: we detect no statistically significant difference in interruption rates between male and female justices at the SCC. Male justices experienced 2.58 interruptions per 1,000 words spoken; female justices experienced 2.51 per 1,000 words (p = 0.92, Cohen's d = 0.057). This null finding holds across multiple analytical approaches and is robust to controls for volubility and Chief Justice status.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "A second significant finding concerns hearing modality. In-person hearings exhibited substantially higher interruption rates than remote and hybrid formats, suggesting that physical co-presence facilitates interruption. This finding may reflect technical factors in videoconference communication or behavioral adaptation to new communication environments.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Yet our analysis is constrained by multiple methodological limitations. Automatic speech recognition systems exhibit systematic biases; overlapping speech presents the most difficult acoustic environment for transcription; bilingual proceedings create unique challenges; and computational classification of interruption behavior, while valuable, inevitably misses the semantic and cultural nuance that linguistic theory emphasizes. These limitations require cautious interpretation of our findings.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Nonetheless, this work advances crucial goals: it demonstrates how AI-generated transcripts can render previously invisible judicial behavior analyzable, supporting judicial transparency and access to justice. It provides the first empirical evidence about gender dynamics in interruption patterns at Canada's highest court. And it establishes methodological foundations that future researchers can extend, whether by analyzing pre-pandemic SCC hearings as they become available, by applying video-based multimodal analysis to improve detection precision beyond our current 68 percent, or by adapting these methods to provincial appellate courts. As courts increasingly adopt transparent proceedings and as AI technologies continue to improve, empirical legal scholarship will play an increasingly important role in illuminating the functioning of the judiciary and holding legal institutions accountable to principles of equality and fairness.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // REFERENCES
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "References",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Farrow, Trevor CW. 2014. \"What is Access to Justice?\" Osgoode Hall Law Journal 51(3): 957-987.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Feldman, Adam & Rebecca Gill. 2019. \"Power Dynamics in Supreme Court Oral Arguments: The Relationship between Gender and Justice-to-Justice Interruptions.\" Journal of the Legal Profession 40(7): 173-189.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Jacobi, Tonja & Dylan Schweers. 2017. \"Justice, Interrupted: The Effect of Gender, Ideology, and Seniority at Supreme Court Oral Arguments.\" Virginia Law Review 103(8): 1379-1435.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Patton, Dana & Joseph Smith. 2017. \"Lawyer, Interrupted: Gender Bias in Oral Arguments at the US Supreme Court.\" Journal of Law and Courts 5(2): 337-366.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Salyzyn, Amy. 2012. \"A New Lens: Reframing the Conversation about the Underrepresentation of Women in the Legal Profession.\" Ottawa Law Review 44(1): 129-164.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Tannen, Deborah. 1994. Gender and Discourse. Oxford: Oxford University Press.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Wallace, Simon. 2023. \"Speaking Like a Judge: An AI-Assisted Analysis of Judicial Behaviour at the Supreme Court of Canada.\" Supreme Court Law Review 115(1): 1-45.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Zimmerman, Don H. & Candace West. 1975. \"Sex Roles, Interruptions and Silences in Conversation.\" In Barrie Thorne & Nancy Henley (eds.), Language and Sex: Difference and Dominance. Rowley, MA: Newbury House.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),

      // PAGE BREAK
      new Paragraph({
        children: [new PageBreak()],
      }),

      // APPENDICES
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Appendices",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Appendix 1: Methodological Appendix",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Complete methodological documentation, data processing scripts, and statistical code are available at: https://github.com/matt-aydin-2000/scc-interruptions",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Appendix 2: Generative AI Disclosure",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This research project has utilized Claude Opus, Claude Sonnet, and other generative AI models for the following purposes: (1) assistance with Python code development for transcript parsing and statistical analysis; (2) conceptualization and refinement of the analytical pipeline; (3) drafting and revising sections of this paper. All data analysis, validation, and interpretation has been conducted by the human authors. All results have been independently verified. The final conclusions and representations in this paper are the responsibility of the authors.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "Appendix 3: Word Count Declaration",
            font: "Times New Roman",
            size: 24,
            bold: true,
          }),
        ],
      }),
      new Paragraph({
        spacing: { line: 480, lineRule: "auto" },
        children: [
          new TextRun({
            text: "This paper contains approximately 4,000 words of body text, excluding title page, table of contents, references, and appendices, as required by the assignment specifications.",
            font: "Times New Roman",
            size: 24,
          }),
        ],
      }),
    ],
  }],
});

// Ensure output directory exists
const outputDir = path.join(__dirname, "output");
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Generate and save the document
Packer.toBuffer(document)
  .then((buffer) => {
    fs.writeFileSync(path.join(outputDir, "final_paper.docx"), buffer);
    console.log("Document generated successfully at output/final_paper.docx");
  })
  .catch((err) => {
    console.error("Error generating document:", err);
    process.exit(1);
  });
