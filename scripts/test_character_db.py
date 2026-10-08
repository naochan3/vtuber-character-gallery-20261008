"""台帳の検索・履歴・参照整合性を検証する。"""
import copy
import json
import sqlite3
import uuid
import unittest
from pathlib import Path
from character_db import DEFAULT_SOURCE, build, search, validate, prompt_for


class CharacterDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = DEFAULT_SOURCE.parents[2]/'.local/tests'/uuid.uuid4().hex
        self.temp.mkdir(parents=True)
        self.db = self.temp/'characters.sqlite3'
        self.source = self.temp/'source.json'
        self.data = json.loads(DEFAULT_SOURCE.read_text(encoding='utf-8'))
        self.save()
        build(self.source, self.db)

    def save(self):
        self.source.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def test_search_japanese_filters(self):
        results = search(self.db, '驚', actor='女の子', kind='表情')
        self.assertTrue({'E09', 'E10'}.issubset({r['id'] for r in results}))
        self.assertTrue(all(r['character']=='女の子' for r in results))
        self.assertEqual(6, len(search(self.db, '502', status='採用済み')))
        self.assertTrue(search(self.db, 'メモ'))
        self.assertLess(len(search(self.db, '猫')), len(self.data['records']))
        self.assertTrue(search(self.db, '口調', actor='ガラス猫'))

    def test_untrusted_search_is_literal_and_read_only(self):
        for query in ["' OR 1=1 --", '%', '_', "'; DROP TABLE entries; --"]:
            self.assertEqual([], search(self.db, query))
        self.assertEqual(91, len(search(self.db)))

    def test_rebuild_and_revision_history(self):
        build(self.source, self.db)
        with sqlite3.connect(self.db) as con:
            self.assertEqual(1, con.execute('SELECT COUNT(*) FROM revisions').fetchone()[0])
        self.data['records']=[r for r in self.data['records'] if r['id']!='B02']
        self.data['version']='1.0.1'
        self.save()
        build(self.source, self.db)
        with sqlite3.connect(self.db) as con:
            self.assertEqual(2, con.execute('SELECT COUNT(*) FROM revisions').fetchone()[0])
            self.assertEqual(0, con.execute("SELECT active FROM entries WHERE id='B02'").fetchone()[0])
        self.assertEqual(90,len(search(self.db)))

    def test_bad_reference_and_duplicate_are_rejected(self):
        data=copy.deepcopy(self.data)
        data['records'].append(data['records'][0])
        with self.assertRaises(ValueError):validate(data)
        data=copy.deepcopy(self.data)
        next(r for r in data['records'] if r['id']=='P01')['expression']='E99'
        with self.assertRaises(ValueError):validate(data)

    def test_prompt_preserves_accepted_design(self):
        result=prompt_for(self.data,'E10')
        self.assertIn('502',result)
        self.assertIn('E10',result)
        self.assertIn('胴体・胸・背中は不透明',result)
        with self.assertRaises(ValueError):prompt_for(self.data,'E99')


if __name__=='__main__':unittest.main()
