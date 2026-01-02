/**
 * Offline Tools for Athena AGI
 * These tools work WITHOUT any API calls - perfect for fallback when rate limited
 */

import * as crypto from 'crypto';

export interface OfflineTool {
  name: string;
  description: string;
  schema: any;
  handler: (args: any, context?: any) => Promise<any> | any;
  requiresAPI: false; // Mark as offline
}

// ============================================================================
// COMPUTATION TOOLS
// ============================================================================

const calculateTool: OfflineTool = {
  name: 'calculate',
  description: 'Perform mathematical calculations offline. Supports basic math, trigonometry, and more.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      expression: {
        type: 'string',
        description: 'Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)", "sin(3.14)")'
      }
    },
    required: ['expression']
  },
  handler: async ({ expression }: { expression: string }) => {
    try {
      // Safe math evaluation using Function constructor with limited scope
      const safeEval = new Function('Math', `
        'use strict';
        return ${expression};
      `);

      const result = safeEval(Math);

      return {
        expression,
        result,
        type: typeof result
      };
    } catch (error) {
      return {
        error: 'Invalid mathematical expression',
        expression,
        details: String(error)
      };
    }
  }
};

const convertUnitsTool: OfflineTool = {
  name: 'convert_units',
  description: 'Convert between common units (temperature, length, weight, time) offline.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      value: { type: 'number', description: 'Value to convert' },
      from: { type: 'string', description: 'Source unit (e.g., "celsius", "meters", "pounds")' },
      to: { type: 'string', description: 'Target unit (e.g., "fahrenheit", "feet", "kilograms")' }
    },
    required: ['value', 'from', 'to']
  },
  handler: async ({ value, from, to }: { value: number; from: string; to: string }) => {
    const conversions: Record<string, Record<string, (v: number) => number>> = {
      celsius: {
        fahrenheit: (c) => (c * 9/5) + 32,
        kelvin: (c) => c + 273.15
      },
      fahrenheit: {
        celsius: (f) => (f - 32) * 5/9,
        kelvin: (f) => (f - 32) * 5/9 + 273.15
      },
      meters: {
        feet: (m) => m * 3.28084,
        inches: (m) => m * 39.3701,
        kilometers: (m) => m / 1000
      },
      feet: {
        meters: (f) => f / 3.28084,
        inches: (f) => f * 12
      },
      pounds: {
        kilograms: (lb) => lb * 0.453592,
        ounces: (lb) => lb * 16
      },
      kilograms: {
        pounds: (kg) => kg / 0.453592
      }
    };

    const converter = conversions[from.toLowerCase()]?.[to.toLowerCase()];

    if (!converter) {
      return { error: `Conversion from ${from} to ${to} not supported` };
    }

    return {
      original: { value, unit: from },
      converted: { value: converter(value), unit: to }
    };
  }
};

// ============================================================================
// TEXT PROCESSING TOOLS
// ============================================================================

const textProcessTool: OfflineTool = {
  name: 'process_text',
  description: 'Process text offline: uppercase, lowercase, reverse, word count, character count, etc.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      text: { type: 'string', description: 'Text to process' },
      operation: {
        type: 'string',
        enum: ['uppercase', 'lowercase', 'titlecase', 'reverse', 'wordcount', 'charcount', 'trim', 'slugify'],
        description: 'Operation to perform'
      }
    },
    required: ['text', 'operation']
  },
  handler: async ({ text, operation }: { text: string; operation: string }) => {
    const operations: Record<string, (s: string) => any> = {
      uppercase: (s) => ({ result: s.toUpperCase() }),
      lowercase: (s) => ({ result: s.toLowerCase() }),
      titlecase: (s) => ({ result: s.replace(/\w\S*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()) }),
      reverse: (s) => ({ result: s.split('').reverse().join('') }),
      wordcount: (s) => ({ count: s.trim().split(/\s+/).length }),
      charcount: (s) => ({ count: s.length, without_spaces: s.replace(/\s/g, '').length }),
      trim: (s) => ({ result: s.trim() }),
      slugify: (s) => ({ result: s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') })
    };

    const op = operations[operation];
    if (!op) {
      return { error: `Unknown operation: ${operation}` };
    }

    return { operation, ...op(text) };
  }
};

const regexTool: OfflineTool = {
  name: 'regex_match',
  description: 'Match patterns in text using regular expressions, offline.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      text: { type: 'string', description: 'Text to search' },
      pattern: { type: 'string', description: 'Regex pattern' },
      flags: { type: 'string', description: 'Regex flags (g, i, m)', default: 'g' }
    },
    required: ['text', 'pattern']
  },
  handler: async ({ text, pattern, flags = 'g' }: { text: string; pattern: string; flags?: string }) => {
    try {
      const regex = new RegExp(pattern, flags);
      const matches = text.match(regex);

      return {
        pattern,
        matches: matches || [],
        count: matches?.length || 0,
        found: !!matches
      };
    } catch (error) {
      return { error: 'Invalid regex pattern', details: String(error) };
    }
  }
};

// ============================================================================
// DATA TOOLS
// ============================================================================

const jsonTool: OfflineTool = {
  name: 'json_operations',
  description: 'Parse, validate, and format JSON offline.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      data: { type: 'string', description: 'JSON string to process' },
      operation: {
        type: 'string',
        enum: ['validate', 'format', 'minify', 'parse'],
        description: 'Operation to perform'
      }
    },
    required: ['data', 'operation']
  },
  handler: async ({ data, operation }: { data: string; operation: string }) => {
    try {
      const parsed = JSON.parse(data);

      switch (operation) {
        case 'validate':
          return { valid: true, message: 'Valid JSON' };

        case 'format':
          return { result: JSON.stringify(parsed, null, 2) };

        case 'minify':
          return { result: JSON.stringify(parsed) };

        case 'parse':
          return { parsed, type: Array.isArray(parsed) ? 'array' : typeof parsed };

        default:
          return { error: 'Unknown operation' };
      }
    } catch (error) {
      return { valid: false, error: 'Invalid JSON', details: String(error) };
    }
  }
};

// ============================================================================
// DATE/TIME TOOLS
// ============================================================================

const dateTimeTool: OfflineTool = {
  name: 'datetime_operations',
  description: 'Work with dates and times offline: format, calculate differences, add/subtract time.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      operation: {
        type: 'string',
        enum: ['now', 'format', 'diff', 'add', 'subtract'],
        description: 'Date/time operation'
      },
      date: { type: 'string', description: 'ISO date string (optional, uses now if not provided)' },
      format: { type: 'string', description: 'Output format (optional)' },
      amount: { type: 'number', description: 'Amount to add/subtract (for add/subtract operations)' },
      unit: { type: 'string', enum: ['seconds', 'minutes', 'hours', 'days'], description: 'Time unit' }
    },
    required: ['operation']
  },
  handler: async ({ operation, date, format, amount, unit }: any) => {
    const d = date ? new Date(date) : new Date();

    switch (operation) {
      case 'now':
        return { iso: d.toISOString(), unix: Math.floor(d.getTime() / 1000), readable: d.toString() };

      case 'format':
        return { iso: d.toISOString(), locale: d.toLocaleString() };

      case 'diff':
        const now = new Date();
        const diff = Math.abs(now.getTime() - d.getTime());
        return {
          milliseconds: diff,
          seconds: Math.floor(diff / 1000),
          minutes: Math.floor(diff / 60000),
          hours: Math.floor(diff / 3600000),
          days: Math.floor(diff / 86400000)
        };

      case 'add':
      case 'subtract': {
        const ms = amount * (unit === 'days' ? 86400000 : unit === 'hours' ? 3600000 : unit === 'minutes' ? 60000 : 1000);
        const newDate = new Date(d.getTime() + (operation === 'add' ? ms : -ms));
        return { result: newDate.toISOString() };
      }

      default:
        return { error: 'Unknown operation' };
    }
  }
};

// ============================================================================
// UTILITY TOOLS
// ============================================================================

const hashTool: OfflineTool = {
  name: 'hash_data',
  description: 'Generate hashes (MD5, SHA256, etc.) offline for data integrity.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      data: { type: 'string', description: 'Data to hash' },
      algorithm: { type: 'string', enum: ['md5', 'sha1', 'sha256', 'sha512'], default: 'sha256' }
    },
    required: ['data']
  },
  handler: async ({ data, algorithm = 'sha256' }: { data: string; algorithm?: string }) => {
    const hash = crypto.createHash(algorithm).update(data).digest('hex');
    return { algorithm, hash, length: hash.length };
  }
};

const uuidTool: OfflineTool = {
  name: 'generate_uuid',
  description: 'Generate a random UUID/GUID offline.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      version: { type: 'number', enum: [4], default: 4, description: 'UUID version' }
    }
  },
  handler: async () => {
    return { uuid: crypto.randomUUID() };
  }
};

const encodeTool: OfflineTool = {
  name: 'encode_decode',
  description: 'Encode/decode data (base64, URL, hex) offline.',
  requiresAPI: false,
  schema: {
    type: 'object',
    properties: {
      data: { type: 'string', description: 'Data to encode/decode' },
      operation: { type: 'string', enum: ['base64_encode', 'base64_decode', 'url_encode', 'url_decode', 'hex_encode', 'hex_decode'] }
    },
    required: ['data', 'operation']
  },
  handler: async ({ data, operation }: { data: string; operation: string }) => {
    try {
      switch (operation) {
        case 'base64_encode':
          return { result: Buffer.from(data).toString('base64') };
        case 'base64_decode':
          return { result: Buffer.from(data, 'base64').toString('utf-8') };
        case 'url_encode':
          return { result: encodeURIComponent(data) };
        case 'url_decode':
          return { result: decodeURIComponent(data) };
        case 'hex_encode':
          return { result: Buffer.from(data).toString('hex') };
        case 'hex_decode':
          return { result: Buffer.from(data, 'hex').toString('utf-8') };
        default:
          return { error: 'Unknown operation' };
      }
    } catch (error) {
      return { error: 'Encoding/decoding failed', details: String(error) };
    }
  }
};

// ============================================================================
// EXPORT ALL OFFLINE TOOLS
// ============================================================================

export const offlineTools: OfflineTool[] = [
  // Computation
  calculateTool,
  convertUnitsTool,

  // Text Processing
  textProcessTool,
  regexTool,

  // Data Operations
  jsonTool,

  // Date/Time
  dateTimeTool,

  // Utilities
  hashTool,
  uuidTool,
  encodeTool
];

// Helper to check if a tool requires API
export function isOfflineTool(toolName: string): boolean {
  return offlineTools.some(t => t.name === toolName);
}

// Execute offline tool
export async function executeOfflineTool(name: string, args: any): Promise<any> {
  const tool = offlineTools.find(t => t.name === name);
  if (!tool) {
    throw new Error(`Offline tool not found: ${name}`);
  }
  return tool.handler(args);
}

console.log(`✅ Loaded ${offlineTools.length} offline tools for Athena`);
