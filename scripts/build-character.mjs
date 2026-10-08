import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export function buildCharacter(){
  const source=JSON.parse(fs.readFileSync(path.join(root,'data/characters/marble-502.json'),'utf8'));
  const catalog=JSON.parse(fs.readFileSync(path.join(root,'data/catalog.json'),'utf8'));
  const findFile=id=>{const item=catalog.items.find(x=>x.id===id);if(!item?.file||!/^assets\/candidate-[\w-]+\.png$/.test(item.file))throw Error('画像が見つかりません：'+id);if(!fs.existsSync(path.join(root,'site',item.file)))throw Error('画像ファイルがありません：'+id);return item.file;};
  const data={...source,canonicalFile:findFile(source.canonicalCandidate),sheets:source.sheets.map(s=>({...s,file:findFile(s.candidateId)}))};
  const serialized=JSON.stringify(data).replaceAll('<','\\u003c');
  const html=fs.readFileSync(path.join(root,'character-template.html'),'utf8').replace('__CHARACTER_DATA__',serialized);
  fs.writeFileSync(path.join(root,'site/character-502.html'),html);
  fs.writeFileSync(path.join(root,'site/character-502.json'),JSON.stringify(data));
  const lines=['# ビー玉の子とガラス猫・詳細設定 第１版','',source.statusNote,'',source.summary,''];
  let previous='';for(const r of source.records){if(r.kind!==previous){lines.push('## '+r.kind,'');previous=r.kind;}lines.push('### '+r.id+' '+r.title+'［'+r.status+'］','',r.body,'');for(const [key,label] of Object.entries({trigger:'きっかけ',face:'顔',gesture:'仕草',line:'台詞',next:'次の表情',girlLine:'女の子の台詞',catLine:'猫の台詞',expression:'対応表情'})){if(r[key])lines.push('- '+label+'：'+r[key]);}lines.push('');}
  fs.writeFileSync(path.join(root,'docs/502詳細設定集.md'),lines.join('\n'));
  console.log('502の設定ページを生成しました：'+source.records.length+'項目、'+source.sheets.length+'枚');
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))buildCharacter();
