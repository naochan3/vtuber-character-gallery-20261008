"""設定の正本から内部台帳を構築し、日本語で検索する。"""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / 'data/characters/marble-502.json'
DEFAULT_DB = ROOT / '.local/characters.sqlite3'


def validate(data):
    records = data['records']
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('設定番号が重複しています')
    sheets = {s['id'] for s in data['sheets']}
    allowed = {'採用済み', '設定案', '制作案', '未確定'}
    for r in records:
        if r['status'] not in allowed:
            raise ValueError('不明な確定状態です：' + r['id'])
        if r.get('sheet') and r['sheet'] not in sheets:
            raise ValueError('対応する資料がありません：' + r['id'])
        for key in ('next', 'expression', 'girlExpression', 'catExpression'):
            if key in r and key != 'expression' and r[key] not in ids:
                raise ValueError('存在しない表情参照です：' + r['id'])
            if key == 'expression' and r['kind'] == 'ポーズ' and r[key] not in ids:
                raise ValueError('存在しない表情参照です：' + r['id'])
    for s in data['sheets']:
        expected = {r['id'] for r in records if r.get('sheet') == s['id']}
        if set(s['recordIds']) != expected:
            raise ValueError('資料の対応番号が一致しません：' + s['id'])


def build(source=DEFAULT_SOURCE, db=DEFAULT_DB):
    source, db = Path(source), Path(db)
    data = json.loads(source.read_text(encoding='utf-8'))
    validate(data)
    serialized = json.dumps(data, ensure_ascii=False, sort_keys=True)
    checksum = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
    db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db) as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS characters (
          id TEXT PRIMARY KEY, version TEXT NOT NULL, source_hash TEXT NOT NULL,
          aliases TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS entries (
          character_id TEXT NOT NULL, id TEXT NOT NULL, kind TEXT NOT NULL,
          actor TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL,
          search_text TEXT NOT NULL, payload TEXT NOT NULL, active INTEGER NOT NULL,
          PRIMARY KEY(character_id, id));
        CREATE INDEX IF NOT EXISTS entries_lookup ON entries(character_id, kind, actor, status);
        CREATE TABLE IF NOT EXISTS revisions (
          character_id TEXT NOT NULL, source_hash TEXT NOT NULL,
          version TEXT NOT NULL, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
          payload TEXT NOT NULL, PRIMARY KEY(character_id, source_hash));
        ''')
        with con:
            con.execute('INSERT OR IGNORE INTO revisions(character_id,source_hash,version,payload) VALUES(?,?,?,?)',
                        (data['id'], checksum, data['version'], serialized))
            con.execute('INSERT INTO characters VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET version=excluded.version, source_hash=excluded.source_hash, aliases=excluded.aliases, payload=excluded.payload',
                        (data['id'], data['version'], checksum, json.dumps(data['aliases'], ensure_ascii=False), serialized))
            con.execute('UPDATE entries SET active=0 WHERE character_id=?', (data['id'],))
            for r in data['records']:
                payload = json.dumps(r, ensure_ascii=False)
                search = ' '.join(a for a in data['aliases'] if a != 'ガラス猫') + ' ' + payload
                con.execute('INSERT INTO entries VALUES(?,?,?,?,?,?,?,?,1) ON CONFLICT(character_id,id) DO UPDATE SET kind=excluded.kind,actor=excluded.actor,title=excluded.title,status=excluded.status,search_text=excluded.search_text,payload=excluded.payload,active=1',
                            (data['id'], r['id'], r['kind'], r['character'], r['title'], r['status'], search, payload))
    return dict(records=len(data['records']), database=str(db), source_hash=checksum)


def search(db=DEFAULT_DB, query='', kind=None, actor=None, status=None, limit=100):
    db = Path(db).resolve()
    if not db.exists():
        raise FileNotFoundError('内部台帳がありません。先に build を実行してください')
    clauses, values = ['active=1'], []
    for column, value in [('kind', kind), ('actor', actor), ('status', status)]:
        if value:
            clauses.append(column + '=?')
            values.append(value)
    for term in query.split():
        clauses.append("search_text LIKE ? ESCAPE '\\'")
        values.append('%' + term.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%')
    values.append(max(1, min(int(limit), 500)))
    with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as con:
        rows = con.execute('SELECT payload FROM entries WHERE ' + ' AND '.join(clauses) + ' ORDER BY character_id,id LIMIT ?', values).fetchall()
    return [json.loads(row[0]) for row in rows]


def prompt_for(data, identifier):
    record = next((r for r in data['records'] if r['id'] == identifier), None)
    if record is None:
        raise ValueError('指定された設定番号はありません：' + identifier)
    locks = '\n'.join(r['title'] + '：' + r['body'] for r in data['records'] if r['status'] == '採用済み')
    return '採用正本502の画像を必ず参照してください。\n' + locks + '\n\n今回の演技指定：\n' + json.dumps(record, ensure_ascii=False, indent=2) + '\n\n設定案の演技であり、衣装・人物・猫を別デザインへ変更しない。'


def main():
    parser = argparse.ArgumentParser(description='キャラクター設定の内部台帳')
    parser.add_argument('command', choices=['build', 'search', 'prompt'])
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--kind')
    parser.add_argument('--actor')
    parser.add_argument('--status')
    parser.add_argument('--limit', type=int, default=100)
    args = parser.parse_args()
    if args.command == 'build':
        result = build(args.source, args.db)
    elif args.command == 'search':
        result = search(args.db, args.query, args.kind, args.actor, args.status, args.limit)
    else:
        print(prompt_for(json.loads(args.source.read_text(encoding='utf-8')), args.query))
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
