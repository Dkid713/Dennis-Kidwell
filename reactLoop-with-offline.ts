/**
 * Enhanced ReAct Tool Execution Loop with Offline Fallback
 * Enables Athena to work even when rate limited!
 */

import { coreTools } from './core';
import { offlineTools, executeOfflineTool, isOfflineTool } from './athena-offline-tools';
import { LLMMessage } from '../../../shared/athena-schema';

// Combine online and offline tools
const allTools = [...coreTools, ...offlineTools];
const toolMap = new Map(allTools.map(t => [t.name, t]));

// Track rate limit state
let isRateLimited = false;
let rateLimitResetTime: number | null = null;

// Convert tools to OpenAI function format
export function getOpenAITools() {
  return allTools.map(tool => ({
    type: 'function' as const,
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.schema
    }
  }));
}

// Get only offline tools (for fallback mode)
export function getOfflineToolsOnly() {
  return offlineTools.map(tool => ({
    type: 'function' as const,
    function: {
      name: tool.name,
      description: `[OFFLINE] ${tool.description}`,
      parameters: tool.schema
    }
  }));
}

// Execute a single tool call with offline fallback
export async function executeTool(
  name: string,
  args: any
): Promise<{ success: boolean; result: any; error?: string; offline?: boolean }> {

  const tool = toolMap.get(name);
  if (!tool) {
    return { success: false, result: null, error: `Unknown tool: ${name}` };
  }

  // Check if tool is offline-capable
  const isOffline = isOfflineTool(name);

  try {
    console.log(`🔧 Executing tool: ${name}${isOffline ? ' [OFFLINE]' : ''}`, args);
    const result = await tool.handler(args, {});
    console.log(`✅ Tool ${name} completed`);
    return { success: true, result, offline: isOffline };
  } catch (error: any) {
    console.error(`❌ Tool ${name} failed:`, error);

    // Check if it's a rate limit error
    if (error.status === 429 || error.message?.includes('rate limit')) {
      console.warn('🚨 Rate limit detected! Switching to offline mode...');
      isRateLimited = true;

      // Extract retry-after if available
      if (error.headers?.['retry-after']) {
        const retryAfter = parseInt(error.headers['retry-after']);
        rateLimitResetTime = Date.now() + (retryAfter * 1000);
        console.log(`⏰ Rate limit resets in ${retryAfter} seconds`);
      }
    }

    return { success: false, result: null, error: String(error) };
  }
}

// Check if we're still rate limited
function checkRateLimitStatus(): boolean {
  if (!isRateLimited) return false;

  if (rateLimitResetTime && Date.now() > rateLimitResetTime) {
    console.log('✅ Rate limit period expired, returning to normal mode');
    isRateLimited = false;
    rateLimitResetTime = null;
    return false;
  }

  return true;
}

// Main ReAct loop with offline fallback
export async function reactLoop(
  provider: any,
  messages: LLMMessage[],
  systemPrompt: string,
  maxLoops: number = 10
): Promise<{
  response: string;
  toolsUsed: string[];
  loops: number;
  offlineMode?: boolean;
  rateLimited?: boolean;
}> {

  const toolsUsed: string[] = [];
  let loopCount = 0;

  // Check rate limit status
  const currentlyRateLimited = checkRateLimitStatus();

  // Get last user message
  const lastUserMessage = messages.filter(m => m.role === 'user').pop();
  if (!lastUserMessage) {
    return { response: 'No user message', toolsUsed: [], loops: 0 };
  }

  // Build conversation
  const conversation: any[] = [
    {
      role: 'system',
      content: currentlyRateLimited
        ? `${systemPrompt}\n\n⚠️ OFFLINE MODE: You are currently rate-limited. You can only use offline tools (calculate, process_text, json_operations, datetime_operations, hash_data, etc.). These tools work without any API calls.`
        : systemPrompt
    },
    { role: 'user', content: lastUserMessage.content }
  ];

  while (loopCount < maxLoops) {
    loopCount++;
    console.log(`🔄 ReAct loop ${loopCount}/${maxLoops}${currentlyRateLimited ? ' [OFFLINE MODE]' : ''}`);

    try {
      // Call LLM with appropriate tools
      const availableTools = currentlyRateLimited ? getOfflineToolsOnly() : getOpenAITools();

      const result = await provider.chatComplete(conversation, {
        tools: availableTools,
        tool_choice: 'auto'
      });

      // Add assistant message to conversation
      const assistantMsg: any = {
        role: 'assistant',
        content: result.text || ''
      };

      if (result.toolCalls && result.toolCalls.length > 0) {
        assistantMsg.tool_calls = result.toolCalls;
      }
      conversation.push(assistantMsg);

      // If no tool calls, we're done
      if (!result.toolCalls || result.toolCalls.length === 0) {
        console.log(`✅ ReAct complete after ${loopCount} loops`);
        return {
          response: result.text || '',
          toolsUsed,
          loops: loopCount,
          offlineMode: currentlyRateLimited,
          rateLimited: currentlyRateLimited
        };
      }

      // Execute each tool call
      for (const toolCall of result.toolCalls) {
        const funcName = toolCall.function?.name || toolCall.name;
        const funcArgs = typeof toolCall.function?.arguments === 'string'
          ? JSON.parse(toolCall.function.arguments)
          : toolCall.function?.arguments || toolCall.arguments || {};

        // Check if trying to use online tool while rate limited
        if (currentlyRateLimited && !isOfflineTool(funcName)) {
          console.warn(`⚠️ Attempted to use online tool ${funcName} while rate limited - skipping`);
          conversation.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            content: JSON.stringify({
              error: 'Tool unavailable - currently rate limited. Please use offline tools only.',
              offline_tools_available: offlineTools.map(t => t.name)
            })
          });
          continue;
        }

        toolsUsed.push(funcName);
        const toolResult = await executeTool(funcName, funcArgs);

        // Add tool result to conversation
        conversation.push({
          role: 'tool',
          tool_call_id: toolCall.id,
          content: JSON.stringify(
            toolResult.success
              ? { ...toolResult.result, _offline: toolResult.offline }
              : { error: toolResult.error }
          ).slice(0, 8000) // Prevent token overflow
        });
      }

    } catch (error: any) {
      console.error('❌ ReAct loop error:', error);

      // Check if it's a rate limit error
      if (error.status === 429 || error.message?.includes('rate limit')) {
        console.warn('🚨 Rate limit hit during loop! Switching to offline mode...');
        isRateLimited = true;

        return {
          response: `I've hit a rate limit. I can still help you using offline tools for:\n- Mathematical calculations\n- Text processing\n- JSON operations\n- Date/time calculations\n- Data encoding/hashing\n\nWhat would you like me to do?`,
          toolsUsed,
          loops: loopCount,
          offlineMode: true,
          rateLimited: true
        };
      }

      // Other errors - try to recover
      console.error('Attempting to continue despite error...');
    }
  }

  console.log(`⚠️ ReAct hit max loops (${maxLoops}) - making final synthesis call`);

  // Make a final LLM call WITHOUT tools to synthesize a proper response
  try {
    conversation.push({
      role: 'user',
      content: 'Based on all the information gathered above, provide a clear, helpful response to the original question. Do not output raw JSON or tool results - summarize the findings in natural language.'
    });

    const synthesisResult = await provider.chatComplete(conversation, {
      tools: [],
      tool_choice: 'none'
    });

    console.log(`✅ Synthesis complete after max loops`);
    return {
      response: synthesisResult.text || 'I gathered information but could not synthesize a response.',
      toolsUsed,
      loops: loopCount,
      offlineMode: currentlyRateLimited,
      rateLimited: currentlyRateLimited
    };
  } catch (synthesisError: any) {
    console.error(`❌ Synthesis failed:`, synthesisError);

    // Even synthesis failed - return offline message
    if (synthesisError.status === 429) {
      return {
        response: 'I\'m currently rate limited and cannot complete this request. I can help with offline tasks like calculations, text processing, and data formatting.',
        toolsUsed,
        loops: loopCount,
        offlineMode: true,
        rateLimited: true
      };
    }

    return {
      response: 'I gathered information but encountered an error synthesizing the response. Please try again.',
      toolsUsed,
      loops: loopCount
    };
  }
}

// Helper: Manually trigger offline mode (for testing)
export function setOfflineMode(offline: boolean) {
  isRateLimited = offline;
  console.log(`🔧 Offline mode ${offline ? 'enabled' : 'disabled'}`);
}

// Helper: Check current mode
export function getOperatingMode(): { offline: boolean; resetTime: number | null } {
  return {
    offline: checkRateLimitStatus(),
    resetTime: rateLimitResetTime
  };
}
