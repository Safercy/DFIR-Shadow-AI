"""Runs ON the endpoint (via Velociraptor execve()), against a directory
Velociraptor has ALREADY staged for us (see the artifact's export: block),
to recover M365 Copilot conversation titles (chatName) cached from the
GetChats API. Prints one JSON object to stdout; nothing else goes to
stdout (diagnostics/errors go to stderr).

This script does NOT copy Cache_Data itself. An earlier version tried a
plain Win32 copy (shutil.copytree) directly against the live directory,
but Chromium's block files (data_0..data_3, index) are held open by the
running WebView2/Edge process with a sharing mode that denies read access
to other processes -- shutil.copytree failed with PermissionError/Errno 13
on exactly those files (individual f_* entry files copied fine). The
artifact's VQL now stages a copy first using Velociraptor's `ntfs`
accessor (raw disk read, bypasses share-mode locks), the same technique
already used elsewhere in this investigation for the same reason. By the
time this script runs, --cache-dir already points at that staged, private,
unlocked copy -- reading it here needs nothing special.

Usage: python.exe extract_chat_titles_live.py --cache-dir "<staged copy of Cache_Data>" [--key-regex ...] [--regex ...]
"""
import argparse, json, re, sys, traceback, csv, datetime, pathlib
from ccl_chromium_reader import ccl_chromium_cache

def eprint(*a):
    print(*a, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument('--cache-dir', required=True, help='Path to an already-staged copy of Cache_Data.')
parser.add_argument('--key-regex', default=r'm365Copilot/GetChats')
parser.add_argument('--regex', default='', help='Optional filter on ChatName only.')
args = parser.parse_args()
key_pattern = re.compile(args.key_regex)
name_pattern = re.compile(args.regex) if args.regex else None

result = {'ConversationTitles': [], 'Diagnostics': {}, 'Errors': []}

copied = pathlib.Path(args.cache_dir)
if not copied.exists():
    result['Diagnostics']['Status'] = 'CACHE_DIR_NOT_FOUND'
    print(json.dumps(result, ensure_ascii=True))
    sys.exit(0)

decoded = copied / '_decoded'
try:
    ccl_chromium_cache.main([str(copied), str(decoded)])
except Exception:
    result['Errors'].append({'Stage': 'ccl_chromium_cache decode', 'Error': traceback.format_exc()})
    print(json.dumps(result, ensure_ascii=True))
    sys.exit(0)

report = decoded / 'cache_report.csv'
if not report.exists():
    result['Diagnostics']['Status'] = 'NO_CACHE_REPORT'
    print(json.dumps(result, ensure_ascii=True))
    sys.exit(0)

with report.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
matched = [r for r in rows if key_pattern.search(r.get('key', ''))]
result['Diagnostics'] = {'TotalCacheEntries': len(rows), 'MatchingKeyEntries': len(matched)}

titles = {}
for row in matched:
    file_hash = row.get('file_hash', '')
    body_path = decoded / 'cache_files' / file_hash
    if not body_path.exists():
        result['Errors'].append({'CacheKey': row.get('key', ''), 'FileHash': file_hash, 'Stage': 'body file missing'})
        continue
    raw = body_path.read_bytes()
    try:
        obj = json.loads(raw.decode('utf-8'))
    except Exception:
        result['Errors'].append({'CacheKey': row.get('key', ''), 'FileHash': file_hash, 'Stage': 'decode/JSON parse failed'})
        continue
    for chat in obj.get('chats', []):
        name = chat.get('chatName')
        if name_pattern and not (name and name_pattern.search(name)):
            continue
        create_raw = chat.get('createTimeUtc')
        update_raw = chat.get('updateTimeUtc')
        key = (chat.get('conversationId'), name)
        entry = {
            'ConversationId': chat.get('conversationId'),
            'ChatName': name,
            'CreateTimeUtcRaw': create_raw,
            'CreateTimeUtc': (datetime.datetime.fromtimestamp(create_raw / 1000, datetime.timezone.utc).isoformat()
                              if create_raw else None),
            'UpdateTimeUtcRaw': update_raw,
            'UpdateTimeUtc': (datetime.datetime.fromtimestamp(update_raw / 1000, datetime.timezone.utc).isoformat()
                              if update_raw else None),
            'ThreadId': chat.get('threadId'),
            'EvidenceType': 'HTTPCacheGetChatsTitle',
            'ExtractionMethod': 'ChromiumSimpleCache.GetChats.chatName.LiveExec',
            'CacheRequestKey': row.get('key', ''),
            'CacheRequestTimeRaw': row.get('request_time', ''),
            'CacheFileHash': file_hash,
        }
        if key not in titles or (entry['CacheRequestTimeRaw'] or '') > (titles[key]['CacheRequestTimeRaw'] or ''):
            titles[key] = entry
result['ConversationTitles'] = sorted(titles.values(), key=lambda t: t['CreateTimeUtcRaw'] or 0)
print(json.dumps(result, ensure_ascii=True))
