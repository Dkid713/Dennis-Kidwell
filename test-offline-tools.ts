/**
 * Test Suite for Offline Tools
 * Run this to verify offline tools work before integration
 */

import { offlineTools, executeOfflineTool } from './athena-offline-tools';

async function testAllOfflineTools() {
  console.log('🧪 Testing Athena Offline Tools\n');
  console.log('=' + '='.repeat(60));

  let passed = 0;
  let failed = 0;

  // Test 1: Calculator
  console.log('\n📊 Test 1: Calculate (Math Operations)');
  try {
    const calc1 = await executeOfflineTool('calculate', { expression: '2 + 2' });
    console.log('  ✓ Basic math:', calc1);
    assert(calc1.result === 4, 'Expected 2+2=4');

    const calc2 = await executeOfflineTool('calculate', { expression: 'Math.sqrt(144)' });
    console.log('  ✓ Square root:', calc2);
    assert(calc2.result === 12, 'Expected sqrt(144)=12');

    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 2: Unit Conversion
  console.log('\n🌡️  Test 2: Convert Units');
  try {
    const conv = await executeOfflineTool('convert_units', {
      value: 0,
      from: 'celsius',
      to: 'fahrenheit'
    });
    console.log('  ✓ Temperature conversion:', conv);
    assert(conv.converted.value === 32, 'Expected 0°C = 32°F');
    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 3: Text Processing
  console.log('\n📝 Test 3: Process Text');
  try {
    const upper = await executeOfflineTool('process_text', {
      text: 'hello world',
      operation: 'uppercase'
    });
    console.log('  ✓ Uppercase:', upper);
    assert(upper.result === 'HELLO WORLD', 'Expected uppercase conversion');

    const words = await executeOfflineTool('process_text', {
      text: 'one two three',
      operation: 'wordcount'
    });
    console.log('  ✓ Word count:', words);
    assert(words.count === 3, 'Expected 3 words');

    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 4: Regex Matching
  console.log('\n🔍 Test 4: Regex Match');
  try {
    const regex = await executeOfflineTool('regex_match', {
      text: 'Contact: test@example.com and admin@site.org',
      pattern: '\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',
      flags: 'g'
    });
    console.log('  ✓ Email extraction:', regex);
    assert(regex.matches.length === 2, 'Expected 2 email matches');
    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 5: JSON Operations
  console.log('\n🗂️  Test 5: JSON Operations');
  try {
    const validate = await executeOfflineTool('json_operations', {
      data: '{"name": "Athena", "version": "6"}',
      operation: 'validate'
    });
    console.log('  ✓ Valid JSON:', validate);
    assert(validate.valid === true, 'Expected valid JSON');

    const format = await executeOfflineTool('json_operations', {
      data: '{"a":1,"b":2}',
      operation: 'format'
    });
    console.log('  ✓ Formatted JSON:', format.result.split('\n').length > 1);

    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 6: Date/Time Operations
  console.log('\n🕐 Test 6: DateTime Operations');
  try {
    const now = await executeOfflineTool('datetime_operations', {
      operation: 'now'
    });
    console.log('  ✓ Current time:', now.iso);
    assert(now.iso && now.unix && now.readable, 'Expected time fields');

    const tomorrow = await executeOfflineTool('datetime_operations', {
      operation: 'add',
      amount: 1,
      unit: 'days'
    });
    console.log('  ✓ Add 1 day:', tomorrow.result);

    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 7: Hashing
  console.log('\n🔐 Test 7: Hash Data');
  try {
    const hash = await executeOfflineTool('hash_data', {
      data: 'hello world',
      algorithm: 'sha256'
    });
    console.log('  ✓ SHA256 hash:', hash.hash.substring(0, 16) + '...');
    assert(hash.hash.length === 64, 'Expected 64-char SHA256 hash');
    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 8: UUID Generation
  console.log('\n🆔 Test 8: Generate UUID');
  try {
    const uuid = await executeOfflineTool('generate_uuid', {});
    console.log('  ✓ UUID:', uuid.uuid);
    assert(uuid.uuid.match(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i), 'Expected valid UUID v4');
    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Test 9: Encoding/Decoding
  console.log('\n🔤 Test 9: Encode/Decode');
  try {
    const encoded = await executeOfflineTool('encode_decode', {
      data: 'Hello Athena!',
      operation: 'base64_encode'
    });
    console.log('  ✓ Base64 encode:', encoded.result);

    const decoded = await executeOfflineTool('encode_decode', {
      data: encoded.result,
      operation: 'base64_decode'
    });
    console.log('  ✓ Base64 decode:', decoded.result);
    assert(decoded.result === 'Hello Athena!', 'Expected round-trip encoding');

    passed++;
  } catch (error) {
    console.error('  ✗ Failed:', error);
    failed++;
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log(`\n📊 Test Results: ${passed} passed, ${failed} failed`);

  if (failed === 0) {
    console.log('✅ All offline tools working perfectly!');
    console.log('\n🚀 Ready to integrate into Athena!');
  } else {
    console.log('❌ Some tests failed. Check the errors above.');
  }

  console.log('\n' + '='.repeat(60));
}

// Simple assertion helper
function assert(condition: boolean, message: string) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

// Run tests
testAllOfflineTools().catch(console.error);

// Export for use in other tests
export { testAllOfflineTools };
