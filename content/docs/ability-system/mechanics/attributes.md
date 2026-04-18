---
title: "Attributes: O Sistema de Status"
type: docs
weight: 3
---

Os **Attributes** são os valores numéricos que definem as capacidades de um ator (Vida, Mana, Força, Velocidade).

## 📊 ASAttributeSet

Diferente de variáveis soltas num script, os atributos são agrupados em um **Set**. Isso permite:

- **Centralização**: Toda a lógica de "Dano" ou "Defesa" fica em um lugar.
- **Segurança**: Valores são protegidos contra estouro (Min/Max).
- **Simulação**: O sistema sabe exatamente como recalcular o valor atual baseado nos modificadores ativos.

---

## 🚗 Attribute Drivers (Derivação)

Uma das funcionalidades mais potentes é a capacidade de um atributo "dirigir" outro.

**Exemplo: Força aumenta o Ataque.**

- Atributo: `Strength`
- Atributo: `AttackPower`
- Driver: `AttackPower = Strength * 2.0`

Sempre que sua `Strength` mudar, o `AttackPower` será recalculado automaticamente pela engine no próximo tick.

---

## 📈 Ordem de Cálculo

Para garantir o determinismo (vital para multiplayer), os atributos seguem esta ordem:

1. **Base Value**: O valor "puro" do personagem.
2. **Drivers**: Aplicação de cálculos derivados de outros atributos.
3. **Flat Modifiers**: Adições diretas (ex: +5 de escudo do item).
4. **Percentage Modifiers**: Multiplicadores finais (ex: +10% de fúria).

> [!NOTE] Mudanças no `Base Value` são permanentes. Mudanças em `Modifiers` são temporárias e ligadas a `ASEffects`.
