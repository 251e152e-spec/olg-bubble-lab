# olg-bubble-lab

[![CI](https://github.com/rin-moromizato/olg-bubble-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/rin-moromizato/olg-bubble-lab/actions/workflows/ci.yml)

世代重複（OLG）モデルにおけるバブル存在の「必要条件」を、自己使用系列 $R^*_t$（自国的利子率）と成長率 $G$ の比の対数系列 $x_t = \log(R^*_t / G)$ に対して数値的にチェック・可視化する小さな CLI / Python ライブラリです。

## 目的

非定常な OLG 経済のバブル理論研究において、$R^*_t$ が高レジーム・低レジームを行き来する系列に対して

- **K 一様頻度条件**（∃K, ∃γ>0, ∀t: 区間 [t, t+K) での $x$ の平均が −γ 以下）
- **Cesàro（対数平均）条件**（累積平均が長期的に非正へ収束するか）

の 2 条件が成立するかどうかを、手計算やその場しのぎの Python スクリプトではなく再利用可能なツールとしてチェックしたい、という研究上の実用ニーズから作りました。周期レジームや「ブロック長が発散する反例系列」を自動生成して両条件の成否を比較できるため、反例の探索や具体例の検証にそのまま使えます。

## インストール方法

```bash
git clone https://github.com/rin-moromizato/olg-bubble-lab.git
cd olg-bubble-lab
pip install .
```

（[uv](https://github.com/astral-sh/uv) を使う場合は `uv pip install .` でも同様です。）

## 一番簡単な使い方

周期レジーム（H を n_high 期、L を n_low 期、これを n_periods 回繰り返す）が頻度条件を満たすかチェックする:

```bash
olg-bubble check-periodic \
  --r-high 1.5 --r-low 0.5 --g 1.0 \
  --n-high 1 --n-low 1 --n-periods 20 \
  --k 2 --gamma 0.01
```

ブロック長が発散する反例系列（1,1,2,2,3,3,...）をチェック・可視化する:

```bash
olg-bubble check-diverging --r-high 2.0 --r-low 0.5 --g 1.0 --n-blocks 8 --k 3
olg-bubble plot-diverging  --r-high 2.0 --r-low 0.5 --g 1.0 --n-blocks 8 --output diverging.pdf
```

自分の CSV データ（列 `R_star`, `G`）をチェックすることもできます:

```bash
olg-bubble check-csv --path data/my_rates.csv --k 5 --gamma 0.0
```

Python から直接使う場合:

```python
from olg_bubble_lab import periodic_regime, check_frequency_condition, check_cesaro_condition

x = periodic_regime(r_high=1.5, r_low=0.5, g=1.0, n_high=2, n_low=3, n_periods=10)
print(check_frequency_condition(x, k=5, gamma=0.01))
print(check_cesaro_condition(x))
```

`plot-periodic` / `plot-diverging` はレジーム系列・累積平均・含意される価格経路の 3 段グラフを PDF（ベクター形式）で保存します。

## 開発環境設定（開発者向け）

[uv](https://github.com/astral-sh/uv) を利用します。

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -e ".[dev]"
```

## テストの実行方法（開発者向け）

```bash
. .venv/bin/activate
pytest
```

型チェックと Lint:

```bash
mypy src
ruff check src tests
```

## ライセンス

MIT License. `LICENSE` を参照してください。
