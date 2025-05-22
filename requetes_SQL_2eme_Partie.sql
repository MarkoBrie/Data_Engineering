SELECT
    t.client_id, -- Sélectionne l'identifiant du client
    SUM(CASE WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble, -- Calcule les ventes pour les produits de type 'MEUBLE'
    SUM(CASE WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco -- Calcule les ventes pour les produits de type 'DECO'
FROM
    TRANSACTIONS AS t -- Alias la table TRANSACTIONS en 't'
JOIN
    PRODUCT_NOMENCLATURE AS pn ON t.prod_id = pn.product_id -- Joint les deux tables sur l'identifiant du produit pour obtenir le type de produit
WHERE
    t.date >= '2019-01-01' AND t.date <= '2019-12-31' -- Filtre les transactions pour la période du 1er janvier au 31 décembre 2019
GROUP BY
    t.client_id -- Regroupe les résultats par client pour obtenir les totaux par client
ORDER BY
    t.client_id; -- Trie les résultats par identifiant client