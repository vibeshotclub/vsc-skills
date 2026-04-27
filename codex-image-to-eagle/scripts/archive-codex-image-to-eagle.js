#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const http = require('http');
const os = require('os');

const DEFAULT_IMAGE_DIR = process.env.CODEX_GENERATED_IMAGES_DIR || path.join(os.homedir(), '.codex', 'generated_images');
const DEFAULT_SERVER = process.env.EAGLE_SERVER_URL || 'http://localhost:41596';
const IMAGE_EXTS = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif']);
const DEFAULT_FOLDER_NAME = 'Codex 生成图';
const DEFAULT_TAGS = ['Codex', 'AI生成', 'Prompt'];

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    return;
  }

  const imageDir = expandHome(args.imageDir || DEFAULT_IMAGE_DIR);
  const prompt = readPrompt(args);
  const tags = parseTags(args.tags);
  const dryRun = Boolean(args.dryRun);

  const imagePaths = selectImagePaths(args, imageDir);
  if (imagePaths.length === 0) {
    throw new Error(`No image files found in ${imageDir}`);
  }

  const folderIds = await resolveFolders(args, dryRun);
  const archivedAt = new Date().toISOString();
  const items = imagePaths.map((imagePath, index) => ({
    source: {
      type: 'path',
      path: imagePath,
    },
    name: args.name || buildName(imagePath, index, imagePaths.length),
    annotation: buildAnnotation(prompt, imagePath, archivedAt),
  }));

  const payload = {
    tags,
    items,
  };

  if (folderIds.length > 0) {
    payload.folders = folderIds;
  }

  if (dryRun) {
    writeJson({
      dryRun: true,
      server: DEFAULT_SERVER,
      imageDir,
      folderIds,
      payload,
    });
    return;
  }

  const result = await callTool('item_add', payload);
  writeJson({
    success: true,
    imagePaths,
    folderIds,
    tags,
    result,
  });
}

function parseArgs(argv) {
  const args = {};

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === '--help' || arg === '-h') args.help = true;
    else if (arg === '--latest') args.latest = true;
    else if (arg === '--latest-session') args.latestSession = true;
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--prompt-stdin') args.promptStdin = true;
    else if (arg.startsWith('--')) {
      const key = toCamel(arg.slice(2));
      const value = argv[i + 1];
      if (value === undefined || value.startsWith('--')) {
        throw new Error(`Missing value for ${arg}`);
      }
      args[key] = value;
      i += 1;
    }
  }

  return args;
}

function toCamel(value) {
  return value.replace(/-([a-z])/g, (_, char) => char.toUpperCase());
}

function readPrompt(args) {
  if (args.promptFile) {
    return fs.readFileSync(expandHome(args.promptFile), 'utf8').trim();
  }

  if (args.promptStdin) {
    return fs.readFileSync(0, 'utf8').trim();
  }

  return (args.prompt || '').trim();
}

function parseTags(value) {
  if (!value) return DEFAULT_TAGS;

  const raw = value.trim();
  if (raw.startsWith('[')) {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) throw new Error('--tags JSON must be an array');
    return unique([...DEFAULT_TAGS, ...parsed.map(String)]);
  }

  return unique([...DEFAULT_TAGS, ...raw.split(',').map((tag) => tag.trim()).filter(Boolean)]);
}

function selectImagePaths(args, imageDir) {
  if (args.path) {
    const imagePath = path.resolve(expandHome(args.path));
    assertImageFile(imagePath);
    return [imagePath];
  }

  if (args.latestSession) {
    const sessionDir = latestSessionDir(imageDir);
    return listImages(sessionDir).sort((a, b) => statMtimeMs(a) - statMtimeMs(b));
  }

  if (args.latest || !args.path) {
    const latest = listImages(imageDir).sort((a, b) => statMtimeMs(b) - statMtimeMs(a))[0];
    return latest ? [latest] : [];
  }

  return [];
}

function latestSessionDir(imageDir) {
  const dirs = fs.readdirSync(imageDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(imageDir, entry.name))
    .filter((dir) => listImages(dir).length > 0)
    .sort((a, b) => statMtimeMs(b) - statMtimeMs(a));

  if (!dirs[0]) throw new Error(`No session folders with images found in ${imageDir}`);
  return dirs[0];
}

function listImages(rootDir) {
  if (!fs.existsSync(rootDir)) {
    throw new Error(`Image directory does not exist: ${rootDir}`);
  }

  const results = [];

  walk(rootDir, (filePath) => {
    if (IMAGE_EXTS.has(path.extname(filePath).toLowerCase())) {
      results.push(filePath);
    }
  });

  return results;
}

function walk(dir, visit) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const filePath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(filePath, visit);
    } else if (entry.isFile()) {
      visit(filePath);
    }
  }
}

function assertImageFile(filePath) {
  if (!fs.existsSync(filePath)) throw new Error(`File does not exist: ${filePath}`);
  if (!fs.statSync(filePath).isFile()) throw new Error(`Path is not a file: ${filePath}`);
  if (!IMAGE_EXTS.has(path.extname(filePath).toLowerCase())) {
    throw new Error(`Unsupported image extension: ${filePath}`);
  }
}

function statMtimeMs(filePath) {
  return fs.statSync(filePath).mtimeMs;
}

async function resolveFolders(args, dryRun) {
  if (args.folderId) return [args.folderId];

  const folderName = args.folderName || DEFAULT_FOLDER_NAME;
  if (!folderName) return [];
  if (dryRun) return [`folder-name:${folderName}`];

  const existing = await callTool('folder_get', {
    getAllHierarchy: true,
    fullDetails: true,
  });

  const folders = flattenFolders(existing.data || []);
  const matched = folders.find((folder) => folder.name === folderName);
  if (matched) return [matched.id];

  if (args.noCreateFolder) return [];

  const created = await callTool('folder_create', {
    folders: [
      {
        name: folderName,
        iconColor: 'blue',
        description: 'Codex generated images archived with prompts.',
      },
    ],
  });

  const createdFolders = flattenFolders(created.data || []);
  const createdFolder = createdFolders.find((folder) => folder.name === folderName) || createdFolders[0];
  if (!createdFolder || !createdFolder.id) {
    throw new Error(`Folder was created but no folder ID was returned: ${JSON.stringify(created)}`);
  }

  return [createdFolder.id];
}

function flattenFolders(value) {
  const input = Array.isArray(value) ? value : [value];
  const results = [];

  for (const item of input) {
    if (!item || typeof item !== 'object') continue;
    results.push(item);

    if (Array.isArray(item.children)) {
      results.push(...flattenFolders(item.children));
    }
  }

  return results;
}

function buildName(imagePath, index, total) {
  const base = path.basename(imagePath, path.extname(imagePath));
  const suffix = total > 1 ? `-${String(index + 1).padStart(2, '0')}` : '';
  return `codex-${base}${suffix}`;
}

function buildAnnotation(prompt, imagePath, archivedAt) {
  return [
    'Prompt:',
    prompt || '(no prompt supplied)',
    '',
    'Archive:',
    '- source: Codex',
    `- original_path: ${imagePath}`,
    `- archived_at: ${archivedAt}`,
  ].join('\n');
}

async function callTool(tool, params) {
  const url = new URL(DEFAULT_SERVER);
  const body = JSON.stringify({ tool, params });

  const response = await httpRequest({
    hostname: url.hostname,
    port: url.port || 80,
    path: '/api/tools/call',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body),
    },
    timeout: 30000,
  }, body);

  const parsed = JSON.parse(response.body);
  if (response.statusCode < 200 || response.statusCode >= 300) {
    throw new Error(`Eagle MCP error (${response.statusCode}): ${response.body}`);
  }

  if (parsed && parsed.success === false) {
    throw new Error(`Eagle tool ${tool} failed: ${JSON.stringify(parsed)}`);
  }

  return parsed;
}

function httpRequest(options, body) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    });

    req.on('error', (error) => {
      reject(new Error(`Connection error: ${error.message}. Make sure Eagle is running with the MCP plugin enabled.`));
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timed out.'));
    });

    req.write(body);
    req.end();
  });
}

function unique(values) {
  return [...new Set(values)];
}

function writeJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function expandHome(value) {
  if (!value) return value;
  if (value === '~') return os.homedir();
  if (value.startsWith(`~${path.sep}`)) return path.join(os.homedir(), value.slice(2));
  if (path.sep === '\\' && value.startsWith('~/')) return path.join(os.homedir(), value.slice(2));
  return value;
}

function printHelp() {
  process.stdout.write(`Archive Codex-generated images to Eagle.

Usage:
  archive-codex-image-to-eagle.js --latest --prompt "PROMPT"
  archive-codex-image-to-eagle.js --latest-session --prompt-file /path/prompt.txt
  archive-codex-image-to-eagle.js --path /path/image.png --prompt "PROMPT"

Options:
  --latest                 Import the newest image under the Codex generated_images directory
  --latest-session         Import all images in the newest generated_images session folder
  --path <file>            Import a specific image path
  --image-dir <dir>        Override image directory (default: CODEX_GENERATED_IMAGES_DIR or ~/.codex/generated_images)
  --prompt <text>          Prompt to save in Eagle annotation
  --prompt-file <file>     Read prompt from a text file
  --prompt-stdin           Read prompt from stdin
  --folder-name <name>     Target Eagle folder name (default: Codex 生成图)
  --folder-id <id>         Target Eagle folder ID
  --no-create-folder true  Do not create folder if --folder-name is missing
  --tags <tags>            Extra tags as comma list or JSON array
  --name <name>            Eagle item name
  --dry-run                Print payload without modifying Eagle

Environment:
  CODEX_GENERATED_IMAGES_DIR  Override the default Codex generated image directory
  EAGLE_SERVER_URL            Override Eagle MCP server URL
`);
}
