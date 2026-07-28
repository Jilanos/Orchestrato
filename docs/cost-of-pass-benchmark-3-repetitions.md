# Conclusion technique — benchmark Cost of Pass (3 répétitions)

## Objet

Ce document synthétise les trois séries complètes du benchmark Cost of Pass. Il
est autonome afin qu'un agent ou un opérateur puisse reprendre le travail sans
dépendre des fichiers JSONL externes.

## Périmètre exécuté

| Axe | Valeurs |
|---|---|
| Modèles demandés | `default`, `gpt-5.5` |
| Modèle retourné pour `default` | `gpt-5.6-terra` |
| Routes | `direct_minimal_context`, `direct_expanded_context`, `adaptive_orchestration`, `fixed_plan_implement_review` |
| Catégories | `bounded_feature`, `cross_module_change`, `high_risk_change` |
| Répétitions | 3 |

La matrice fait `2 × 4 × 3 × 3 = 72` runs exploitables. Les worktrees ont été
recréés entre répétitions. Les tentatives partielles ou interrompues sont
exclues des agrégats.

## Sens opérationnel des routes

| Route | Intention de politique | Mesure effective dans le runner |
|---|---|---|
| `direct_minimal_context` | Exécuteur unique avec paquet de tâche borné. | Un appel CDX unique invité à éviter le contexte non pertinent. |
| `direct_expanded_context` | Exécuteur unique avec contexte CDX plus large. | Un appel CDX unique invité à utiliser le contexte du dépôt. |
| `adaptive_orchestration` | Direct par défaut ; planification, revue et récupération sur risque ou échec. | Un appel CDX unique invité à adopter cette stratégie. |
| `fixed_plan_implement_review` | Planification, implémentation et revue systématiques. | Un appel CDX unique invité à simuler ces phases. |

### Limite de validité majeure

Le runner n'appelle pas encore planner, executor, reviewer et recovery comme
passes fournisseur séparées. Les chiffres comparent donc des **variantes de
prompt single-agent**, pas le coût d'une véritable chaîne multi-agent. En
particulier, `fixed_plan_implement_review` n'est pas la somme mesurée de trois
appels distincts.

## Scénarios et validation

Chaque catégorie utilise un worktree distinct et la même acceptance :

```bash
PYTHONPATH=src python3 -m pytest -q
```

Le manifeste ne contient pas encore de consigne fonctionnelle dédiée, de
fichiers cibles, ni d'oracle spécifique par scénario. Les catégories sont donc
des étiquettes de worktree. Un pytest passant confirme que la suite présente
passe après le run ; il ne prouve pas qu'une fonctionnalité précise a été
réalisée. C'est la principale limite à corriger avant une décision de
production.

## Contrat de données

Chaque run enregistre le modèle demandé et retourné, la route, le scénario, la
répétition, le statut de validation, la durée, les retries, les tokens et la
référence CDX (`raw_run_ref`).

```text
coût_par_passage_réussi = somme(total_tokens) / nombre_de_runs_passed
```

Les champs `new_input_tokens` et `cached_input_tokens` sont nuls dans ces
captures : CDX ne retournait pas ces détails. Aucune conclusion sur le cache ou
la taille réelle du contexte ne doit donc reposer sur ces valeurs.

## Résultats consolidés

Résultat global : **72 runs**, **71 réussites (98,6 %)** et **40 199 668
tokens**.

| Modèle demandé | Runs | Réussites | Taux | Tokens | Coût/pass | Durée moyenne |
|---|---:|---:|---:|---:|---:|---:|
| `default` (`gpt-5.6-terra`) | 36 | 35 | 97,2 % | 13 985 967 | 399 599 | 109 s |
| `gpt-5.5` | 36 | 36 | 100 % | 26 213 701 | 728 158 | 183 s |

| Modèle | Route | Runs | Réussites | Coût/pass | Durée moyenne | Lecture |
|---|---|---:|---:|---:|---:|---|
| `default` | `direct_minimal_context` | 9 | 8 | 330 616 | 88 s | Moins cher, mais un échec. |
| `default` | `adaptive_orchestration` | 9 | 9 | 361 697 | 103 s | Meilleur compromis observé. |
| `default` | `direct_expanded_context` | 9 | 9 | 386 292 | 110 s | Plus coûteux sans gain visible. |
| `default` | `fixed_plan_implement_review` | 9 | 9 | 512 126 | 136 s | Coûteux ; bénéfice non démontré ici. |
| `gpt-5.5` | `direct_minimal_context` | 9 | 9 | 627 864 | 168 s | Fiable, mais nettement plus cher. |
| `gpt-5.5` | `adaptive_orchestration` | 9 | 9 | 706 495 | 189 s | Plus cher que default adaptive. |
| `gpt-5.5` | `direct_expanded_context` | 9 | 9 | 748 580 | 169 s | Aucun gain de réussite observé. |
| `gpt-5.5` | `fixed_plan_implement_review` | 9 | 9 | 829 695 | 207 s | Route et modèle les plus coûteux. |

## Politique recommandée

1. **Politique standard : `default / adaptive_orchestration`.** 9/9 réussites
   et environ 361 697 tokens par passage réussi ; meilleur compromis observé.
2. **Tâches petites et réversibles : `default / direct_minimal_context`.**
   Environ 8,6 % moins coûteux qu'adaptive, mais 8/9 réussites : la validation
   doit déclencher un fallback vers adaptive ou recovery.
3. **Contexte étendu : opt-in avec preuve.** Sous `default`, la route coûte
   environ 6,8 % de plus qu'adaptive sans gain observé.
4. **Plan-revue fixe : uniquement risque élevé.** Migrations, persistance,
   sécurité, intégrations externes ou releases critiques. Sous `default`, le
   surcoût est d'environ 41,6 % par rapport à adaptive.
5. **`gpt-5.5` : palier d'escalade.** 36/36 réussites, mais environ 82,2 % plus
   cher par passage réussi que le modèle par défaut. L'utiliser si le risque,
   un échec répété ou un gain de qualité mesuré justifie ce budget.

## Travail requis avant généralisation

1. Définir par scénario une tâche fonctionnelle immuable, des fichiers cibles
   et une acceptance dédiée.
2. Faire exécuter les vraies étapes Orchestrato séparément et mesurer le
   contexte/tokens à chaque étape.
3. Ajouter un évaluateur indépendant : tests cachés, revue diff ou rework
   humain.
4. Terminer les répétitions 4 et 5, puis analyser moyenne, médiane et variance.

## Règle courte pour un agent

```text
SI tâche bornée + faible risque + validation déterministe :
  default/direct_minimal_context ; si échec, escalade vers adaptive.

SI tâche normale ou contexte incertain :
  default/adaptive_orchestration.

SI migration, schéma, sécurité, intégration externe ou release critique :
  vraie chaîne plan -> implement -> review ; gpt-5.5 seulement si le risque ou
  une première tentative ratée justifie son surcoût.
```
