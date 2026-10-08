# 解説役のキャラクター選択室

**[探偵役を先に見る](https://vtuber-character-gallery-20261008.pages.dev/?view=detective)**

**[キャラクターを選ぶ画面を開く](https://vtuber-character-gallery-20261008.pages.dev/)**

音声を当てたショートムービーで、ニュースやいろいろなことを説明してくれるキャラクターを選ぶための画面と画像を管理します。

## できること

- 同じモチーフをまとめて比較。紅茶は紅茶、お米はお米として並びます。
- ２０人ごとの服や世界観のテーマ、探偵役、髪型、帽子、服で絞り込み。
- 設定シートを拡大し、表情やミニキャラを確認。
- 気に入った番号と理由を保存し、選択ファイルを読み込み・書き出し。
- 人物を大きく表示し、スマートフォンでも選択。

候補には約５頭身の丸く親しみのある造形を採用。明るく人懐っこく一生懸命で少しドジ、顔や髪の輪郭で覚えられる方向です。お米・ラムネ・パンと麦や、切手・木の実・きなこ・ほうじ茶・積み木が本人の注目モチーフです。

探偵役の組は、茶色のだぼっとした服、大きいチェック柄、でっかい虫眼鏡で「調べて、確かめて、ニュースを届ける」子を比較します。

## 構成

- `site/`：公開する画面と生成画像。画像原本と同じ内容を保存。
- `data/catalog.json`：候補の表示情報。
- `data/design-plans/`：各組の共通条件と個別の画像生成指示。
- `template.html`：画面の正本。
- `scripts/build.mjs`：表示情報から公開画面を生成。
- `scripts/serve.mjs`：ローカルの確認用サーバー。

内蔵画像生成を使用。設定資料の画像を選ぶ画面であり、音声、動画、パーツ分けした原画や動作設定は別の制作工程です。選択率は閲覧した本人の好みであり、一般の人気や企業の評価の実測ではありません。

## ローカルで開く

```powershell
pnpm install
pnpm build
pnpm preview
```

表示されたローカルのURLをブラウザーで開きます。

## Cloudflare Pagesへ反映

```powershell
pnpm deploy
```

認証済みのCloudflareアカウントを使用します。認証情報、個人の絶対パス、ローカルの保存記録はこのリポジトリに含めません。

画像生成の指示文の正本は保存しています。画像を再生成する場合は、共通条件とその１人の条件だけを渡して独立した１枚を作り、過去の人物の着せ替えに固定しない運用です。
## 収録数と確認

候補470人、試案・修正前25枚、合計495枚を収録。最初の２０人＋追加１００人＋追加１９５人＋探偵役４０人＋好みを踏まえた主役６案＋綿花の個性３案＋綿花のコンセプト１０案＋田舎の綿花５案＋顔と髪で覚える１０案＋ビー玉の衣装６案＋原案142のスポーツ６案＋透け感とバランス３案＋透け感と丸み３案＋腕と裾の透け感３案＋白い内側と襟・パンツ３案＋白キャミの重ね３案＋パンツと靴６案＋サイズと小物１０案＋かたち05の小物６案＋統合デザイン２案＋パンツのサイズ２案＋大人版２案＋見送りの相棒初案６案＋青いガラスの相棒１０案＋図太い猫と部分シアー衣装３案＋服の遊び心と猫の目４案＋相棒01固定の服３案です。途中で追加生成を停止した５つの未生成枠は画像として掲載していません。

[追加した主役６案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=lead)

[綿花の個性３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=cotton)

[綿花のコンセプト１０案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=cotton10)

[１０案の設計意図と比較基準](docs/綿花１０案の設計.md)

[田舎の綿花５案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=rural)

[田舎の綿花５案の設計](docs/田舎の綿花５案の設計.md)

[顔と髪で覚える１０案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=identity)

[顔と髪の１０案の設計](docs/顔と髪の１０案の設計.md)

[ビー玉の衣装６案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=marble)

[ビー玉衣装６案の設計](docs/ビー玉衣装６案の設計.md)

[原案142のスポーツ・透け感４９案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=sport)

[透け感と全身バランスの３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=sheer)

[スポーツ６案の設計](docs/ビー玉スポーツ６案の設計.md)・[透け感３案の設計](docs/ビー玉透け感３案の設計.md)

[透け感と丸みの改良３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=soft)

[改良３案の設計](docs/ビー玉透け感と丸み３案の設計.md)

[腕と裾の透け感３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=airy)

[腕と裾の３案の設計](docs/ビー玉腕と裾３案の設計.md)

[白い内側と襟・パンツ３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=white)

[白い内側と襟・パンツ３案の設計](docs/ビー玉白い内側と襟・パンツ３案の設計.md)

[白キャミの重ね３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=cami)

[白キャミ３案の設計](docs/ビー玉白キャミ３案の設計.md)

[パンツと靴６案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=bottoms)

[パンツと靴６案の設計](docs/ビー玉パンツと靴６案の設計.md)

[サイズと小物１０案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=shape)

[サイズと小物１０案の設計](docs/ビー玉サイズと小物１０案の設計.md)

[かたち05の小物６案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=accessories)

[小物６案の設計](docs/ビー玉05の小物６案の設計.md)

[ビー玉の統合デザインを見る](https://vtuber-character-gallery-20261008.pages.dev/?view=final)

[統合デザインの設計](docs/ビー玉統合デザインの設計.md)・[調整後の設計](docs/ビー玉統合デザイン02の設計.md)

[パンツのサイズ２案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=size)

[パンツのサイズ２案の設計](docs/ビー玉パンツサイズ２案の設計.md)

[大人版２案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=adult)

[大人版２案の設計](docs/ビー玉大人版２案の設計.md)

[最新の相棒01固定・服の仕上げ３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=partner01)

[採用した相棒と衣装の基準](docs/採用した相棒と衣装の基準.md)・[服３案の設計](docs/相棒01を固定した服３案の設計.md)

[服の遊び心と猫の目４案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=playful)

[服と目の４案の設計](docs/服の遊び心と猫の目４案の設計.md)

[図太い猫と部分シアー衣装３案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=buddy-character)

[改良３案の設計](docs/図太い猫と部分シアー３案の設計.md)

[子供版01と青いガラス猫・狸１０案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=buddy)

[ガラスの相棒１０案の設計](docs/ガラスの相棒１０案の設計.md)

[見送りの相棒初案６案を見る](https://vtuber-character-gallery-20261008.pages.dev/?view=buddy-old)

画像コピーの内容をハッシュ値で確認。画面の絞り込み、モチーフのまとめ表示、拡大、選択理由、保存ファイルの読み込み・書き出し、携帯幅を検証しています。
