SELECT
    date,
    SUM(prod_price * prod_qty) AS ventes -- Calcule le chiffre d'affaires (prix * quantité) et le nomme 'ventes'
FROM
    TRANSACTIONS
WHERE
    date >= '2019-01-01' AND date <= '2019-12-31' -- Filtre les transactions pour la période du 1er janvier au 31 décembre 2019
GROUP BY
    date -- Regroupe les résultats par date pour obtenir le total par jour
ORDER BY
    date; -- Trie les résultats par date croissante
