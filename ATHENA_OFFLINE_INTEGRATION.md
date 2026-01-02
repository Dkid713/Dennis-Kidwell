# Athena Offline Tools - Integration Guide

## Problem Solved ✅

**Before:** OpenAI rate limit (429) → Athena completely dead ❌
**After:** Rate limit detected → Automatically switch to offline tools → Athena still works ✅

---

## What You Got

### 1. **9 Offline Tools** (`athena-offline-tools.ts`)

These work WITHOUT any API calls:

| Tool | What It Does | Example |
|------|-------------|---------|
| `calculate` | Math operations | `2 + 2`, `sqrt(16)`, `sin(3.14)` |
| `convert_units` | Unit conversions | Celsius to Fahrenheit, meters to feet |
| `process_text` | Text manipulation | Uppercase, word count, slugify |
| `regex_match` | Pattern matching | Find emails, phone numbers, etc |
| `json_operations` | JSON parse/validate | Validate, format, minify JSON |
| `datetime_operations` | Date/time | Current time, date math, formatting |
| `hash_data` | Generate hashes | MD5, SHA256, SHA512 |
| `generate_uuid` | Create UUIDs | Random unique IDs |
| `encode_decode` | Encoding | Base64, URL encoding, hex |

### 2. **Enhanced ReAct Loop** (`reactLoop-with-offline.ts`)

- Automatically detects 429 rate limit errors
- Switches to offline mode
- Tracks rate limit reset time
- Falls back gracefully
- Returns to normal mode when rate limit expires

---

## How to Integrate

### Option 1: Replace Your Current ReAct Loop

```typescript
// Replace your current reactLoop import
// FROM:
import { reactLoop } from './original-react-loop';

// TO:
import { reactLoop } from './reactLoop-with-offline';
```

That's it! The API is the same, but now it handles rate limits.

### Option 2: Add to Existing Tools

```typescript
// In your core tools file
import { offlineTools } from './athena-offline-tools';
import { coreTools } from './core';

// Combine them
export const allTools = [...coreTools, ...offlineTools];
```

---

## Testing It

### Test Offline Tools

```typescript
import { executeOfflineTool } from './athena-offline-tools';

// Test calculator
const result = await executeOfflineTool('calculate', {
  expression: '2 + 2 * 10'
});
console.log(result); // { expression: '2 + 2 * 10', result: 22 }

// Test text processing
const text = await executeOfflineTool('process_text', {
  text: 'hello world',
  operation: 'uppercase'
});
console.log(text); // { operation: 'uppercase', result: 'HELLO WORLD' }

// Test date/time
const now = await executeOfflineTool('datetime_operations', {
  operation: 'now'
});
console.log(now); // { iso: '2025-01-...', unix: 1704..., readable: '...' }
```

### Manually Trigger Offline Mode (for testing)

```typescript
import { setOfflineMode, getOperatingMode } from './reactLoop-with-offline';

// Force offline mode
setOfflineMode(true);

// Check current mode
const mode = getOperatingMode();
console.log(mode); // { offline: true, resetTime: null }

// Disable offline mode
setOfflineMode(false);
```

---

## What Happens During Rate Limit

### Before (Your Old Code)
```
User: "Calculate 2+2"
  ↓
API Call → 429 Rate Limit
  ↓
❌ Error: Rate limit exceeded
  ↓
Athena is dead until reset
```

### After (New Code)
```
User: "Calculate 2+2"
  ↓
API Call → 429 Rate Limit Detected!
  ↓
✅ Switch to offline mode
  ↓
Use calculate tool (offline)
  ↓
Return result: 4
  ↓
Athena still works!
```

---

## Example Usage

```typescript
import { reactLoop } from './reactLoop-with-offline';

const messages = [
  { role: 'user', content: 'Calculate the square root of 144' }
];

const result = await reactLoop(
  provider,
  messages,
  'You are Athena, a helpful AI assistant.',
  10
);

console.log(result);
// {
//   response: "The square root of 144 is 12.",
//   toolsUsed: ['calculate'],
//   loops: 1,
//   offlineMode: false,  // ← Tells you if offline mode was used
//   rateLimited: false   // ← Tells you if rate limited
// }
```

---

## Rate Limit Detection

The system detects rate limits in two ways:

1. **HTTP Status 429** from OpenAI
2. **Error message** containing "rate limit"

When detected:
- Switches to offline mode
- Extracts `Retry-After` header (if available)
- Automatically returns to normal mode when reset time expires
- Logs everything for debugging

---

## User Experience During Rate Limit

### Scenario 1: User Asks Math Question

**User:** "What's 15% of 250?"

**Athena (rate limited):** "Let me calculate that for you. 15% of 250 is 37.5"
- ✅ Works offline using `calculate` tool
- User doesn't even know you're rate limited!

### Scenario 2: User Asks Complex Question

**User:** "Search the web for the latest AI news"

**Athena (rate limited):** "I'm currently rate limited and cannot search the web. However, I can help you with:
- Mathematical calculations
- Text processing and formatting
- JSON validation
- Date/time operations
- Data encoding and hashing

What would you like me to help with?"

---

## Monitoring

```typescript
import { getOperatingMode } from './reactLoop-with-offline';

// Check status periodically
setInterval(() => {
  const mode = getOperatingMode();

  if (mode.offline) {
    console.log('⚠️ Operating in offline mode');

    if (mode.resetTime) {
      const secondsLeft = Math.floor((mode.resetTime - Date.now()) / 1000);
      console.log(`⏰ Resets in ${secondsLeft} seconds`);
    }
  } else {
    console.log('✅ Normal operation');
  }
}, 10000); // Check every 10 seconds
```

---

## Adding More Offline Tools

Want to add your own offline tool?

```typescript
// In athena-offline-tools.ts

const myCustomTool: OfflineTool = {
  name: 'my_tool',
  description: 'What my tool does',
  requiresAPI: false, // ← Important!
  schema: {
    type: 'object',
    properties: {
      input: { type: 'string', description: 'Input parameter' }
    },
    required: ['input']
  },
  handler: async ({ input }) => {
    // Your offline logic here
    return { result: `Processed: ${input}` };
  }
};

// Add to exports
export const offlineTools: OfflineTool[] = [
  // ... existing tools ...
  myCustomTool
];
```

---

## Benefits

✅ **Never completely offline** - Always have some functionality
✅ **Automatic fallback** - No code changes needed
✅ **Cost savings** - Offline tools are free!
✅ **Better UX** - Users still get help during outages
✅ **Debugging** - Test without burning API credits
✅ **Resilient** - Works during API issues, not just rate limits

---

## Integration Checklist

- [ ] Copy `athena-offline-tools.ts` to your project
- [ ] Copy `reactLoop-with-offline.ts` to your project
- [ ] Update imports to use new reactLoop
- [ ] Test offline tools manually
- [ ] Test rate limit scenario
- [ ] Update UI to show offline mode (optional)
- [ ] Add monitoring/logging (optional)

---

## Questions?

**Q: Will this slow down normal operations?**
A: No! Offline tools are actually FASTER (no API calls). The rate limit check is instant.

**Q: Can I disable offline mode?**
A: Yes, just don't import the offline tools, or filter them out.

**Q: What if offline tools can't handle the request?**
A: The agent will inform the user and suggest what offline tools CAN do.

**Q: Does this work with Claude/GPT-4/other models?**
A: Yes! It's provider-agnostic. Works with any LLM.

---

## Summary

You now have **9 offline tools** that keep Athena functional even when rate limited. The system:

1. Automatically detects rate limits
2. Switches to offline mode
3. Uses local computation instead of API calls
4. Returns to normal when rate limit expires
5. Provides graceful degradation

**No more dead Athena during rate limits!** 🎉
