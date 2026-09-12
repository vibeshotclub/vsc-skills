#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const http = require('http');
const os = require('os');
const { spawn } = require('child_process');

const DEFAULT_IMAGE_DIR = process.env.CODEX_GENERATED_IMAGES_DIR || path.join(os.homedir(), '.codex', 'generated_images');
const DEFAULT_SERVER = process.env.EAGLE_SERVER_URL || 'http://127.0.0.1:41596';
const DEFAULT_MCP_SERVER_NAME = process.env.EAGLE_MCP_SERVER_NAME || 'eagle';
const IMAGE_EXTS = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif']);
const DEFAULT_FOLDER_NAME = 'Codex 生成图';
const DEFAULT_TAGS = ['Codex', 'AI生成', 'Prompt'];
const FOLDER_LOCK_TIMEOUT_MS = Number(process.env.EAGLE_FOLDER_LOCK_TIMEOUT_MS || 15000);
const FOLDER_LOCK_POLL_MS = Number(process.env.EAGLE_FOLDER_LOCK_POLL_MS || 150);
let cliArgs = {};
let stdioClientPromise = null;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  cliArgs = args;

  if (args.help) {
    printHelp();
    return;
  }

  if (args.checkConnection) {
    const result = await callTool('get_app_info', {});
    writeJson({
      success: true,
      transport: transportName(),
      result,
    });
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

  const folderIdsByImagePath = await resolveFoldersForImages(args, imagePaths, dryRun);
  const archivedAt = new Date().toISOString();
  const items = imagePaths.map((imagePath, index) => ({
    source: {
      type: 'path',
      path: imagePath,
    },
    name: args.name || buildName(imagePath, index, imagePaths.length),
    annotation: buildAnnotation(prompt, imagePath, archivedAt),
    folders: folderIdsByImagePath.get(imagePath) || [],
  }));

  const payload = {
    tags,
    items,
  };

  if (dryRun) {
    writeJson({
      dryRun: true,
      transport: transportName(),
      server: DEFAULT_SERVER,
      imageDir,
      dateSubfolders: shouldUseDateSubfolders(args),
      foldersByImagePath: Object.fromEntries(folderIdsByImagePath),
      payload,
    });
    return;
  }

  const result = await callTool('item_add', payload);
  writeJson({
    success: true,
    imagePaths,
    foldersByImagePath: Object.fromEntries(folderIdsByImagePath),
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
    else if (arg === '--check-connection') args.checkConnection = true;
    else if (arg === '--prompt-stdin') args.promptStdin = true;
    else if (arg === '--no-date-subfolders' || arg === '--flat-folder') args.noDateSubfolders = true;
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

async function resolveFoldersForImages(args, imagePaths, dryRun) {
  const fixedFolderId = args.folderId || process.env.EAGLE_CODEX_FOLDER_ID;
  if (fixedFolderId) {
    return new Map(imagePaths.map((imagePath) => [imagePath, [fixedFolderId]]));
  }

  const rootFolderId = args.rootFolderId || process.env.EAGLE_CODEX_ROOT_FOLDER_ID;
  const rootFolderName = args.folderName || DEFAULT_FOLDER_NAME;
  if (!rootFolderId && !rootFolderName) return new Map(imagePaths.map((imagePath) => [imagePath, []]));

  if (!shouldUseDateSubfolders(args)) {
    if (rootFolderId) {
      return new Map(imagePaths.map((imagePath) => [imagePath, [rootFolderId]]));
    }

    const folderIds = await resolveFolderPath([rootFolderName], args, dryRun);
    return new Map(imagePaths.map((imagePath) => [imagePath, folderIds]));
  }

  const uniqueDateNames = unique(imagePaths.map(dateFolderName));
  const idsByDateName = new Map();
  for (const dateName of uniqueDateNames) {
    const folderIds = rootFolderId
      ? await resolveFolderPath([dateName], args, dryRun, { parentId: rootFolderId })
      : await resolveFolderPath([rootFolderName, dateName], args, dryRun);
    idsByDateName.set(dateName, folderIds);
  }

  return new Map(imagePaths.map((imagePath) => [imagePath, idsByDateName.get(dateFolderName(imagePath)) || []]));
}

function shouldUseDateSubfolders(args) {
  return !args.noDateSubfolders && !args.folderId && !process.env.EAGLE_CODEX_FOLDER_ID;
}

async function resolveFolderPath(names, args, dryRun, options = {}) {
  if (dryRun) return [`folder-path:${names.join('/')}`];

  const lockKey = ['eagle-folder', options.parentId || 'root', ...names].join('/');
  return withFolderLock(lockKey, async () => {
    const existing = await callTool('folder_get', {
      getAllHierarchy: true,
      fullDetails: true,
    });

    const folders = flattenFolders(existing.data || []);
    let parentId = options.parentId || null;
    let current = null;

    for (const name of names) {
      current = findFolderByNameAndParent(folders, name, parentId);
      if (!current) {
        if (args.noCreateFolder) return [];

        await callTool('folder_create', {
          parentId: parentId || undefined,
          folders: [
            {
              name,
              parentId: parentId || undefined,
              iconColor: parentId ? 'aqua' : 'blue',
              description: parentId ? 'Codex generated images grouped by local generation date.' : 'Codex generated images archived with prompts.',
            },
          ],
        });

        const refreshed = await callTool('folder_get', {
          getAllHierarchy: true,
          fullDetails: true,
        });
        const refreshedFolders = flattenFolders(refreshed.data || []);
        current = findFolderByNameAndParent(refreshedFolders, name, parentId);
        if (!current || !current.id) {
          throw new Error(`Folder was created but could not be resolved under parent ${parentId || 'root'}: ${name}`);
        }

        folders.length = 0;
        folders.push(...refreshedFolders);
      }

      parentId = current.id;
    }

    return current ? [current.id] : [];
  });
}

function findFolderByNameAndParent(folders, name, parentId) {
  const matches = folders
    .filter((folder) => folder.name === name && normalizeParent(getFolderParentId(folder)) === normalizeParent(parentId))
    .sort((a, b) => Number(a.createdAt || 0) - Number(b.createdAt || 0));
  return matches[0] || null;
}

async function withFolderLock(key, fn) {
  const lockDir = path.join(os.tmpdir(), `codex-image-to-eagle-${hashKey(key)}.lock`);
  const start = Date.now();

  while (true) {
    try {
      fs.mkdirSync(lockDir);
      break;
    } catch (error) {
      if (error && error.code !== 'EEXIST') throw error;
      if (Date.now() - start > FOLDER_LOCK_TIMEOUT_MS) {
        throw new Error(`Timed out waiting for Eagle folder lock: ${key}`);
      }
      await sleep(FOLDER_LOCK_POLL_MS);
    }
  }

  try {
    return await fn();
  } finally {
    fs.rmSync(lockDir, { recursive: true, force: true });
  }
}

function hashKey(value) {
  let hash = 5381;
  for (let i = 0; i < value.length; i += 1) {
    hash = ((hash << 5) + hash) ^ value.charCodeAt(i);
  }
  return (hash >>> 0).toString(36);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getFolderParentId(folder) {
  if (!folder || typeof folder !== 'object') return null;
  return folder.parent ?? folder.parentId ?? folder._parentId ?? null;
}

function normalizeParent(value) {
  return value || null;
}

function dateFolderName(imagePath) {
  const date = fs.statSync(imagePath).mtime;
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

function flattenFolders(value, parentId = null) {
  const input = Array.isArray(value) ? value : [value];
  const results = [];

  for (const item of input) {
    if (!item || typeof item !== 'object') continue;
    const current = {
      ...item,
      _parentId: item.parent ?? item.parentId ?? parentId ?? null,
    };
    results.push(current);

    if (Array.isArray(item.children)) {
      results.push(...flattenFolders(item.children, item.id || null));
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
  if (transportName() === 'stdio') {
    const client = await getStdioClient();
    return client.callTool(tool, params);
  }

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

function transportName() {
  const explicit = cliArgs.transport || process.env.EAGLE_MCP_TRANSPORT;
  if (explicit) return explicit.toLowerCase();

  const serverName = cliArgs.mcpServer || process.env.EAGLE_MCP_SERVER_NAME || DEFAULT_MCP_SERVER_NAME;
  const configPath = expandHome(cliArgs.codexConfig || process.env.CODEX_CONFIG_FILE || path.join(os.homedir(), '.codex', 'config.toml'));
  return resolveCodexMcpServerConfig(configPath, serverName) ? 'stdio' : 'http';
}

async function getStdioClient() {
  if (!stdioClientPromise) {
    stdioClientPromise = StdioMcpClient.create(resolveStdioConfig(cliArgs));
  }
  return stdioClientPromise;
}

function resolveStdioConfig(args) {
  const command = args.stdioCommand || process.env.EAGLE_MCP_COMMAND;
  const argText = args.stdioArgs || process.env.EAGLE_MCP_ARGS;
  if (command) {
    return {
      command,
      args: parseArgList(argText),
      env: parseEnvObject(process.env.EAGLE_MCP_ENV || ''),
    };
  }

  const serverName = args.mcpServer || process.env.EAGLE_MCP_SERVER_NAME || DEFAULT_MCP_SERVER_NAME;
  const configPath = expandHome(args.codexConfig || process.env.CODEX_CONFIG_FILE || path.join(os.homedir(), '.codex', 'config.toml'));
  const config = resolveCodexMcpServerConfig(configPath, serverName);
  if (config) return config;

  throw new Error(`No Eagle stdio MCP config found in ${configPath}. Use --stdio-command or configure a [mcp_servers.${serverName}] entry.`);
}

function resolveCodexMcpServerConfig(configPath, preferredName) {
  const preferred = readCodexMcpServerConfig(configPath, preferredName);
  if (preferred) return preferred;
  if (preferredName !== 'eagle') {
    const eagle = readCodexMcpServerConfig(configPath, 'eagle');
    if (eagle) return eagle;
  }
  return findEagleMcpServerConfig(configPath);
}

function readCodexMcpServerConfig(configPath, serverName) {
  if (!fs.existsSync(configPath)) return null;

  const text = fs.readFileSync(configPath, 'utf8');
  const escaped = serverName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const sectionRe = new RegExp(`^\\s*\\[mcp_servers\\.(?:"${escaped}"|${escaped})\\]\\s*$`);
  const lines = text.split(/\r?\n/);
  const start = lines.findIndex((line) => sectionRe.test(line));
  if (start === -1) return null;

  const section = [];
  for (let i = start + 1; i < lines.length; i += 1) {
    if (/^\s*\[/.test(lines[i])) break;
    section.push(lines[i]);
  }

  const command = parseTomlStringValue(section, 'command');
  if (!command) return null;

  return {
    command,
    args: parseTomlStringArrayValue(section, 'args'),
    env: parseTomlInlineObjectValue(section, 'env'),
  };
}

function findEagleMcpServerConfig(configPath) {
  if (!fs.existsSync(configPath)) return null;

  const text = fs.readFileSync(configPath, 'utf8');
  const lines = text.split(/\r?\n/);

  for (let i = 0; i < lines.length; i += 1) {
    const match = lines[i].match(/^\s*\[mcp_servers\.(?:"([^"]+)"|([A-Za-z0-9_-]+))\]\s*$/);
    if (!match) continue;

    const section = [];
    for (let j = i + 1; j < lines.length; j += 1) {
      if (/^\s*\[/.test(lines[j])) break;
      section.push(lines[j]);
    }

    const config = {
      command: parseTomlStringValue(section, 'command'),
      args: parseTomlStringArrayValue(section, 'args'),
      env: parseTomlInlineObjectValue(section, 'env'),
    };
    if (!config.command) continue;
    if (looksLikeEagleMcpConfig(config, match[1] || match[2])) return config;
  }

  return null;
}

function looksLikeEagleMcpConfig(config, name) {
  const haystack = [
    name,
    config.command,
    ...(config.args || []),
    ...Object.values(config.env || {}),
  ].join(' ').toLowerCase();

  return haystack.includes('eagle') || haystack.includes('mcp-proxy.js') || haystack.includes('mcp-server');
}

function parseTomlStringValue(lines, key) {
  const re = new RegExp(`^\\s*${key}\\s*=\\s*"((?:[^"\\\\]|\\\\.)*)"\\s*$`);
  for (const line of lines) {
    const match = line.match(re);
    if (match) return unescapeTomlString(match[1]);
  }
  return null;
}

function parseTomlStringArrayValue(lines, key) {
  const re = new RegExp(`^\\s*${key}\\s*=\\s*\\[(.*)\\]\\s*$`);
  for (const line of lines) {
    const match = line.match(re);
    if (!match) continue;
    return [...match[1].matchAll(/"((?:[^"\\]|\\.)*)"/g)].map((item) => unescapeTomlString(item[1]));
  }
  return [];
}

function parseTomlInlineObjectValue(lines, key) {
  const re = new RegExp(`^\\s*${key}\\s*=\\s*\\{(.*)\\}\\s*$`);
  for (const line of lines) {
    const match = line.match(re);
    if (!match) continue;
    const env = {};
    for (const item of match[1].matchAll(/([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"((?:[^"\\]|\\.)*)"/g)) {
      env[item[1]] = unescapeTomlString(item[2]);
    }
    return env;
  }
  return {};
}

function unescapeTomlString(value) {
  return value
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, '\\')
    .replace(/\\n/g, '\n')
    .replace(/\\t/g, '\t');
}

function parseArgList(value) {
  if (!value) return [];
  const raw = value.trim();
  if (!raw) return [];
  if (raw.startsWith('[')) {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) throw new Error('EAGLE_MCP_ARGS JSON must be an array');
    return parsed.map(String);
  }
  return raw.split(',').map((item) => item.trim()).filter(Boolean);
}

function parseEnvObject(value) {
  if (!value.trim()) return {};
  if (value.trim().startsWith('{')) return JSON.parse(value);
  const env = {};
  for (const item of value.split(',')) {
    const [key, ...rest] = item.split('=');
    if (key && rest.length > 0) env[key.trim()] = rest.join('=').trim();
  }
  return env;
}

class StdioMcpClient {
  static async create(config) {
    const client = new StdioMcpClient(config);
    await client.start();
    return client;
  }

  constructor(config) {
    this.config = config;
    this.nextId = 1;
    this.pending = new Map();
    this.stderrTail = '';
  }

  async start() {
    this.child = spawn(this.config.command, this.config.args || [], {
      env: { ...process.env, ...(this.config.env || {}) },
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    this.child.stdout.setEncoding('utf8');
    this.child.stderr.setEncoding('utf8');
    this.child.stdout.on('data', (data) => this.handleStdout(data));
    this.child.stderr.on('data', (data) => {
      this.stderrTail = (this.stderrTail + data).slice(-4000);
    });
    this.child.on('exit', (code, signal) => {
      const error = new Error(`stdio MCP server exited (${signal || code}). ${this.stderrTail}`.trim());
      for (const { reject } of this.pending.values()) reject(error);
      this.pending.clear();
    });

    await this.request('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'codex-image-to-eagle', version: '1.0.0' },
    });
    this.notify('notifications/initialized', {});
  }

  handleStdout(data) {
    this.buffer = (this.buffer || '') + data;
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';

    for (const line of lines) {
      if (!line.trim()) continue;
      let message;
      try {
        message = JSON.parse(line);
      } catch (error) {
        continue;
      }

      if (message.id !== undefined && this.pending.has(message.id)) {
        const { resolve, reject, timeout } = this.pending.get(message.id);
        clearTimeout(timeout);
        this.pending.delete(message.id);
        if (message.error) reject(new Error(JSON.stringify(message.error)));
        else resolve(message.result);
      }
    }
  }

  request(method, params) {
    const id = this.nextId;
    this.nextId += 1;

    const message = { jsonrpc: '2.0', id, method, params };
    this.child.stdin.write(`${JSON.stringify(message)}\n`);

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`stdio MCP request timed out: ${method}. ${this.stderrTail}`.trim()));
      }, 120000);
      this.pending.set(id, { resolve, reject, timeout });
    });
  }

  notify(method, params) {
    this.child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', method, params })}\n`);
  }

  async callTool(name, args) {
    const result = await this.request('tools/call', {
      name,
      arguments: args || {},
    });
    return normalizeMcpToolResult(name, result);
  }

  close() {
    if (this.child && !this.child.killed) {
      this.child.stdin.end();
    }
  }
}

function normalizeMcpToolResult(tool, result) {
  if (!result || !Array.isArray(result.content)) return result;

  const text = result.content
    .filter((item) => item && item.type === 'text' && typeof item.text === 'string')
    .map((item) => item.text)
    .join('\n')
    .trim();

  if (!text) return result;

  try {
    const parsed = JSON.parse(text);
    if (parsed && parsed.success === false) {
      throw new Error(`Eagle tool ${tool} failed: ${JSON.stringify(parsed)}`);
    }
    return parsed;
  } catch (error) {
    if (error.message.startsWith('Eagle tool ')) throw error;
    return { success: true, data: text };
  }
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
  --folder-id <id>         Exact target Eagle folder ID; skips folder lookup and disables date subfolders
  --root-folder-id <id>    Existing Eagle root folder ID; keeps date subfolders under this root
  --no-create-folder true  Do not create folder if --folder-name is missing
  --no-date-subfolders     Import into the root folder instead of Codex 生成图/YYYY-M-D
  --flat-folder            Alias for --no-date-subfolders
  --tags <tags>            Extra tags as comma list or JSON array
  --name <name>            Eagle item name
  --dry-run                Print payload without modifying Eagle
  --check-connection       Test Eagle MCP connectivity without importing images
  --transport <http|stdio> Transport to use (default: auto; stdio if Eagle MCP config is found)
  --mcp-server <name>      Preferred Codex MCP server name for stdio config (default: eagle)
  --codex-config <file>    Codex config file for stdio lookup (default: ~/.codex/config.toml)
  --stdio-command <cmd>    Override stdio MCP command instead of reading config
  --stdio-args <args>      Stdio MCP args as JSON array or comma list

Environment:
  CODEX_GENERATED_IMAGES_DIR  Override the default Codex generated image directory
  EAGLE_CODEX_FOLDER_ID       Exact Eagle folder ID; skips folder_get and folder_create
  EAGLE_CODEX_ROOT_FOLDER_ID  Existing Eagle root folder ID; creates/reuses date subfolders below it
  EAGLE_SERVER_URL            Override Eagle MCP server URL
  EAGLE_MCP_TRANSPORT         Set to stdio to use a stdio MCP server
  EAGLE_MCP_SERVER_NAME       Codex MCP server name for stdio config
  EAGLE_MCP_COMMAND           Override stdio MCP command
  EAGLE_MCP_ARGS              Override stdio MCP args as JSON array or comma list
`);
}

main()
  .finally(async () => {
    if (stdioClientPromise) {
      try {
        const client = await stdioClientPromise;
        client.close();
      } catch (error) {
        // Ignore cleanup errors after the main command has already finished.
      }
    }
  })
  .catch((error) => {
    console.error(error.message || error);
    process.exit(1);
  });
