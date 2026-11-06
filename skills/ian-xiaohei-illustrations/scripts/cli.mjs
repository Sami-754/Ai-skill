#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(__dirname, "..");

function readRef(filename) {
  const filePath = path.join(skillDir, "references", filename);
  if (fs.existsSync(filePath)) {
    return fs.readFileSync(filePath, "utf8");
  }
  return "";
}

function showHelp() {
  console.log(`===================================================================
  illustration — Weird, Clean English Article Illustrations
  (Aliases: xiaohei, ian-xiaohei, illustrations)
===================================================================

Usage:
  illustration <command> [arguments...]
  xiaohei <command> [arguments...]

Commands:
  prompt <theme> [options]
      Generate a production-ready 16:9 illustration prompt matching
      the strict Style DNA, color constraints, and prompt template.
      Options:
        --idea "<idea>"           Core cognitive idea / metaphor
        --structure "<type>"      Workflow | Before-after | Metaphor | Layered (default: Conceptual metaphor)
        --action "<action>"       What Xiaohei is doing (core action)
        --elements "<e1, e2...>"  Suggested visual objects / props
        --labels "<l1, l2...>"    Short English handwritten annotations (max 5)

  validate
      Run integrity tests on skill structure, frontmatter, and assets.

  dna
      Show Style DNA: line art, color palette, whitespace, and visual bans.

  ip
      Show Xiaohei character design, personality rules, and banned behaviors.

  patterns
      Show allowed composition structures (flow, contrast, state, metaphor).

  examples
      List bundled reference illustration cases and prompt templates.

  path
      Print installation path of the skill directory.

  help, --help
      Show this help message.

Skill documentation: ${skillDir}/SKILL.md
Reference guides:    ${skillDir}/references/
`);
}

function buildPrompt(args) {
  let theme = "";
  let idea = "";
  let structure = "Conceptual metaphor";
  let action = "Xiaohei is seriously participating in the main conceptual mechanism";
  let elements = "simple hand-drawn props / cognitive anchor elements";
  let labels = "Input, Mechanism, Output";

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--idea" && args[i + 1]) {
      idea = args[++i];
    } else if (arg === "--structure" && args[i + 1]) {
      structure = args[++i];
    } else if (arg === "--action" && args[i + 1]) {
      action = args[++i];
    } else if (arg === "--elements" && args[i + 1]) {
      elements = args[++i];
    } else if (arg === "--labels" && args[i + 1]) {
      labels = args[++i];
    } else if (!arg.startsWith("--") && !theme) {
      theme = arg;
    }
  }

  if (!theme) {
    console.error("Error: Please provide a theme or topic for the prompt.");
    console.error("Example: xiaohei prompt \"Trust Building\" --idea \"Trust is laid down brick by brick\"");
    process.exit(1);
  }

  if (!idea) {
    idea = theme;
  }

  const promptText = `Generate one standalone 16:9 horizontal English article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten English annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
Xiaohei, a small solid-black absurd creature with white dot eyes, tiny thin legs, blank serious expression, slightly uneven hand-drawn body shape. Xiaohei must perform the core conceptual action, not decorate the scene. Make Xiaohei serious, deadpan, and slightly bizarre, not cute.

Theme:
${theme}

Structure type:
${structure}

Core idea:
${idea}

Composition:
${action}. Keep main subject between 40%-60% of the canvas with at least 35% empty white space.

Suggested elements:
${elements}

English handwritten labels:
${labels}

Color use:
Black for main line art and Xiaohei. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Use at most 5-8 short handwritten English labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Invent a fresh visual metaphor for this specific idea. Do not use Chinese labels unless explicitly requested.`;

  console.log(promptText);
}

const args = process.argv.slice(2);
const command = args[0] || "help";

switch (command) {
  case "prompt":
    buildPrompt(args.slice(1));
    break;
  case "validate": {
    const validateScript = path.join(skillDir, "scripts", "validate-skill.mjs");
    import(validateScript);
    break;
  }
  case "dna":
    console.log(readRef("style-dna.md") || "Style DNA guide not found.");
    break;
  case "ip":
    console.log(readRef("xiaohei-ip.md") || "Xiaohei IP guide not found.");
    break;
  case "patterns":
    console.log(readRef("composition-patterns.md") || "Composition patterns guide not found.");
    break;
  case "template":
    console.log(readRef("prompt-template.md") || "Prompt template not found.");
    break;
  case "examples": {
    const examplesDir = path.join(skillDir, "assets", "examples");
    console.log(`=== Bundled Example Illustrations (${examplesDir}) ===\n`);
    if (fs.existsSync(examplesDir)) {
      const files = fs.readdirSync(examplesDir).filter(f => f.endsWith(".png"));
      files.forEach(f => console.log(`• ${f}`));
    }
    const promptsFile = path.join(skillDir, "examples", "prompts.md");
    if (fs.existsSync(promptsFile)) {
      console.log(`\n=== Prompt Patterns (${promptsFile}) ===\n`);
      console.log(fs.readFileSync(promptsFile, "utf8"));
    }
    break;
  }
  case "path":
    console.log(skillDir);
    break;
  case "help":
  case "--help":
  case "-h":
    showHelp();
    break;
  default:
    console.error(`Unknown command: ${command}`);
    showHelp();
    process.exit(1);
}
