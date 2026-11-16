# Entrega – Onfly Desafio

## Defeitos corrigidos (causa raiz)

| # | Arquivo | Causa raiz |
|---|---------|-----------|
| 1 | `repositories/csv_reservation_repository.py` | O `read()` parava em 200 linhas (`break`), então 100 das 300 reservas eram ignoradas. |
| 2 | `services/status_policy.py` | `is_billable` só excluía `CANCELLED`, deixando `NO_SHOW` entrar nos valores e noites. Agora só `CONFIRMED`. |
| 3 | `services/stay_calculator.py` | Subtraía só o dia do mês (`checkout.day - checkin.day`), quebrando na virada de mês/ano. Agora `(checkout - checkin).days`. |
| 4 | `services/currency_converter.py` | Dividia pela taxa em vez de multiplicar e usava `float`. Agora `amount * rate` com `Decimal`. |
| 5 | `services/report_builder.py` | O ranking de hotéis estava em ordem crescente de valor. Agora valor decrescente, empate por `hotel_id` crescente. |

Cada correção tem um comentário curto `# CORREÇÃO:` no ponto da mudança.

## Como investiguei

1. Li o README e todo o código em `src/`, que é pequeno.
2. Rodei `pytest` e vi os testes falharem.
3. Comparei cada regra de negócio do README com o código correspondente.
4. Conferi que o CSV tem 300 linhas e que o relatório deveria contar 300 reservas (era o que revelou o limite de 200).
5. Validei na amostra `data/exemplo-validacao.csv` contra a tabela do README.

## Como validar

```bash
pip install -r requirements-dev.txt
pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

## Resultado

- `pytest -q`: **10 passed** (5 fornecidos + 5 novos em `tests/test_extra.py`).
- Amostra de validação: bate com o README (12 / 9 / 2 / 1, 28 noites, `7566.00`, média `270.21`, by_month e top_hotels iguais).
- Dataset completo: 300 reservas, 235 confirmadas, 1347 noites, `396170.00` BRL.
- `ruff check .`: sem erros.
